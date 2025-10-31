import pandas as pd, numpy as np
from pathlib import Path
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error
import argparse

def main(data_dir: Path):
    events = pd.read_csv(data_dir / "events_hourly.csv", parse_dates=["ts"])
    signals = pd.read_csv(data_dir / "signals_hourly.csv", parse_dates=["ts"])
    df = events.merge(signals, on="ts", how="left")
    df["hour"] = df["ts"].dt.hour
    df["dow"] = df["ts"].dt.weekday
    df["is_weekend"] = df["dow"].isin([5,6]).astype(int)
    df["day"] = df["ts"].dt.day
    df = df.sort_values(["zone_id","ts"])

    def add_lags(g):
        for L in [1, 2, 24]:
            g[f"lag_{L}"] = g["booked_slots"].shift(L)
        g["rolling_24"] = g["booked_slots"].rolling(24, min_periods=1).mean()
        return g

    df = df.groupby("zone_id", group_keys=False).apply(add_lags)
    df = df.fillna(0.0)

    split_ts = df["ts"].max() - pd.Timedelta(hours=72)
    train = df[df["ts"] <= split_ts]
    valid = df[df["ts"] > split_ts]

    features = ["hour","dow","is_weekend","temp_f","precip_prob","traffic_idx","event_score",
                "lag_1","lag_2","lag_24","rolling_24"]
    target = "booked_slots"

    forecasts = []
    metrics = []
    for zid, g in df.groupby("zone_id"):
        tr = train[train["zone_id"]==zid]
        va = valid[valid["zone_id"]==zid]
        if len(tr) < 48:
            continue
        Xtr, ytr = tr[features], tr[target]
        Xva, yva = va[features], va[target]
        model = GradientBoostingRegressor(random_state=42)
        model.fit(Xtr, ytr)
        pred = model.predict(Xva)
        mae = mean_absolute_error(yva, pred)
        metrics.append({"zone_id": zid, "val_mae": mae})

        last_ts = df["ts"].max()
        horizon_hours = 48
        for h in range(1, horizon_hours+1):
            ts = last_ts + pd.Timedelta(hours=h)
            base_row = df[df["zone_id"]==zid].iloc[-1:].copy()
            base_row["ts"] = ts
            base_row["hour"] = ts.hour
            base_row["dow"] = ts.weekday()
            base_row["is_weekend"] = int(ts.weekday() in [5,6])
            for col in ["temp_f","precip_prob","traffic_idx","event_score","rolling_24","lag_1","lag_2","lag_24"]:
                if col not in base_row.columns: base_row[col] = 0.0
                base_row[col] = float(base_row[col])
            X = base_row[features]
            yhat = float(model.predict(X)[0])
            forecasts.append({"ts": ts, "zone_id": zid, "forecast": max(0.0, yhat)})

    fc_df = pd.DataFrame(forecasts)
    fc_df.to_csv(data_dir / "forecast_48h.csv", index=False)

    if not fc_df.empty:
        fc_df["date"] = pd.to_datetime(fc_df["ts"]).dt.date
        daily = fc_df.groupby(["zone_id","date"])["forecast"].sum().reset_index()
        expanded = []
        today = pd.to_datetime(df["ts"].max()).normalize()
        for zid, g in daily.groupby("zone_id"):
            avg_day = g["forecast"].mean()
            for d in range(1, 42+1):
                expanded.append({"date": (today + pd.Timedelta(days=d)).date(),
                                 "zone_id": zid,
                                 "forecast_daily": float(avg_day)})
        daily6 = pd.DataFrame(expanded)
        daily6.to_csv(data_dir / "forecast_6weeks_daily.csv", index=False)

    pd.DataFrame(metrics).to_csv(data_dir / "forecast_metrics.csv", index=False)
    print("Forecasts generated.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", default=str(Path(__file__).resolve().parents[1] / "data"))
    args = parser.parse_args()
    main(Path(args.data_dir))
