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
            make_pdf: bool = True,
            email_after: bool = False,
            email_to: Optional[str] = None,
            email_from: str = "no-reply@nationalsportsdome.com",
            email_subject: str = "SportAI Ops Report",
            email_body: str = "Attached: latest 1-page Ops Report from SportAI FinCast.") -> dict:
    data_dir = base_dir / "data"
    out = {"steps": []}
    try:
        # Import from sibling modules when run from modules/ directory
        # or from modules.* when run from parent directory
        try:
            from validate_data import main as validate_main
        except ImportError:
            from modules.validate_data import main as validate_main
        validate_main(data_dir); out["steps"].append("Validation: OK")
    except SystemExit as e:
        out["steps"].append(f"Validation failed: {e}")
    if sportskey_csv:
        try:
            from sportskey_importer import import_sportskey_csv
        except ImportError:
            from modules.sportskey_importer import import_sportskey_csv
        out_csv = data_dir / "events_hourly.csv"
        map_json = data_dir / "mappings" / "sportskey_map.json"
        import_sportskey_csv(Path(sportskey_csv), out_csv, map_json, tzname)
        out["steps"].append(f"Imported SportsKey → {out_csv.name}")
    if lat is not None and lon is not None and start_date and end_date:
        try:
            from signals_loader import build_signals_csv
        except ImportError:
            from modules.signals_loader import build_signals_csv
        sig_out = data_dir / "signals_hourly.csv"
        build_signals_csv(float(lat), float(lon), start_date, end_date, local_events_csv, sig_out)
        out["steps"].append(f"Signals built → {sig_out.name}")
    try:
        from generate_forecast import main as gen_forecast
    except ImportError:
        from modules.generate_forecast import main as gen_forecast
    gen_forecast(data_dir); out["steps"].append("Forecast generated")
    try:
        from rules_engine import suggest_actions
    except ImportError:
        from modules.rules_engine import suggest_actions
    acts = suggest_actions(data_dir)
    (data_dir / "actions_log.csv").write_text(acts.to_csv(index=False))
    out["steps"].append(f"Suggestions written → actions_log.csv ({len(acts)} rows)")
    pdf_path = None
    if make_pdf:
        try:
            from ops_report_pdf import generate_pdf
        except ImportError:
            from modules.ops_report_pdf import generate_pdf
        pdf_path = generate_pdf(base_dir); out["steps"].append(f"Ops report → {pdf_path.name}")
        out["pdf"] = str(pdf_path)
        if email_after and email_to:
            try:
                try:
                    from email_sender import send_pdf_via_sendgrid
                except ImportError:
                    from modules.email_sender import send_pdf_via_sendgrid
                to_list = [e.strip() for e in str(email_to).split(",") if e.strip()]
                res = send_pdf_via_sendgrid(to_list, email_subject, email_body, pdf_path, from_email=email_from)
                out["steps"].append(f"Email sent: {res.get('ok', False)} {res.get('message','')}")
            except Exception as e:
                out["steps"].append(f"Email failed: {e}")
    return out

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Run validation → import → signals → forecast → suggestions → PDF (+ optional email)")
    p.add_argument("--sportskey", default="")
    p.add_argument("--tz", default="America/Chicago")
    p.add_argument("--lat", type=float, default=None)
    p.add_argument("--lon", type=float, default=None)
    p.add_argument("--start", default=None)
    p.add_argument("--end", default=None)
    p.add_argument("--events", default="")
    p.add_argument("--no-pdf", action="store_true")
    p.add_argument("--email", action="store_true")
    p.add_argument("--email-to", default="")
    p.add_argument("--email-from", default="no-reply@nationalsportsdome.com")
    p.add_argument("--email-subject", default="SportAI Ops Report")
    p.add_argument("--email-body", default="Attached: latest 1-page Ops Report from SportAI FinCast.")
    args = p.parse_args()
    base_dir = Path(__file__).resolve().parents[1]
    sk = Path(args.sportskey) if args.sportskey else None
    ev = Path(args.events) if args.events else None
    res = run_all(base_dir, sk, args.tz, args.lat, args.lon, args.start, args.end, ev,
                  make_pdf=not args.no_pdf, email_after=args.email, email_to=args.email_to,
                  email_from=args.email_from, email_subject=args.email_subject, email_body=args.email_body)
    print("\n".join(res.get("steps", [])))
    if res.get("pdf"): print(f"PDF: {res['pdf']}")
