from __future__ import annotations
from pathlib import Path
from typing import Optional
import pandas as pd

def run_all(base_dir: Path,
            sportskey_csv: Optional[Path] = None,
            tzname: str = "America/Chicago",
            lat: Optional[float] = None,
            lon: Optional[float] = None,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            local_events_csv: Optional[Path] = None,
            make_pdf: bool = True) -> dict:
    data_dir = base_dir / "data"
    out = {"steps": []}

    # 0) Validate current data (may fail, user can fix)
    from modules.validate_data import main as validate_main
    try:
        validate_main(data_dir)
        out["steps"].append("Validation: OK")
    except SystemExit as e:
        out["steps"].append(f"Validation failed: {e}")
        # continue; importer/signals may fix issues

    # 1) Optional: import SportsKey CSV to events_hourly.csv
    if sportskey_csv:
        from modules.sportskey_importer import import_sportskey_csv
        out_csv = data_dir / "events_hourly.csv"
        map_json = data_dir / "mappings" / "sportskey_map.json"
        import_sportskey_csv(Path(sportskey_csv), out_csv, map_json, tzname)
        out["steps"].append(f"Imported SportsKey → {out_csv.name}")

    # 2) Build signals if params provided
    if lat is not None and lon is not None and start_date and end_date:
        from modules.signals_loader import build_signals_csv
        sig_out = data_dir / "signals_hourly.csv"
        build_signals_csv(float(lat), float(lon), start_date, end_date, local_events_csv, sig_out)
        out["steps"].append(f"Signals built → {sig_out.name}")

    # 3) Forecast
    from modules.generate_forecast import main as gen_forecast
    gen_forecast(data_dir)
    out["steps"].append("Forecast generated")

    # 4) Suggestions / rules engine
    from modules.rules_engine import suggest_actions
    acts = suggest_actions(data_dir)
    (data_dir / "actions_log.csv").write_text(acts.to_csv(index=False))
    out["steps"].append(f"Suggestions written → actions_log.csv ({len(acts)} rows)")

    # 5) PDF
    pdf_path = None
    if make_pdf:
        from modules.ops_report_pdf import generate_pdf
        pdf_path = generate_pdf(base_dir)
        out["steps"].append(f"Ops report → {pdf_path.name}")
        out["pdf"] = str(pdf_path)
    return out

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Run validation → import → signals → forecast → suggestions → PDF")
    p.add_argument("--sportskey", default="", help="Optional path to SportsKey CSV")
    p.add_argument("--tz", default="America/Chicago")
    p.add_argument("--lat", type=float, default=None)
    p.add_argument("--lon", type=float, default=None)
    p.add_argument("--start", default=None)
    p.add_argument("--end", default=None)
    p.add_argument("--events", default="", help="Optional local events CSV")
    p.add_argument("--no-pdf", action="store_true")
    args = p.parse_args()
    base_dir = Path(__file__).resolve().parents[1]
    sk = Path(args.sportskey) if args.sportskey else None
    ev = Path(args.events) if args.events else None
    res = run_all(base_dir, sk, args.tz, args.lat, args.lon, args.start, args.end, ev, make_pdf=not args.no_pdf)
    print("\n".join(res.get("steps", [])))
    if res.get("pdf"):
        print(f"PDF: {res['pdf']}")
