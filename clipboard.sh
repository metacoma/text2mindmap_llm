#!/usr/bin/env bash
cd "$(dirname "$0")"
source .venv/bin/activate
python3 text2mindmap.py --clipboard
