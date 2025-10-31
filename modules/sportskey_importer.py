from __future__ import annotations
import pandas as pd
from pathlib import Path
from typing import Optional, List
import json
from datetime import timedelta
import pytz

def _pick_column(df: pd.DataFrame, candidates: List[str]) -> Optional[str]:
    low_cols = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand in df.columns: return cand
        if cand.lower() in low_cols: return low_cols[cand.lower()]
    # fuzzy: strip spaces and lower
    norm = {c.lower().replace(" ", ""): c for c in df.columns}
    for cand in candidates:
        key = cand.lower().replace(" ", "")
        if key in norm: return norm[key]
    return None

def _normalize_zone(z: str, cfg: dict) -> str:
    if z is None: return "UNKNOWN"
    s = str(z).strip()
    if cfg.get("zone_normalize", {}).get("upper", False):
        s = s.upper()
    if cfg.get("zone_normalize", {}).get("spaces_to_underscore", False):
        s = s.replace(" ", "_")
    return s

def _ensure_tz(dt_series: pd.Series, tzname: str) -> pd.Series:
    tz = pytz.timezone(tzname)
    s = pd.to_datetime(dt_series, errors="coerce", infer_datetime_format=True)
    # If tz-aware, convert; else localize to tz
    if s.dt.tz is None:
        s = s.dt.tz_localize(tz, nonexistent="NaT", ambiguous="NaT")
    else:
        s = s.dt.tz_convert(tz)
    return s

def import_sportskey_csv(in_csv: Path, out_csv: Path, mapping_json: Path | None = None, tzname: str | None = None) -> Path:
    cfg = {}
    if mapping_json and Path(mapping_json).exists():
        cfg = json.loads(Path(mapping_json).read_text())
    else:
        # try default next to out_csv
        default_map = out_csv.parents[1] / "data" / "mappings" / "sportskey_map.json"
        if default_map.exists():
            cfg = json.loads(default_map.read_text())

    tzname = tzname or cfg.get("timezone_default", "America/Chicago")

    raw = pd.read_csv(in_csv)
    ts_col = _pick_column(raw, cfg.get("timestamp_candidates", [])) or "Start"
    end_col = _pick_column(raw, cfg.get("endtime_candidates", []))
    zone_col = _pick_column(raw, cfg.get("zone_candidates", [])) or "Resource"
    dur_col = _pick_column(raw, cfg.get("duration_minutes_candidates", []))
    chk_col = _pick_column(raw, cfg.get("checkins_candidates", []))

    if ts_col not in raw.columns or zone_col not in raw.columns:
        raise ValueError(f"Could not locate timestamp/zone columns in {in_csv.name}. Found ts={ts_col}, zone={zone_col}.")

    # Timezone normalize
    starts = _ensure_tz(raw[ts_col], tzname)
    if end_col and end_col in raw.columns:
        ends = _ensure_tz(raw[end_col], tzname)
    elif dur_col and dur_col in raw.columns:
        ends = starts + pd.to_timedelta(raw[dur_col], unit="m")
    else:
        # assume 60 minutes if no end/duration
        ends = starts + pd.to_timedelta(60, unit="m")

    # Normalize zone_id
    zone_ids = raw[zone_col].astype(str).map(lambda z: _normalize_zone(z, cfg))

    # Row → hourly expansion
    rows = []
    booked_default = int(cfg.get("booked_slots_per_row_default", 1))
    est_walkins_default = int(cfg.get("est_walkins_default", 0))

    for i in range(len(raw)):
        st = starts.iloc[i]
        en = ends.iloc[i]
        zid = zone_ids.iloc[i]
        if pd.isna(st) or pd.isna(en) or st >= en:
            continue
        # iterate hourly buckets
        cur = st.floor("H")
        while cur < en:
            rows.append({
                "ts": cur.tz_convert("UTC").tz_localize(None) if cur.tzinfo else cur,  # store naive UTC-like
                "zone_id": zid,
                "booked_slots": booked_default,
                "checkins": int(raw.iloc[i][chk_col]) if chk_col and not pd.isna(raw.iloc[i][chk_col]) else 0,
                "est_walkins": est_walkins_default,
            })
            cur = cur + pd.Timedelta(hours=1)

    if not rows:
        raise ValueError("No usable rows were parsed from the CSV. Check mappings and time columns.")

    df = pd.DataFrame(rows)
    # Aggregate by hour/zone
    df = df.groupby(["ts","zone_id"], as_index=False).sum(numeric_only=True)
    df["ts"] = pd.to_datetime(df["ts"]).dt.floor("H")
    # Ensure required columns
    for c in ["booked_slots","checkins","est_walkins"]:
        if c not in df.columns:
            df[c] = 0

    df.to_csv(out_csv, index=False)
    return out_csv

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Import SportsKey CSV to events_hourly.csv")
    p.add_argument("--in", dest="in_csv", required=True, help="Path to SportsKey export CSV")
    p.add_argument("--out", dest="out_csv", default=str(Path(__file__).resolve().parents[1] / "data" / "events_hourly.csv"))
    p.add_argument("--map", dest="map_json", default=str(Path(__file__).resolve().parents[1] / "data" / "mappings" / "sportskey_map.json"))
    p.add_argument("--tz", dest="tzname", default=None, help="Timezone name, e.g., America/Chicago")
    args = p.parse_args()
    out = import_sportskey_csv(Path(args.in_csv), Path(args.out_csv), Path(args.map_json), args.tzname)
    print(f"Wrote {out}")
