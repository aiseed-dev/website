import 'dart:convert';
import 'dart:io';

import 'package:blake3/blake3.dart';
import 'package:http/http.dart' as http;
import 'package:mime/mime.dart' as mime;
import 'package:path/path.dart' as p;

/// Cloudflare API base.
const String kApiBase = 'https://api.cloudflare.com/client/v4';

/// Pages limit: a single asset may not exceed 25 MiB.
const int kMaxFileSize = 25 * 1024 * 1024;

/// Target byte budget for one upload batch call.
const int kBatchBytes = 30 * 1024 * 1024;

/// Max files per upload batch call.
const int kBatchFiles = 500;

/// Thrown when the deploy flow fails. [details] carries the Cloudflare
/// `errors` array (if any) for display in the log.
class DeployException implements Exception {
  DeployException(this.message, {this.details});
  final String message;
  final Object? details;

  @override
  String toString() {
    if (details == null) return 'DeployException: $message';
    return 'DeployException: $message\n${jsonEncode(details)}';
  }
}

/// A file discovered under the publish root.
class _Asset {
  _Asset(this.urlPath, this.file);

  /// POSIX URL path, e.g. `/index.html`.
  final String urlPath;
  final File file;
}

/// Inputs for a deploy run.
class DeployRequest {
  DeployRequest({
    required this.directory,
    required this.project,
    required this.branch,
    required this.apiToken,
    required this.accountId,
    this.create = true,
  });

  final String directory;
  final String project;
  final String branch;
  final String apiToken;
  final String accountId;
  final bool create;
}

/// Progress callback signature. [message] is human-readable log text.
typedef ProgressCallback = void Function(String message);

/// UI-agnostic deploy engine. Mirrors `tools/cloudflare_pages_deploy.py`.
///
/// Construct with the request, then call [run]. Reports progress through
/// [onProgress] and returns the deployment URL, or throws [DeployException].
class Deployer {
  Deployer(this.request, {ProgressCallback? onProgress})
      : onProgress = onProgress ?? ((_) {});

  final DeployRequest request;
  final ProgressCallback onProgress;

  final http.Client _client = http.Client();

  void _log(String message) => onProgress(message);

  /// Run the full deploy flow and return the deployment URL.
  Future<String> run() async {
    try {
      final root = Directory(request.directory);
      if (!root.existsSync()) {
        throw DeployException('Directory not found: ${request.directory}');
      }
      if (request.project.trim().isEmpty) {
        throw DeployException('Project name is required.');
      }

      _log('Scanning ${request.directory} ...');
      final assets = _collect(root);
      if (assets.isEmpty) {
        throw DeployException('No files found under ${request.directory}');
      }

      // Build manifest {urlPath: hash} and byHash {hash: file}.
      final manifest = <String, String>{};
      final byHash = <String, File>{};
      for (final asset in assets) {
        final bytes = await asset.file.readAsBytes();
        final suffix = p.extension(asset.file.path).replaceFirst('.', '');
        final hash = fileHash(bytes, suffix);
        manifest[asset.urlPath] = hash;
        byHash[hash] = asset.file;
      }
      _log('${assets.length} files (${byHash.length} unique).');

      final pagesBase =
          '$kApiBase/accounts/${request.accountId}/pages';

      // 1. Ensure the project exists.
      if (!await _projectExists(pagesBase)) {
        if (request.create) {
          await _createProject(pagesBase);
          _log('Created project: ${request.project}');
        } else {
          throw DeployException('Project does not exist: ${request.project}');
        }
      }

      // 2. Get a short-lived upload JWT.
      final jwt = await _uploadToken(pagesBase);

      // 3. Upload the missing assets using the JWT.
      await _uploadAssets(jwt, byHash);

      // 4. Create the deployment with the manifest.
      final url = await _deploy(pagesBase, manifest);
      _log('Deploy complete: $url');
      return url;
    } finally {
      _client.close();
    }
  }

  /// wrangler / Cloudflare Pages content key:
  ///   blake3( base64(bytes) + extWithoutDot ).hexdigest()[:32]
  ///
  /// This MUST be BLAKE3 — substituting SHA-256 etc. produces keys the Pages
  /// upload API rejects. The single line below is the only point that depends
  /// on the `blake3` pub package's exact surface; if `flutter pub get` resolves
  /// a package whose API differs, adjust *only* this call (see README ->
  /// "BLAKE3 dependency must be verified"). The contract this function must
  /// honour: input UTF-8 bytes -> lowercase hex string of the digest.
  static String fileHash(List<int> bytes, String suffix) {
    final b64 = base64.encode(bytes);
    // `hashData` returns a Digest whose `toString()` is the lowercase hex.
    final Digest digest = hashData(utf8.encode(b64 + suffix));
    final String hex = digest.toString();
    return hex.substring(0, 32);
  }

  /// Recursively collect files; skip dotfiles/dot-dirs; enforce size limit.
  List<_Asset> _collect(Directory root) {
    final assets = <_Asset>[];
    final entities = root.listSync(recursive: true, followLinks: true);
    for (final entity in entities) {
      if (entity is! File) continue;
      final rel = p.relative(entity.path, from: root.path);
      final posixRel = p.posix.joinAll(p.split(rel));
      // Skip if any path segment starts with a dot (e.g. .git/, .DS_Store).
      final segments = p.split(rel);
      if (segments.any((s) => s.startsWith('.'))) continue;

      final size = entity.lengthSync();
      if (size > kMaxFileSize) {
        throw DeployException(
          'File exceeds 25 MiB (Pages limit): ${entity.path}',
        );
      }
      assets.add(_Asset('/$posixRel', entity));
    }
    assets.sort((a, b) => a.urlPath.compareTo(b.urlPath));
    return assets;
  }

  Map<String, String> get _authHeaders => {
        'Authorization': 'Bearer ${request.apiToken}',
      };

  /// Unwrap a Cloudflare `{success, errors, result}` envelope or throw.
  Map<String, dynamic> _unwrap(http.Response resp, String what) {
    Map<String, dynamic> body;
    try {
      body = jsonDecode(resp.body) as Map<String, dynamic>;
    } catch (_) {
      throw DeployException(
        '$what: unexpected response (HTTP ${resp.statusCode})',
        details: resp.body,
      );
    }
    if (body['success'] != true) {
      throw DeployException('$what failed', details: body['errors']);
    }
    return body;
  }

  Future<bool> _projectExists(String pagesBase) async {
    final resp = await _client.get(
      Uri.parse('$pagesBase/projects/${request.project}'),
      headers: _authHeaders,
    );
    if (resp.statusCode != 200) return false;
    try {
      final body = jsonDecode(resp.body) as Map<String, dynamic>;
      return body['success'] == true;
    } catch (_) {
      return false;
    }
  }

  Future<void> _createProject(String pagesBase) async {
    final resp = await _client.post(
      Uri.parse('$pagesBase/projects'),
      headers: {..._authHeaders, 'Content-Type': 'application/json'},
      body: jsonEncode({
        'name': request.project,
        'production_branch': 'main',
      }),
    );
    _unwrap(resp, 'Create project');
  }

  Future<String> _uploadToken(String pagesBase) async {
    final resp = await _client.get(
      Uri.parse('$pagesBase/projects/${request.project}/upload-token'),
      headers: _authHeaders,
    );
    final body = _unwrap(resp, 'Get upload token');
    final result = body['result'] as Map<String, dynamic>;
    final jwt = result['jwt'] as String?;
    if (jwt == null || jwt.isEmpty) {
      throw DeployException('Upload token response had no jwt.');
    }
    return jwt;
  }

  /// Upload missing assets via the `pages/assets/*` endpoints using the JWT.
  Future<void> _uploadAssets(String jwt, Map<String, File> byHash) async {
    final jwtHeaders = {'Authorization': 'Bearer $jwt'};

    Map<String, dynamic> unwrapUpload(http.Response resp, String what) {
      Map<String, dynamic> body;
      try {
        body = jsonDecode(resp.body) as Map<String, dynamic>;
      } catch (_) {
        throw DeployException(
          '$what: unexpected response (HTTP ${resp.statusCode})',
          details: resp.body,
        );
      }
      if (body['success'] != true) {
        throw DeployException('$what failed', details: body['errors']);
      }
      return body;
    }

    // check-missing -> list of hashes that still need uploading.
    final checkResp = await _client.post(
      Uri.parse('$kApiBase/pages/assets/check-missing'),
      headers: {...jwtHeaders, 'Content-Type': 'application/json'},
      body: jsonEncode({'hashes': byHash.keys.toList()}),
    );
    final missingBody = unwrapUpload(checkResp, 'check-missing');
    final missing = (missingBody['result'] as List).cast<String>();
    _log('To upload: ${missing.length} / ${byHash.length} files '
        '(rest already cached).');

    // Batched upload.
    var batch = <Map<String, dynamic>>[];
    var batchBytes = 0;

    Future<void> flush() async {
      if (batch.isEmpty) return;
      final resp = await _client.post(
        Uri.parse('$kApiBase/pages/assets/upload'),
        headers: {...jwtHeaders, 'Content-Type': 'application/json'},
        body: jsonEncode(batch),
      );
      unwrapUpload(resp, 'upload');
      _log('  Sent ${batch.length} files.');
      batch = <Map<String, dynamic>>[];
      batchBytes = 0;
    }

    for (final hash in missing) {
      final file = byHash[hash]!;
      final bytes = await file.readAsBytes();
      final ctype =
          mime.lookupMimeType(file.path) ?? 'application/octet-stream';
      batch.add({
        'key': hash,
        'value': base64.encode(bytes),
        'metadata': {'contentType': ctype},
        'base64': true,
      });
      batchBytes += bytes.length;
      if (batchBytes >= kBatchBytes || batch.length >= kBatchFiles) {
        await flush();
      }
    }
    await flush();

    // upsert-hashes: declare all hashes still in use (matches wrangler).
    final upsertResp = await _client.post(
      Uri.parse('$kApiBase/pages/assets/upsert-hashes'),
      headers: {...jwtHeaders, 'Content-Type': 'application/json'},
      body: jsonEncode({'hashes': byHash.keys.toList()}),
    );
    unwrapUpload(upsertResp, 'upsert-hashes');
  }

  /// Create the deployment (multipart) and return the resulting URL.
  Future<String> _deploy(
    String pagesBase,
    Map<String, String> manifest,
  ) async {
    final uri =
        Uri.parse('$pagesBase/projects/${request.project}/deployments');
    final req = http.MultipartRequest('POST', uri)
      ..headers.addAll(_authHeaders)
      ..fields['branch'] = request.branch
      ..fields['manifest'] = jsonEncode(manifest);

    final streamed = await _client.send(req);
    final resp = await http.Response.fromStream(streamed);
    final body = _unwrap(resp, 'Create deployment');
    final result = body['result'] as Map<String, dynamic>;
    return (result['url'] as String?) ?? '(url unknown)';
  }
}
