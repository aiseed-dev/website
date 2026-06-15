//! `cf-publish` — deploy a local folder to Cloudflare Pages with no npm or
//! wrangler dependency, using the same half-public Direct Upload API.

use std::path::PathBuf;
use std::process::ExitCode;

use clap::Parser;

mod pages;

/// Deploy a local folder to Cloudflare Pages via the Direct Upload API.
#[derive(Parser, Debug)]
#[command(name = "cf-publish", version, about, long_about = None)]
struct Cli {
    /// Public directory whose contents become the site.
    directory: PathBuf,

    /// Pages project name.
    #[arg(long)]
    project: String,

    /// Branch: "main" = production, anything else = preview URL.
    #[arg(long, default_value = "main")]
    branch: String,

    /// Do not create the project if it is missing (error instead).
    #[arg(long)]
    no_create: bool,
}

fn main() -> ExitCode {
    let cli = Cli::parse();
    match pages::deploy(&cli.directory, &cli.project, &cli.branch, !cli.no_create) {
        Ok(url) => {
            println!("{url}");
            ExitCode::SUCCESS
        }
        Err(err) => {
            eprintln!("error: {err:#}");
            ExitCode::FAILURE
        }
    }
}
