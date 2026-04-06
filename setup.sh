#!/bin/bash
# Setup script for aiseed.dev build environment
#
# Usage:
#   ./setup.sh
#
# This installs Python dependencies and applies the CJK emphasis fix
# to markdown-it-py. Run once after cloning or creating a new venv.

set -e

pip install -r requirements.txt
python3 tools/patches/markdown_it_cjk_emphasis.py
echo "Setup complete."
