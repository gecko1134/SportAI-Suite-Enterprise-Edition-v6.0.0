import sys
from pathlib import Path
import pandas as pd

REQUIRED = {
    "events_hourly.csv": ["ts","zone_id","booked_slots","checkins","est_walkins"],
    "signals_hourly.csv": ["ts","temp_f","precip_prob","traffic_idx","event_score"],
    "capacity.csv": ["zone_id","zone_name","layout","setup_minutes","clean_minutes","max_slots_per_hour"],
    "protected_hours.csv": ["zone_id","dow","start_time","end_time","applies_to","action_block"],
}

def _fail(msg: str):
    print(f"[VALIDATION ERROR] {msg}")
    sys.exit(1)

def _warn(msg: str):
    print(f"[WARN] {msg}")

def validate_csv(path: Path, required_cols: list[str]):
    if not path.exists():
        _fail(f"Missing file: {path.name}")
    try:
        df = pd.read_csv(path)
    except Exception as e:
        _fail(f"Could not read {path.name}: {e}")
    for c in required_cols:
        if c not in df.columns:
            _fail(f"{path.name} missing required column '{c}'")
    return df

def validate_events(df: pd.DataFrame):
    if df.empty:
        _fail("events_hourly.csv is empty")
    # basic types/ranges
    if (df["booked_slots"] < 0).any():
        _fail("events_hourly.csv has negative booked_slots")
    if (df["checkins"] < 0).any():
        _fail("events_hourly.csv has negative checkins")
    if (df["est_walkins"] < 0).any():
        _fail("events_hourly.csv has negative est_walkins")
    dups = df.duplicated(subset=["ts","zone_id"]).sum()
    if dups:
        _warn(f"events_hourly.csv has {dups} duplicate (ts, zone_id) rows")

def validate_signals(df: pd.DataFrame):
    if df.empty:
        _fail("signals_hourly.csv is empty")
    if (df["precip_prob"] < 0).any() or (df["precip_prob"] > 1).any():
        _fail("signals_hourly.csv precip_prob must be in [0,1]")
    if (df["traffic_idx"] < 0).any():
        _fail("signals_hourly.csv traffic_idx must be >= 0")
    if df["ts"].isna().any():
        _fail("signals_hourly.csv has null ts")

def validate_capacity(df: pd.DataFrame):
    if df.empty:
        _fail("capacity.csv is empty")
    for c in ["setup_minutes","clean_minutes","max_slots_per_hour"]:
        if (df[c] <= 0).any():
            _fail(f"capacity.csv {c} must be > 0")
    if df["zone_id"].duplicated().any():
        _warn("capacity.csv has duplicated zone_id; ensure uniqueness")

def validate_protected(df: pd.DataFrame):
    # dow 0-6, times hh:mm
    if (~df["dow"].between(0,6)).any():
        _fail("protected_hours.csv dow must be 0-6 (Mon=0)")
    for col in ["start_time","end_time"]:
        bad = ~df[col].astype(str).str.match(r"^\d{2}:\d{2}$")
        if bad.any():
            _fail(f"protected_hours.csv bad time format in {col}; expected HH:MM")

def main(data_dir: Path):
    ev = validate_csv(data_dir / "events_hourly.csv", REQUIRED["events_hourly.csv"])
    sg = validate_csv(data_dir / "signals_hourly.csv", REQUIRED["signals_hourly.csv"])
    cp = validate_csv(data_dir / "capacity.csv", REQUIRED["capacity.csv"])
    ph = validate_csv(data_dir / "protected_hours.csv", REQUIRED["protected_hours.csv"])

    validate_events(ev)
    validate_signals(sg)
    validate_capacity(cp)
    validate_protected(ph)

    # Join sanity check: all event ts exist in signals ts
    ev_ts = set(pd.to_datetime(ev["ts"]).astype(int).tolist())
    sg_ts = set(pd.to_datetime(sg["ts"]).astype(int).tolist())
    missing_ts = len(ev_ts - sg_ts)
    if missing_ts > 0:
        _warn(f"{missing_ts} event timestamps missing from signals; forward-fill may occur")

    # Zone coverage: every zone in events appears in capacity
    missing_zones = set(ev["zone_id"].unique()) - set(cp["zone_id"].unique())
    if missing_zones:
        _fail(f"Zones missing from capacity.csv: {sorted(missing_zones)}")

    print("[OK] Data validation passed.")

if __name__ == "__main__":
    data_dir = Path(__file__).resolve().parents[1] / "data"
    main(data_dir)
