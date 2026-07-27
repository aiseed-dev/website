# cf-publish (Flutter)

A small **desktop GUI** that publishes a local folder to **Cloudflare Pages**
using the same half-public *Direct Upload* API that `wrangler` drives — with
**no npm, no wrangler, and no terminal**. It is aimed at designers: pick a
folder, type a project name, press **Publish**, copy the URL.

This is the native-Flutter entry in a 3-way trial (Rust CLI vs Flet GUI vs
Flutter GUI). The reference behaviour is `tools/cloudflare_pages_deploy.py`;
the deploy logic here is a faithful reimplementation in Dart
(`lib/deploy.dart`). The selling point versus the others is the UI: the most
polished, consumer-grade cross-platform surface, with a credible path to
mobile later, paid for by reimplementing the Cloudflare flow in Dart.

> [!IMPORTANT]
> **This scaffold was authored without a Flutter toolchain.** The container it
> was written in has **no Flutter SDK and no `dart`**, so it was never run
> through `flutter pub get`, the analyzer, or a build. Treat it as a *reviewed
> scaffold*, not a verified build. The Dart syntax, imports, and `pubspec.yaml`
> were hand-written to compile, but expect to fix small things on first run —
> in particular the BLAKE3 dependency (see below).

## What it does

Single Material window:

- **Project name** text field (required).
- **Choose folder** button (native directory picker via `file_picker`'s
  `getDirectoryPath`); the chosen path is shown and remembered between runs.
- **Branch** dropdown: `main (production)` (default) or `preview`.
- **Publish** button — disabled with a spinner while a deploy runs; the deploy
  runs asynchronously so the UI never blocks.
- A scrollable **log**.
- On success, a selectable **URL** with **Copy** and **Open in browser**.
- A **Settings** dialog for `CLOUDFLARE_API_TOKEN` + `CLOUDFLARE_ACCOUNT_ID`,
  saved to `~/.config/cloudflare/pages.env` as `KEY=VALUE` (the same file the
  Python tool reads). It opens automatically on first run if creds are missing.

## Project layout

```
flutter/
  pubspec.yaml            # deps: http, blake3, file_picker, path, mime, url_launcher
  analysis_options.yaml   # flutter_lints
  .gitignore
  README.md               # this file
  lib/
    main.dart             # Flutter app + the single-window UI (thin)
    deploy.dart           # UI-agnostic deploy engine (mirrors the Python tool)
    config.dart           # load/save creds + last-used folder/project
```

### Platform folders are intentionally omitted

There is **no `macos/`, `linux/`, `windows/`, `android/`, `ios/`, or `web/`**
directory. Those are generated, boilerplate-heavy runners that depend on the
local Flutter version, and they could not be produced here without the SDK.

On a machine with Flutter installed, generate them once with:

```sh
cd apps/cf-publish/flutter
flutter create --platforms=macos,linux .
```

This adds the desktop runner folders **without** overwriting `lib/`,
`pubspec.yaml`, or `README.md`. (Add `windows` to the list if you want it.)

## Build & run (on a real machine)

```sh
cd apps/cf-publish/flutter
flutter create --platforms=macos,linux .   # one-time: generate runners
flutter pub get
flutter run -d macos                        # or:  flutter run -d linux
```

Desktop entitlements: `file_picker` and `url_launcher` work out of the box on
macOS/linux. On macOS you may need network + user-selected-file entitlements in
`macos/Runner/*.entitlements` for a *release* build (debug is unrestricted).

## BLAKE3 dependency must be verified

Cloudflare Pages content keys are
`blake3( base64(fileBytes) + extensionWithoutDot )`, hex, first 32 chars — the
exact scheme `wrangler` uses. **This requires BLAKE3, which is _not_ in the
`crypto` package.** The `pubspec.yaml` references a pub package named `blake3`,
and `lib/deploy.dart` calls `hashData(...)` and reads `.toString()` as the
lowercase hex digest.

Because this was written without a working pub resolver, the package **name,
version, and exact API are UNCONFIRMED**. On a real machine:

1. Run `flutter pub get`. If the `blake3` constraint does not resolve, search
   pub.dev for a maintained BLAKE3 package and swap it in `pubspec.yaml`.
2. Adjust **only** `Deployer.fileHash` in `lib/deploy.dart` to that package's
   API. The contract is fixed: *UTF-8 input bytes -> lowercase hex string*,
   then take the first 32 chars.
3. **Do not substitute a different hash** (SHA-256, etc.). The keys would be
   wrong and the Pages upload API would reject them. It must be BLAKE3.

A quick correctness check against the Python reference:

```sh
python3 -c "import base64,blake3; \
print(blake3.blake3((base64.b64encode(b'hello').decode()+'txt').encode()).hexdigest()[:32])"
```

The Dart `fileHash(utf8.encode('hello'), 'txt')` must produce the same 32 chars.

## Deploy flow (lib/deploy.dart)

Mirrors `tools/cloudflare_pages_deploy.py`. API base
`https://api.cloudflare.com/client/v4`; `pagesBase =
$API/accounts/$account/pages`.

1. Recursively list files under the chosen dir; skip any path segment starting
   with `.`; throw if a file exceeds 25 MiB. `urlPath = "/" + relative posix
   path`.
2. `manifest = {urlPath: hash}`, `byHash = {hash: file}` using the BLAKE3 key
   above.
3. `GET  $pagesBase/projects/$project` — does it exist? If not (and create is
   on) `POST $pagesBase/projects {name, production_branch:"main"}`.
4. `GET  $pagesBase/projects/$project/upload-token` -> `result.jwt`.
5. With the JWT as Bearer against `$API/pages/assets/*`:
   `POST /check-missing {hashes}` -> missing list;
   `POST /upload` a JSON array of
   `{key, value: base64, metadata:{contentType}, base64:true}`, batched to
   ~500 files / ~30 MB; then `POST /upsert-hashes {hashes}`.
6. `POST $pagesBase/projects/$project/deployments` as multipart (field
   `branch`, field `manifest = jsonEncode(manifest)`) -> `result.url`.

Every Cloudflare response is the `{success, errors, result}` envelope; the
engine throws `DeployException` (carrying the `errors` array) on
`success != true`.

## Credentials

Read at startup, env first then file, matching the Python tool:

- `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` from the process
  environment, else from `~/.config/cloudflare/pages.env`.
- The Settings dialog writes that same file (and best-effort `chmod 600`).
- Last-used folder + project are persisted to `~/.config/cf_publish/state.env`
  purely for convenience.

There are **no Cloudflare credentials in this repo** and a live deploy is
untestable here regardless.
