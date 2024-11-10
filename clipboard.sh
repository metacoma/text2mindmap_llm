#!/usr/bin/env bash
set -ex
cd "$(dirname "$0")"
source .venv/bin/activate
python3 ./text2mindmap.py --clipboard $*
