from __future__ import annotations
import pandas as pd
from pathlib import Path
import json
from datetime import datetime, time
def _load_protected(data_dir: Path) -> pd.DataFrame:
    ph = data_dir / "protected_hours.csv"
    if ph.exists():
        return pd.read_csv(ph)
    return pd.DataFrame(columns=["zone_id","dow","start_time","end_time","applies_to","action_block"])

def _is_blocked(ts: pd.Timestamp, zone_id: str, action_type: str, protected: pd.DataFrame) -> bool:
    if protected.empty:
        return False
    dow = ts.weekday()
    tstr = ts.strftime("%H:%M")
    # match rows where zone matches or ALL, and dow matches, and time within window
    rows = protected[(protected["dow"] == dow) & (protected["zone_id"].isin([zone_id, "ALL"]))]
    for _, r in rows.iterrows():
        start = str(r.get("start_time", "00:00"))
        end = str(r.get("end_time", "23:59"))
        if start <= tstr <= end:
            blocked_actions = [a.strip() for a in str(r.get("action_block", "")).split(",") if a.strip()]
            if action_type in blocked_actions or "all" in blocked_actions:
                return True
    return False


def _load_policies(data_dir: Path) -> dict:
    pol_path = data_dir / "policies.json"
    if pol_path.exists():
        with open(pol_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def _within_any_window(ts: pd.Timestamp, windows: list[str]) -> bool:
    if not windows:
        return False
    t = ts.time()
    for w in windows:
        try:
            start_s, end_s = w.split("-")
            h1, m1 = map(int, start_s.split(":"))
            h2, m2 = map(int, end_s.split(":"))
            if time(h1, m1) <= t <= time(h2, m2):
                return True
        except Exception:
            continue
    return False

def suggest_actions(data_dir: str | Path) -> pd.DataFrame:
    data_dir = Path(data_dir)
    fc_path = data_dir / "forecast_48h.csv"
    cap_path = data_dir / "capacity.csv"
    if not fc_path.exists():
        return pd.DataFrame(columns=["ts","zone_id","action_type","before","after","rationale"])

    fc = pd.read_csv(fc_path, parse_dates=["ts"])
    cap = pd.read_csv(cap_path)
    policies = _load_policies(data_dir)
    protected = _load_protected(data_dir)

    if fc.empty:
        return pd.DataFrame(columns=["ts","zone_id","action_type","before","after","rationale"])

    fc = fc.merge(cap[["zone_id","max_slots_per_hour"]], on="zone_id", how="left")

    # Guardrails
    notice_sched_h = int(policies.get("notice_windows", {}).get("schedule_change_hours", 24))
    increase_thr = float(policies.get("staffing", {}).get("increase_threshold", 0.8))
    decrease_thr = float(policies.get("staffing", {}).get("decrease_threshold", 0.3))
    max_staff_delta = int(policies.get("staffing", {}).get("max_delta_per_hour", 1))
    max_overflow = int(policies.get("inventory", {}).get("max_overflow_slots_per_hour", 1))
    allow_split = bool(policies.get("inventory", {}).get("allow_split_layouts", True))
    max_changes_day = int(policies.get("global", {}).get("max_total_changes_per_day", 20))
    active_mode = policies.get("active_mode", "Normal")

    actions = []
    today = pd.Timestamp.now().normalize()
    now = pd.Timestamp.now()

    def add_action(row_dict):
        # Skip if protected hours block this action
        if _is_blocked(pd.to_datetime(row_dict['ts']), row_dict['zone_id'], row_dict['action_type'], protected):
            return
        # Enforce max per day
        ts = pd.to_datetime(row_dict["ts"])
        if sum(1 for a in actions if pd.to_datetime(a["ts"]).date() == ts.date()) >= max_changes_day:
            return
        actions.append(row_dict)

    for zid, g in fc.groupby("zone_id"):
        g = g.sort_values("ts")
        # Troughs for cleaning (lowest 10%)
        thresh = g["forecast"].quantile(0.10)
        troughs = g[g["forecast"] <= thresh]["ts"].tolist()

        # Suggest up to 3 cleaning windows honoring notice window
        for ts in troughs:
            if (ts - now) < pd.Timedelta(hours=notice_sched_h):
                continue
            add_action({
                "ts": ts.isoformat(),
                "zone_id": zid,
                "action_type": "cleaning_window",
                "before": "",
                "after": "Schedule cleaning",
                "rationale": f"[{active_mode}] Trough hour; >= {notice_sched_h}h notice"
            })
            if sum(1 for a in actions if a["action_type"]=="cleaning_window" and a["zone_id"]==zid) >= 3:
                break

        # Overflow inventory when near capacity
        near_cap = g[g["forecast"] >= increase_thr * g["max_slots_per_hour"].fillna(1)]
        per_hour_count = {}
        for _, r in near_cap.iterrows():
            key = (zid, r["ts"].floor("H"))
            per_hour_count[key] = per_hour_count.get(key, 0)
            if per_hour_count[key] >= max_overflow:
                continue
            per_hour_count[key] += 1
            after = "Release overflow slot"
            if allow_split:
                after += " or enable split-layout"
            add_action({
                "ts": r["ts"].isoformat(),
                "zone_id": zid,
                "action_type": "open_overflow",
                "before": "",
                "after": after,
                "rationale": f"[{active_mode}] Forecast >= {int(increase_thr*100)}% of capacity"
            })

        # Staffing deltas
        low = g[g["forecast"] < decrease_thr * g["max_slots_per_hour"].fillna(1)]
        high = near_cap

        per_hour_staff = {}
        for _, r in high.iterrows():
            key = (zid, r["ts"].floor("H"))
            per_hour_staff[key] = per_hour_staff.get(key, 0)
            if per_hour_staff[key] >= max_staff_delta:
                continue
            per_hour_staff[key] += 1
            add_action({
                "ts": r["ts"].isoformat(),
                "zone_id": zid,
                "action_type": "staff_increase",
                "before": "baseline",
                "after": "+1",
                "rationale": f"[{active_mode}] Forecast >= {int(increase_thr*100)}% of capacity"
            })
        for _, r in low.iterrows():
            key = (zid, r["ts"].floor("H"))
            per_hour_staff[key] = per_hour_staff.get(key, 0)
            if per_hour_staff[key] <= -max_staff_delta:
                continue
            per_hour_staff[key] -= 1
            add_action({
                "ts": r["ts"].isoformat(),
                "zone_id": zid,
                "action_type": "staff_reduce",
                "before": "baseline",
                "after": "-1",
                "rationale": f"[{active_mode}] Forecast < {int(decrease_thr*100)}% of capacity"
            })

    # Reorder by priority from policies
    priority = policies.get("global", {}).get("change_types_priority", [])
    if priority:
        type_index = {t:i for i,t in enumerate(priority)}
        actions.sort(key=lambda a: (pd.to_datetime(a["ts"]), type_index.get(a["action_type"], 999)))

    # Return DataFrame
    return pd.DataFrame(actions, columns=["ts","zone_id","action_type","before","after","rationale"])

if __name__ == "__main__":
    out = suggest_actions(Path(__file__).resolve().parents[1] / "data")
    out_path = Path(__file__).resolve().parents[1] / "data" / "actions_log.csv"
    out.to_csv(out_path, index=False)
    print(f"Wrote {out_path}")
