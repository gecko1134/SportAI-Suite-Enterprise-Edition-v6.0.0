#!/usr/bin/env bash
# Nightly scheduler for SportAI FinCast: Ops
# Usage (cron):  15 22 * * * /path/to/cron_run_all.sh >> /path/to/cron_run_all.log 2>&1
set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"
cd "$BASE_DIR"

# Load .env if present
if [ -f ".env" ]; then
  set -a
  source .env
  set +a
fi

# Create venv if missing and install deps
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

# Run pipeline with email enabled using ENV defaults
python modules/run_all.py \
  --email \
  --email-to "${BOARD_EMAILS:-board@nationalsportsdome.com}"
