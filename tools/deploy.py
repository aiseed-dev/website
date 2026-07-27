#!/usr/bin/env python3
"""ビルドしてデプロイする。実行: python3 deploy.py"""
import subprocess
import sys

from cloudflare_pages_deploy import deploy

# subprocess.run([sys.executable, "build.py"], check=True)  
# いつもの生成コマンドに読み替え
deploy("./html", project="aiseed-dev")
