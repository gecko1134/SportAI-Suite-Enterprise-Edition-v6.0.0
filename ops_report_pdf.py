from __future__ import annotations
import pandas as pd
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def _save_chart(df, x, y, outpath: Path, xlabel: str, ylabel: str, title: str):
    fig, ax = plt.subplots()
    ax.plot(df[x], df[y])
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    fig.savefig(outpath, bbox_inches="tight")
    plt.close(fig)

def generate_pdf(base_dir: Path) -> Path:
    data_dir = base_dir / "data"
    docs_dir = base_dir / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)

    events = pd.read_csv(data_dir / "events_hourly.csv", parse_dates=["ts"])
    capacity = pd.read_csv(data_dir / "capacity.csv")
    forecast = None
    fc_path = data_dir / "forecast_48h.csv"
    if fc_path.exists():
        forecast = pd.read_csv(fc_path, parse_dates=["ts"])
    actions = None
    act_path = data_dir / "actions_log.csv"
    if act_path.exists():
        actions = pd.read_csv(act_path, parse_dates=["ts"])

    # Pick a primary zone for charts (first by alpha)
    zones = sorted(events["zone_id"].unique().tolist())
    zone = zones[0] if zones else None

    # Compute simple KPIs
    kpis = {}
    if zone:
        evz = events[events["zone_id"] == zone].copy().sort_values("ts").tail(168)  # last 7 days
        max_slots = capacity.set_index("zone_id").loc[zone, "max_slots_per_hour"]
        if len(evz):
            util = (evz["booked_slots"].sum() / (len(evz) * max_slots)) if max_slots else 0
            kpis["7d_utilization_zone"] = f"{util*100:.1f}%"
            kpis["zone"] = zone

    total_actions = len(actions) if actions is not None else 0
    kpis["suggested_actions_48h"] = str(total_actions)

    # Save charts as PNG
    chart1 = docs_dir / "chart_actuals.png"
    chart2 = docs_dir / "chart_forecast.png"
    if zone:
        evz = events[events["zone_id"] == zone].copy().sort_values("ts").tail(168)
        if len(evz):
            _save_chart(evz, "ts", "booked_slots", chart1, "Time", "Booked Slots", f"Actuals — {zone}")
    if forecast is not None and zone:
        fcz = forecast[forecast["zone_id"] == zone].copy().sort_values("ts")
        if len(fcz):
            _save_chart(fcz, "ts", "forecast", chart2, "Time", "Forecast", f"48h Forecast — {zone}")

    # Build PDF
    ts_label = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    out_pdf = docs_dir / f"Ops_Report_{datetime.utcnow().strftime('%Y%m%d_%H%M')}.pdf"
    c = canvas.Canvas(str(out_pdf), pagesize=letter)
    width, height = letter

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, height-1*inch, "SportAI FinCast: Ops — 1-Page Report")
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, height-1.2*inch, f"Generated: {ts_label}")

    # KPIs
    y = height - 1.6*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y, "Key KPIs")
    y -= 0.2*inch
    c.setFont("Helvetica", 10)
    for k,v in kpis.items():
        c.drawString(1.1*inch, y, f"- {k.replace('_',' ').title()}: {v}")
        y -= 0.18*inch

    # Charts
    y -= 0.1*inch
    if chart1.exists():
        c.drawImage(str(chart1), 1*inch, y-2.6*inch, width=3.8*inch, height=2.6*inch, preserveAspectRatio=True, mask='auto')
    if chart2.exists():
        c.drawImage(str(chart2), 4.2*inch, y-2.6*inch, width=3.8*inch, height=2.6*inch, preserveAspectRatio=True, mask='auto')
    y -= 2.9*inch

    # Actions table (top 10 upcoming)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y, "Upcoming Suggested Actions")
    y -= 0.2*inch
    c.setFont("Helvetica", 9)
    if actions is not None and len(actions):
        act = actions.copy().sort_values("ts").head(10)
        for _, r in act.iterrows():
            line = f"{pd.to_datetime(r['ts']).strftime('%m-%d %H:%M')}  |  {r['zone_id']}  |  {r['action_type']}  →  {r['after']}"
            if y < 1*inch:
                c.showPage(); y = height - 1*inch; c.setFont("Helvetica", 9)
            c.drawString(1.05*inch, y, line[:110])
            y -= 0.18*inch
    else:
        c.drawString(1.05*inch, y, "No actions available. Generate suggestions in the dashboard.")

    c.showPage()
    c.save()
    return out_pdf
