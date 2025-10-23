#!/usr/bin/env bash
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Create venv
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

# 0) Validate data
    python modules/validate_data.py

    # 1) Generate forecasts (creates data/forecast_48h.csv, etc.)
python modules/generate_forecast.py

# 2) Launch Streamlit dashboard
streamlit run dashboard/app.py

# Optional: Run the full pipeline if RUN_ALL=1
if [ "${RUN_ALL:-0}" = "1" ]; then
  python modules/run_all.py ${RUN_ALL_ARGS:-}
  exit 0
fi
