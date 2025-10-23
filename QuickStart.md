# SportAI FinCast: Ops — Quick Start

## Run (Mac/Linux)
```bash
./run.sh
```

## Run (Windows)
Double-click `run.bat` or run in Command Prompt.

## Data refresh
Replace CSVs in `data/`, then run:
```bash
.venv/bin/python modules/generate_forecast.py   # Mac/Linux
.venv\Scripts\python modules\generate_forecast.py  # Windows
```

## Dashboard
The app opens at http://localhost:8501


## Policies & Guardrails
Edit `data/policies.json` to tune pricing bands, notice windows, staffing thresholds, and protected hours.

- To reserve time blocks from automation, edit `data/protected_hours.csv` (per-zone/day/time).
- Data checks: `modules/validate_data.py` runs before forecasts to catch schema/values issues.

- Create a 1-pager PDF: run `python modules/generate_ops_report.py` or use the dashboard button.

- Emailing reports: set `SENDGRID_API_KEY` in your environment before using the dashboard email button.

- Import SportsKey CSV: use the dashboard section or run `python modules/sportskey_importer.py --in your_export.csv --tz America/Chicago`.

- Build signals from weather + events: `python modules/signals_loader.py --lat 46.747 --lon -92.2243 --start 2025-10-20 --end 2025-10-27 --events data/local_events_template.csv`

- One-click pipeline: `python modules/run_all.py --sportskey your.csv --lat 46.747 --lon -92.2243 --start 2025-10-20 --end 2025-10-27 --events data/local_events_template.csv`
