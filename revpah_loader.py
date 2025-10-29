
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def load_data(data_dir: str):
    bookings = pd.read_csv(f"{data_dir}/Bookings.csv", parse_dates=["start","end"])
    ops = pd.read_csv(f"{data_dir}/Ops.csv")
    calendars = pd.read_csv(f"{data_dir}/Calendars.csv", parse_dates=["date"])
    membership = pd.read_csv(f"{data_dir}/Membership.csv")
    return bookings, ops, calendars, membership

def _usd_from_cash_and_credits(row, credit_value_lookup):
    credit_val = credit_value_lookup.get(row.get("member_tier",""), 1.0)
    return float(row.get("price_cash", 0.0)) + float(row.get("price_credits", 0.0)) * credit_val

def _hour_floor(ts):
    return ts.replace(minute=0, second=0, microsecond=0)

def compute_kpis(bookings, ops, credit_value_by_tier=None):
    bookings = bookings.copy()
    ops = ops.copy()
    if credit_value_by_tier is None:
        credit_value_by_tier = {"Standard":1.0, "Plus":1.0, "Elite":1.2}

    bookings = bookings[bookings["status"]=="booked"].copy()
    bookings["hour"] = bookings["start"].apply(_hour_floor)
    bookings["duration_hr"] = (bookings["end"] - bookings["start"]).dt.total_seconds() / 3600.0
    bookings["revenue_usd"] = bookings.apply(lambda r: _usd_from_cash_and_credits(r, credit_value_by_tier), axis=1)

    asset_capacity = ops.set_index("asset")["capacity_units"].to_dict()
    buffer_min = ops.set_index("asset")["buffer_min"].to_dict()
    labor_cost = ops.set_index("asset")["labor_cost_per_hour"].to_dict()

    rows = []
    for _, r in bookings.iterrows():
        cur = r["start"]
        while cur < r["end"]:
            hour_start = _hour_floor(cur)
            hour_end = hour_start + timedelta(hours=1)
            slice_start = max(cur, hour_start)
            slice_end = min(r["end"], hour_end)
            slice_hours = (slice_end - slice_start).total_seconds()/3600.0
            if slice_hours > 0:
                rows.append({
                    "asset": r["asset"],
                    "asset_parent": r.get("asset_parent", np.nan),
                    "hour": hour_start,
                    "slice_hours": slice_hours,
                    "slice_rev": r["revenue_usd"] * (slice_hours / r["duration_hr"] if r["duration_hr"] else 0.0)
                })
            cur = hour_end
    hour_df = pd.DataFrame(rows) if rows else pd.DataFrame(columns=["asset","hour","slice_hours","slice_rev","asset_parent"])

    kpi = hour_df.groupby(["asset","hour"], as_index=False).agg(
        booked_hours=("slice_hours","sum"),
        revenue_usd=("slice_rev","sum")
    )
    kpi["available_hours"] = 1.0
    kpi["capacity_units"] = 1
    kpi["fill_pct"] = (kpi["booked_hours"] / kpi["available_hours"]) * 100.0
    kpi["avg_rate"] = kpi.apply(lambda r: r["revenue_usd"] / r["booked_hours"] if r["booked_hours"]>0 else 0.0, axis=1)
    kpi["revpah"] = kpi["revenue_usd"] / kpi["available_hours"]
    kpi["buffer_min"] = 10
    kpi["gap_min"] = np.clip((1.0 - kpi["booked_hours"]) * 60.0 - kpi["buffer_min"], a_min=0.0, a_max=None)
    kpi["labor_cost_hr"] = 0.0

    def _norm(series):
        if series.max() - series.min() < 1e-9:
            return pd.Series(0.5, index=series.index)
        return (series - series.min())/(series.max()-series.min())

    kpi["revpah_norm"] = kpi.groupby("asset")["revpah"].transform(_norm)
    kpi["fill_norm"] = kpi.groupby("asset")["fill_pct"].transform(_norm)
    kpi["gap_norm"] = 1.0 - kpi.groupby("asset")["gap_min"].transform(_norm)
    kpi["labor_norm"] = 1.0 - kpi.groupby("asset")["labor_cost_hr"].transform(_norm)

    kpi["integrity_index"] = (
        0.40*kpi["revpah_norm"]*100
        + 0.30*kpi["fill_norm"]*100
        + 0.20*kpi["gap_norm"]*100
        + 0.10*kpi["labor_norm"]*100
    ).round(1)

    parent_rows = []
    return kpi.sort_values(["asset","hour"]), parent_rows

def suggest_reallocations(kpi_df, ops=None, max_suggestions=10):
    suggestions = []
    if kpi_df.empty: return suggestions
    tmp = kpi_df.copy()
    tmp["hour_next"] = tmp["hour"] + pd.Timedelta(hours=1)
    merged = tmp.merge(tmp[["asset","hour","integrity_index","revpah"]], left_on=["asset","hour_next"], right_on=["asset","hour"], suffixes=("","_next"))
    merged["delta"] = merged["integrity_index_next"] - merged["integrity_index"]
    cand = merged.sort_values("delta", ascending=False).head(50)
    for _, r in cand.iterrows():
        if len(suggestions) >= max_suggestions:
            break
        if r["delta"] > 8:
            suggestions.append({
                "asset": r["asset"],
                "from_hour": r["hour"].isoformat(),
                "to_hour": r["hour_next"].isoformat(),
                "reason": f"Integrity +{r['delta']:.1f}. Nudge bookings by 5–10 mins to tighten buffers and lift RevPAH.",
            })
    return suggestions

def run_all(data_dir: str):
    bookings, ops, calendars, membership = load_data(data_dir)
    tier_vals = dict(zip(membership["tier"], membership["credit_value_usd"]))
    kpi, parent = compute_kpis(bookings, ops, credit_value_by_tier=tier_vals)
    suggestions = suggest_reallocations(kpi, ops, max_suggestions=10)
    return kpi, parent, suggestions
