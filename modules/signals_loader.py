from __future__ import annotations
import csv, io, math, requests
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

def _daterange(start: datetime, end: datetime):
    cur = start
    while cur <= end:
        yield cur
        cur += timedelta(hours=1)

def _load_local_events(csv_path: Path) -> pd.DataFrame:
    if not csv_path or not Path(csv_path).exists():
        return pd.DataFrame(columns=["date","start_time","end_time","event_score","notes"])
    df = pd.read_csv(csv_path)
    # Normalize to hourly scores
    rows = []
    for _, r in df.iterrows():
        try:
            d = datetime.strptime(str(r["date"]), "%Y-%m-%d")
            st = str(r.get("start_time","00:00"))
            en = str(r.get("end_time","23:59"))
            s_h, s_m = map(int, st.split(":"))
            e_h, e_m = map(int, en.split(":"))
            start_dt = d.replace(hour=s_h, minute=s_m)
            end_dt = d.replace(hour=e_h, minute=e_m)
            score = int(r.get("event_score", 0))
        except Exception:
            continue
        cur = start_dt
        while cur <= end_dt:
            rows.append({"ts": cur, "event_score": score})
            cur += timedelta(hours=1)
    return pd.DataFrame(rows)

def _traffic_index_heuristic(hour: int) -> int:
    # Simple synthetic: rush hours higher
    base = 100
    if hour in (7,8,16,17):
        base += 40
    return base

def fetch_weather_signals(lat: float, lon: float, start_date: str, end_date: str) -> pd.DataFrame:
    # Pull hourly temp (F) and precip probability from Open-Meteo
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,precipitation_probability",
        "start_date": start_date,
        "end_date": end_date,
        "timezone": "UTC"
    }
    r = requests.get(OPEN_METEO_URL, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    temps_c = hourly.get("temperature_2m", [])
    pprob = hourly.get("precipitation_probability", [])
    rows = []
    for i, t in enumerate(times):
        try:
            ts = datetime.fromisoformat(t)
        except Exception:
            continue
        temp_c = float(temps_c[i]) if i < len(temps_c) else None
        temp_f = temp_c * 9/5 + 32 if temp_c is not None else None
        precip = float(pprob[i]) / 100.0 if i < len(pprob) and pprob[i] is not None else 0.0
        rows.append({"ts": ts, "temp_f": round(temp_f,1) if temp_f is not None else None, "precip_prob": round(precip,2)})
    df = pd.DataFrame(rows)
    # Traffic index heuristic + event_score placeholder
    if not df.empty:
        df["traffic_idx"] = df["ts"].dt.hour.map(_traffic_index_heuristic).astype(int)
        df["event_score"] = 0
    return df

def build_signals_csv(lat: float, lon: float, start_date: str, end_date: str, local_events_csv: Path | None, out_csv: Path) -> Path:
    weather = fetch_weather_signals(lat, lon, start_date, end_date)
    if local_events_csv:
        le = _load_local_events(local_events_csv)
    else:
        le = pd.DataFrame(columns=["ts","event_score"])
    df = weather.copy()
    if not le.empty:
        le["ts"] = pd.to_datetime(le["ts"])
        df = df.merge(le, on="ts", how="left", suffixes=("", "_local"))
        df["event_score"] = df["event_score"].fillna(df.get("event_score_local", 0)).fillna(0).astype(int)
        if "event_score_local" in df.columns:
            df = df.drop(columns=["event_score_local"])
    # Fill missing numeric columns
    for col in ["temp_f","precip_prob","traffic_idx","event_score"]:
        if col not in df.columns:
            df[col] = 0
        df[col] = df[col].fillna(0)
    # Round and sort
    df = df.sort_values("ts")
    df.to_csv(out_csv, index=False)
    return out_csv

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Build signals_hourly.csv via Open-Meteo + local events CSV")
    p.add_argument("--lat", type=float, required=True)
    p.add_argument("--lon", type=float, required=True)
    p.add_argument("--start", required=True, help="YYYY-MM-DD")
    p.add_argument("--end", required=True, help="YYYY-MM-DD")
    p.add_argument("--events", default="", help="Optional path to local_events.csv (date,start_time,end_time,event_score)")
    p.add_argument("--out", default=str(Path(__file__).resolve().parents[1] / "data" / "signals_hourly.csv"))
    args = p.parse_args()
    events_path = Path(args.events) if args.events else None
    out = build_signals_csv(args.lat, args.lon, args.start, args.end, events_path, Path(args.out))
    print(f"Wrote {out}")
