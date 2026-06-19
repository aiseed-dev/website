import 'dart:io';

import 'package:path/path.dart' as p;

/// Loads and saves the Cloudflare credentials and the last-used folder.
///
/// Credentials live in `~/.config/cloudflare/pages.env` as `KEY=VALUE` lines
/// (the same file the Python deploy tool reads). Environment variables take
/// precedence over the file, mirroring the reference behaviour.
///
/// The last-used folder is a small convenience persisted next to the creds in
/// `~/.config/cf_publish/state.env`.
class AppConfig {
  AppConfig({
    required this.apiToken,
    required this.accountId,
    required this.lastFolder,
    required this.lastProject,
  });

  String? apiToken;
  String? accountId;
  String? lastFolder;
  String? lastProject;

  bool get hasCredentials =>
      (apiToken?.isNotEmpty ?? false) && (accountId?.isNotEmpty ?? false);

  /// `~/.config/cloudflare/pages.env`
  static File credsFile() =>
      File(p.join(_configHome(), 'cloudflare', 'pages.env'));

  /// `~/.config/cf_publish/state.env`
  static File stateFile() =>
      File(p.join(_configHome(), 'cf_publish', 'state.env'));

  static String _configHome() {
    final env = Platform.environment;
    final xdg = env['XDG_CONFIG_HOME'];
    if (xdg != null && xdg.isNotEmpty) return xdg;
    final home = env['HOME'] ?? env['USERPROFILE'] ?? '';
    return p.join(home, '.config');
  }

  /// Parse a `KEY=VALUE` env-style file. Blank lines and `#` comments skipped.
  static Map<String, String> _parseEnv(File file) {
    final map = <String, String>{};
    if (!file.existsSync()) return map;
    for (var line in file.readAsLinesSync()) {
      line = line.trim();
      if (line.isEmpty || line.startsWith('#') || !line.contains('=')) {
        continue;
      }
      final idx = line.indexOf('=');
      final key = line.substring(0, idx).trim();
      final value = line.substring(idx + 1).trim();
      if (key.isNotEmpty) map[key] = value;
    }
    return map;
  }

  /// Load creds (env overrides file) and persisted UI state.
  static Future<AppConfig> load() async {
    final fileEnv = _parseEnv(credsFile());
    final procEnv = Platform.environment;

    String? pick(String key) {
      final fromProc = procEnv[key];
      if (fromProc != null && fromProc.isNotEmpty) return fromProc;
      final fromFile = fileEnv[key];
      if (fromFile != null && fromFile.isNotEmpty) return fromFile;
      return null;
    }

    final state = _parseEnv(stateFile());

    return AppConfig(
      apiToken: pick('CLOUDFLARE_API_TOKEN'),
      accountId: pick('CLOUDFLARE_ACCOUNT_ID'),
      lastFolder: state['LAST_FOLDER'],
      lastProject: state['LAST_PROJECT'],
    );
  }

  /// Persist credentials to `~/.config/cloudflare/pages.env`.
  Future<void> saveCredentials() async {
    final file = credsFile();
    await file.parent.create(recursive: true);
    final buf = StringBuffer()
      ..writeln('# Written by cf_publish')
      ..writeln('CLOUDFLARE_API_TOKEN=${apiToken ?? ''}')
      ..writeln('CLOUDFLARE_ACCOUNT_ID=${accountId ?? ''}');
    await file.writeAsString(buf.toString());
    // Best-effort tighten perms (creds file). Ignored on platforms w/o chmod.
    try {
      if (!Platform.isWindows) {
        await Process.run('chmod', ['600', file.path]);
      }
    } catch (_) {
      // non-fatal
    }
  }

  /// Persist the last-used folder + project name for convenience.
  Future<void> saveState() async {
    final file = stateFile();
    await file.parent.create(recursive: true);
    final buf = StringBuffer()
      ..writeln('# Written by cf_publish')
      ..writeln('LAST_FOLDER=${lastFolder ?? ''}')
      ..writeln('LAST_PROJECT=${lastProject ?? ''}');
    await file.writeAsString(buf.toString());
  }
}
