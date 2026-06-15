import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:url_launcher/url_launcher.dart';

import 'config.dart';
import 'deploy.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final config = await AppConfig.load();
  runApp(CfPublishApp(config: config));
}

class CfPublishApp extends StatelessWidget {
  const CfPublishApp({super.key, required this.config});

  final AppConfig config;

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Cloudflare Pages Publisher',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorSchemeSeed: const Color(0xFFF6821F), // Cloudflare orange.
        brightness: Brightness.light,
      ),
      darkTheme: ThemeData(
        useMaterial3: true,
        colorSchemeSeed: const Color(0xFFF6821F),
        brightness: Brightness.dark,
      ),
      home: PublishPage(config: config),
    );
  }
}

class PublishPage extends StatefulWidget {
  const PublishPage({super.key, required this.config});

  final AppConfig config;

  @override
  State<PublishPage> createState() => _PublishPageState();
}

class _PublishPageState extends State<PublishPage> {
  late final TextEditingController _projectController;
  String? _folder;
  String _branch = 'main';
  bool _running = false;
  String? _resultUrl;
  final List<String> _log = [];
  final ScrollController _logScroll = ScrollController();

  static const _branches = {
    'main': 'main (production)',
    'preview': 'preview',
  };

  @override
  void initState() {
    super.initState();
    _projectController =
        TextEditingController(text: widget.config.lastProject ?? '');
    _folder = widget.config.lastFolder;

    // On first run, if creds are missing, open settings automatically.
    if (!widget.config.hasCredentials) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        _openSettings(force: true);
      });
    }
  }

  @override
  void dispose() {
    _projectController.dispose();
    _logScroll.dispose();
    super.dispose();
  }

  bool get _canPublish =>
      !_running &&
      _projectController.text.trim().isNotEmpty &&
      (_folder?.isNotEmpty ?? false);

  void _appendLog(String line) {
    setState(() => _log.add(line));
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_logScroll.hasClients) {
        _logScroll.jumpTo(_logScroll.position.maxScrollExtent);
      }
    });
  }

  Future<void> _chooseFolder() async {
    final path = await FilePicker.platform.getDirectoryPath(
      dialogTitle: 'Choose the folder to publish',
      initialDirectory: _folder,
    );
    if (path != null) {
      setState(() => _folder = path);
      widget.config.lastFolder = path;
      await widget.config.saveState();
    }
  }

  Future<void> _publish() async {
    if (!widget.config.hasCredentials) {
      _openSettings(force: true);
      return;
    }
    final project = _projectController.text.trim();
    widget.config.lastProject = project;
    await widget.config.saveState();

    setState(() {
      _running = true;
      _resultUrl = null;
      _log.clear();
    });

    final request = DeployRequest(
      directory: _folder!,
      project: project,
      branch: _branch,
      apiToken: widget.config.apiToken!,
      accountId: widget.config.accountId!,
      create: true,
    );

    try {
      final deployer = Deployer(request, onProgress: _appendLog);
      final url = await deployer.run();
      if (!mounted) return;
      setState(() => _resultUrl = url);
    } on DeployException catch (e) {
      _appendLog('ERROR: ${e.message}');
      if (e.details != null) _appendLog(e.details.toString());
    } catch (e) {
      _appendLog('ERROR: $e');
    } finally {
      if (mounted) setState(() => _running = false);
    }
  }

  Future<void> _openSettings({bool force = false}) async {
    await showDialog<void>(
      context: context,
      barrierDismissible: !force,
      builder: (_) => _SettingsDialog(config: widget.config, force: force),
    );
    if (mounted) setState(() {}); // refresh enabled state after saving
  }

  Future<void> _openUrl(String url) async {
    final uri = Uri.tryParse(url);
    if (uri != null) {
      await launchUrl(uri, mode: LaunchMode.externalApplication);
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(
        title: const Text('Cloudflare Pages Publisher'),
        actions: [
          IconButton(
            tooltip: 'Settings',
            onPressed: _running ? null : () => _openSettings(),
            icon: const Icon(Icons.settings_outlined),
          ),
        ],
      ),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 680),
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                TextField(
                  controller: _projectController,
                  enabled: !_running,
                  onChanged: (_) => setState(() {}),
                  decoration: const InputDecoration(
                    labelText: 'Project name',
                    hintText: 'e.g. my-site',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 16),
                Row(
                  children: [
                    Expanded(
                      child: OutlinedButton.icon(
                        onPressed: _running ? null : _chooseFolder,
                        icon: const Icon(Icons.folder_open),
                        label: const Text('Choose folder'),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      flex: 2,
                      child: Text(
                        _folder ?? 'No folder selected',
                        style: theme.textTheme.bodySmall,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 16),
                DropdownButtonFormField<String>(
                  value: _branch,
                  decoration: const InputDecoration(
                    labelText: 'Branch',
                    border: OutlineInputBorder(),
                  ),
                  items: _branches.entries
                      .map((e) => DropdownMenuItem(
                            value: e.key,
                            child: Text(e.value),
                          ))
                      .toList(),
                  onChanged: _running
                      ? null
                      : (v) => setState(() => _branch = v ?? 'main'),
                ),
                const SizedBox(height: 20),
                FilledButton.icon(
                  onPressed: _canPublish ? _publish : null,
                  icon: _running
                      ? const SizedBox(
                          width: 18,
                          height: 18,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Icon(Icons.cloud_upload_outlined),
                  label: Text(_running ? 'Publishing…' : 'Publish'),
                ),
                const SizedBox(height: 20),
                if (_resultUrl != null) _ResultCard(
                  url: _resultUrl!,
                  onCopy: () async {
                    await Clipboard.setData(ClipboardData(text: _resultUrl!));
                    if (mounted) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text('URL copied')),
                      );
                    }
                  },
                  onOpen: () => _openUrl(_resultUrl!),
                ),
                const SizedBox(height: 12),
                Text('Log', style: theme.textTheme.labelLarge),
                const SizedBox(height: 4),
                Expanded(
                  child: Container(
                    decoration: BoxDecoration(
                      color: theme.colorScheme.surfaceContainerHighest,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    padding: const EdgeInsets.all(12),
                    child: Scrollbar(
                      controller: _logScroll,
                      child: ListView.builder(
                        controller: _logScroll,
                        itemCount: _log.length,
                        itemBuilder: (_, i) => Text(
                          _log[i],
                          style: const TextStyle(
                            fontFamily: 'monospace',
                            fontSize: 12,
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _ResultCard extends StatelessWidget {
  const _ResultCard({
    required this.url,
    required this.onCopy,
    required this.onOpen,
  });

  final String url;
  final VoidCallback onCopy;
  final VoidCallback onOpen;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      color: theme.colorScheme.primaryContainer,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(Icons.check_circle_outline),
                const SizedBox(width: 8),
                Text('Published', style: theme.textTheme.titleMedium),
              ],
            ),
            const SizedBox(height: 8),
            SelectableText(url),
            const SizedBox(height: 8),
            Row(
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                TextButton.icon(
                  onPressed: onCopy,
                  icon: const Icon(Icons.copy, size: 18),
                  label: const Text('Copy'),
                ),
                const SizedBox(width: 8),
                FilledButton.tonalIcon(
                  onPressed: onOpen,
                  icon: const Icon(Icons.open_in_new, size: 18),
                  label: const Text('Open'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _SettingsDialog extends StatefulWidget {
  const _SettingsDialog({required this.config, required this.force});

  final AppConfig config;
  final bool force;

  @override
  State<_SettingsDialog> createState() => _SettingsDialogState();
}

class _SettingsDialogState extends State<_SettingsDialog> {
  late final TextEditingController _token;
  late final TextEditingController _account;
  bool _obscure = true;

  @override
  void initState() {
    super.initState();
    _token = TextEditingController(text: widget.config.apiToken ?? '');
    _account = TextEditingController(text: widget.config.accountId ?? '');
  }

  @override
  void dispose() {
    _token.dispose();
    _account.dispose();
    super.dispose();
  }

  Future<void> _save() async {
    widget.config.apiToken = _token.text.trim();
    widget.config.accountId = _account.text.trim();
    await widget.config.saveCredentials();
    if (mounted) Navigator.of(context).pop();
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Cloudflare credentials'),
      content: SizedBox(
        width: 460,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              'Saved to ~/.config/cloudflare/pages.env',
              style: Theme.of(context).textTheme.bodySmall,
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _token,
              obscureText: _obscure,
              decoration: InputDecoration(
                labelText: 'CLOUDFLARE_API_TOKEN',
                border: const OutlineInputBorder(),
                suffixIcon: IconButton(
                  icon: Icon(
                    _obscure ? Icons.visibility : Icons.visibility_off,
                  ),
                  onPressed: () => setState(() => _obscure = !_obscure),
                ),
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _account,
              decoration: const InputDecoration(
                labelText: 'CLOUDFLARE_ACCOUNT_ID',
                border: OutlineInputBorder(),
              ),
            ),
          ],
        ),
      ),
      actions: [
        if (!widget.force)
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Cancel'),
          ),
        FilledButton(
          onPressed: _save,
          child: const Text('Save'),
        ),
      ],
    );
  }
}
