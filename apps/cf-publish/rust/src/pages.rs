//! Cloudflare Pages Direct Upload deploy logic.
//!
//! This mirrors the canonical Python implementation
//! (`tools/cloudflare_pages_deploy.py`) using the same half-public Direct
//! Upload API that wrangler drives. The public entry point is [`deploy`],
//! kept free of `process::exit` so a future GUI (Tauri/egui) can reuse it.

use std::collections::BTreeMap;
use std::path::{Path, PathBuf};

use anyhow::{anyhow, bail, Context, Result};
use base64::engine::general_purpose::STANDARD as B64;
use base64::Engine as _;
use reqwest::blocking::{multipart, Client};
use serde::Deserialize;
use serde_json::{json, Value};

const API: &str = "https://api.cloudflare.com/client/v4";
const MAX_FILE_SIZE: u64 = 25 * 1024 * 1024; // Pages per-file limit (25 MiB)
const BATCH_BYTES: usize = 30 * 1024 * 1024; // soft cap per upload call
const BATCH_FILES: usize = 500; // soft cap per upload call

/// Generic Cloudflare API envelope: `{ success, errors, result }`.
#[derive(Deserialize)]
struct CfEnvelope {
    #[serde(default)]
    success: bool,
    #[serde(default)]
    errors: Value,
    #[serde(default)]
    result: Value,
}

/// Parse a Cloudflare response body, returning `result` on success or an
/// error carrying the `errors` array on `success == false`.
fn cf_result(url: &str, body: &str) -> Result<Value> {
    let env: CfEnvelope = serde_json::from_str(body)
        .with_context(|| format!("invalid JSON from {url}: {body}"))?;
    if !env.success {
        bail!("Cloudflare API error from {url}: {}", env.errors);
    }
    Ok(env.result)
}

/// Load a `KEY=VALUE` env file; existing process env vars take precedence.
fn load_env_file(path: &Path) {
    let Ok(text) = std::fs::read_to_string(path) else {
        return;
    };
    for line in text.lines() {
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        if let Some((key, value)) = line.split_once('=') {
            let key = key.trim();
            if std::env::var_os(key).is_none() {
                std::env::set_var(key, value.trim());
            }
        }
    }
}

/// Per-file hash, matching wrangler: `blake3(base64(bytes) ++ ext).hex()[:32]`.
fn file_hash(data: &[u8], suffix: &str) -> String {
    let b64 = B64.encode(data);
    let mut input = b64.into_bytes();
    input.extend_from_slice(suffix.as_bytes());
    let hex = blake3::hash(&input).to_hex();
    hex[..32].to_string()
}

/// Collect deployable files under `root`.
///
/// Skips dotfiles and dot-directories. Errors if any file exceeds 25 MiB.
/// Returns a map of `url_path` ("/" + relative posix path) -> file path.
fn collect(root: &Path) -> Result<BTreeMap<String, PathBuf>> {
    let mut files = BTreeMap::new();
    for entry in walkdir::WalkDir::new(root)
        .follow_links(true)
        .sort_by_file_name()
        .into_iter()
        .filter_entry(|e| {
            // Skip any entry whose own name starts with '.' (the root itself
            // has file_name() of its last component; depth 0 is always kept).
            e.depth() == 0
                || e.file_name()
                    .to_str()
                    .map(|n| !n.starts_with('.'))
                    .unwrap_or(false)
        })
    {
        let entry = entry.context("error walking directory")?;
        if !entry.file_type().is_file() {
            continue;
        }
        let path = entry.path();
        let rel = path
            .strip_prefix(root)
            .with_context(|| format!("path not under root: {}", path.display()))?;
        // Build a posix relative path.
        let rel_posix = rel
            .components()
            .map(|c| c.as_os_str().to_string_lossy())
            .collect::<Vec<_>>()
            .join("/");
        let size = entry
            .metadata()
            .with_context(|| format!("cannot stat {}", path.display()))?
            .len();
        if size > MAX_FILE_SIZE {
            bail!("{} exceeds 25 MiB (Pages per-file limit)", path.display());
        }
        files.insert(format!("/{rel_posix}"), path.to_path_buf());
    }
    if files.is_empty() {
        bail!("no files found under {}", root.display());
    }
    Ok(files)
}

/// MIME type guessed from extension, defaulting to octet-stream.
fn content_type(path: &Path) -> String {
    mime_guess::from_path(path)
        .first_raw()
        .unwrap_or("application/octet-stream")
        .to_string()
}

/// Wrapper around the account-scoped Pages endpoints (Bearer = API token).
struct Pages {
    base: String,
    client: Client,
}

impl Pages {
    fn new(account_id: &str) -> Result<Self> {
        let client = Client::builder()
            .timeout(std::time::Duration::from_secs(120))
            .build()
            .context("building HTTP client")?;
        Ok(Self {
            base: format!("{API}/accounts/{account_id}/pages"),
            client,
        })
    }

    fn bearer(&self, req: reqwest::blocking::RequestBuilder, token: &str) -> reqwest::blocking::RequestBuilder {
        req.bearer_auth(token)
    }

    fn project_exists(&self, project: &str, token: &str) -> Result<bool> {
        let url = format!("{}/projects/{project}", self.base);
        let resp = self
            .bearer(self.client.get(&url), token)
            .send()
            .with_context(|| format!("GET {url}"))?;
        let status = resp.status();
        let body = resp.text().unwrap_or_default();
        if status.as_u16() != 200 {
            return Ok(false);
        }
        let env: CfEnvelope = serde_json::from_str(&body).unwrap_or(CfEnvelope {
            success: false,
            errors: Value::Null,
            result: Value::Null,
        });
        Ok(env.success)
    }

    fn create_project(&self, project: &str, token: &str) -> Result<()> {
        let url = format!("{}/projects", self.base);
        let resp = self
            .bearer(self.client.post(&url), token)
            .json(&json!({ "name": project, "production_branch": "main" }))
            .send()
            .with_context(|| format!("POST {url}"))?;
        let body = resp.text().unwrap_or_default();
        cf_result(&url, &body)?;
        eprintln!("created project: {project}");
        Ok(())
    }

    fn upload_token(&self, project: &str, token: &str) -> Result<String> {
        let url = format!("{}/projects/{project}/upload-token", self.base);
        let resp = self
            .bearer(self.client.get(&url), token)
            .send()
            .with_context(|| format!("GET {url}"))?;
        let body = resp.text().unwrap_or_default();
        let result = cf_result(&url, &body)?;
        result
            .get("jwt")
            .and_then(|v| v.as_str())
            .map(|s| s.to_string())
            .ok_or_else(|| anyhow!("no jwt in upload-token response"))
    }

    fn deploy(
        &self,
        project: &str,
        manifest: &BTreeMap<String, String>,
        branch: &str,
        token: &str,
    ) -> Result<String> {
        let url = format!("{}/projects/{project}/deployments", self.base);
        let manifest_json = serde_json::to_string(manifest)?;
        let form = multipart::Form::new()
            .text("branch", branch.to_string())
            .part("manifest", multipart::Part::text(manifest_json));
        let resp = self
            .bearer(self.client.post(&url), token)
            .multipart(form)
            .send()
            .with_context(|| format!("POST {url}"))?;
        let body = resp.text().unwrap_or_default();
        let result = cf_result(&url, &body)?;
        Ok(result
            .get("url")
            .and_then(|v| v.as_str())
            .unwrap_or("(unknown URL)")
            .to_string())
    }
}

/// Upload missing assets using the deployment JWT against the global
/// `/pages/assets/*` endpoints, then re-affirm all hashes.
fn upload_assets(jwt: &str, by_hash: &BTreeMap<String, PathBuf>) -> Result<()> {
    let client = Client::builder()
        .timeout(std::time::Duration::from_secs(300))
        .build()
        .context("building upload HTTP client")?;

    let all_hashes: Vec<&String> = by_hash.keys().collect();

    // check-missing
    let url = format!("{API}/pages/assets/check-missing");
    let resp = client
        .post(&url)
        .bearer_auth(jwt)
        .json(&json!({ "hashes": all_hashes }))
        .send()
        .with_context(|| format!("POST {url}"))?;
    let body = resp.text().unwrap_or_default();
    let result = cf_result(&url, &body)?;
    let missing: Vec<String> = serde_json::from_value(result).unwrap_or_default();
    eprintln!(
        "to upload: {} / {} files (rest already cached)",
        missing.len(),
        by_hash.len()
    );

    // upload in batches
    let upload_url = format!("{API}/pages/assets/upload");
    let mut batch: Vec<Value> = Vec::new();
    let mut batch_bytes = 0usize;

    let flush = |client: &Client, batch: &mut Vec<Value>, batch_bytes: &mut usize| -> Result<()> {
        if batch.is_empty() {
            return Ok(());
        }
        let n = batch.len();
        let resp = client
            .post(&upload_url)
            .bearer_auth(jwt)
            .json(&*batch)
            .send()
            .with_context(|| format!("POST {upload_url}"))?;
        let body = resp.text().unwrap_or_default();
        cf_result(&upload_url, &body)?;
        eprintln!("  sent {n} files");
        batch.clear();
        *batch_bytes = 0;
        Ok(())
    };

    for h in &missing {
        let path = by_hash
            .get(h)
            .ok_or_else(|| anyhow!("missing hash not in by_hash map: {h}"))?;
        let data = std::fs::read(path)
            .with_context(|| format!("reading {}", path.display()))?;
        let value = B64.encode(&data);
        batch.push(json!({
            "key": h,
            "value": value,
            "metadata": { "contentType": content_type(path) },
            "base64": true,
        }));
        batch_bytes += data.len();
        if batch_bytes >= BATCH_BYTES || batch.len() >= BATCH_FILES {
            flush(&client, &mut batch, &mut batch_bytes)?;
        }
    }
    flush(&client, &mut batch, &mut batch_bytes)?;

    // upsert-hashes: affirm all hashes are still in use (same as wrangler).
    let url = format!("{API}/pages/assets/upsert-hashes");
    let resp = client
        .post(&url)
        .bearer_auth(jwt)
        .json(&json!({ "hashes": all_hashes }))
        .send()
        .with_context(|| format!("POST {url}"))?;
    let body = resp.text().unwrap_or_default();
    cf_result(&url, &body)?;

    Ok(())
}

/// Deploy `dir` to a Pages `project` on `branch`, optionally creating the
/// project if it does not exist. Returns the deployment URL.
///
/// Credentials are read from env (`CLOUDFLARE_API_TOKEN`,
/// `CLOUDFLARE_ACCOUNT_ID`), falling back to `~/.config/cloudflare/pages.env`.
pub fn deploy(dir: &Path, project: &str, branch: &str, create: bool) -> Result<String> {
    // env file: ~/.config/cloudflare/pages.env (env takes precedence)
    if let Some(home) = dirs_home() {
        load_env_file(&home.join(".config/cloudflare/pages.env"));
    }
    let token = std::env::var("CLOUDFLARE_API_TOKEN").ok();
    let account = std::env::var("CLOUDFLARE_ACCOUNT_ID").ok();
    let (token, account) = match (token, account) {
        (Some(t), Some(a)) if !t.is_empty() && !a.is_empty() => (t, a),
        _ => bail!(
            "set CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID in the environment \
             or in ~/.config/cloudflare/pages.env"
        ),
    };

    if !dir.is_dir() {
        bail!("directory does not exist: {}", dir.display());
    }

    let files = collect(dir)?;
    let mut manifest: BTreeMap<String, String> = BTreeMap::new();
    let mut by_hash: BTreeMap<String, PathBuf> = BTreeMap::new();
    for (url_path, path) in &files {
        let data = std::fs::read(path)
            .with_context(|| format!("reading {}", path.display()))?;
        let suffix = path
            .extension()
            .and_then(|e| e.to_str())
            .unwrap_or("");
        let h = file_hash(&data, suffix);
        manifest.insert(url_path.clone(), h.clone());
        by_hash.insert(h, path.clone());
    }
    eprintln!("{} files ({} unique)", files.len(), by_hash.len());

    let pages = Pages::new(&account)?;
    if !pages.project_exists(project, &token)? {
        if create {
            pages.create_project(project, &token)?;
        } else {
            bail!("project does not exist: {project}");
        }
    }

    let jwt = pages.upload_token(project, &token)?;
    upload_assets(&jwt, &by_hash)?;
    let url = pages.deploy(project, &manifest, branch, &token)?;
    eprintln!("deploy complete: {url}");
    Ok(url)
}

/// Minimal home-dir lookup without pulling in an extra crate.
fn dirs_home() -> Option<PathBuf> {
    std::env::var_os("HOME").map(PathBuf::from)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn hash_matches_wrangler_shape() {
        // 32 hex chars, deterministic.
        let h = file_hash(b"hello world", "html");
        assert_eq!(h.len(), 32);
        assert!(h.chars().all(|c| c.is_ascii_hexdigit()));
        assert_eq!(h, file_hash(b"hello world", "html"));
        assert_ne!(h, file_hash(b"hello world", "css"));
    }

    #[test]
    fn content_type_guess() {
        assert_eq!(content_type(Path::new("a/b.html")), "text/html");
        assert_eq!(
            content_type(Path::new("a/b.unknownext")),
            "application/octet-stream"
        );
    }
}
