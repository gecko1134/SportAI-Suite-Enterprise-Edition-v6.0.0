import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

st.set_page_config(page_title="SportAI FinCast: Ops", layout="wide")
st.title("SportAI FinCast: Ops — Pilot Dashboard")

data_dir = Path(__file__).resolve().parents[1] / "data"

@st.cache_data
def load_data():
    events = pd.read_csv(data_dir / "events_hourly.csv", parse_dates=["ts"])
    signals = pd.read_csv(data_dir / "signals_hourly.csv", parse_dates=["ts"])
    capacity = pd.read_csv(data_dir / "capacity.csv")
    try:
        forecast = pd.read_csv(data_dir / "forecast_48h.csv", parse_dates=["ts"])
    except Exception:
        forecast = pd.DataFrame(columns=["ts","zone_id","forecast"])
    return events, signals, capacity, forecast

events, signals, capacity, forecast = load_data()

zones = sorted(events["zone_id"].unique().tolist())
zone = st.selectbox("Select zone", zones)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Recent Actuals (booked_slots)")
    g = events[events["zone_id"] == zone].sort_values("ts").tail(240)  # last 10 days
    fig1, ax1 = plt.subplots()
    ax1.plot(g["ts"], g["booked_slots"])
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Booked Slots")
    st.pyplot(fig1)

with col2:
    st.subheader("48h Forecast")
    if not forecast.empty:
        gf = forecast[forecast["zone_id"] == zone].sort_values("ts")
        fig2, ax2 = plt.subplots()
        ax2.plot(gf["ts"], gf["forecast"])
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Forecast Slots")
        st.pyplot(fig2)
    else:
        st.info("Run the notebook to generate forecasts.")

st.divider()
st.subheader("Modes")
mode = st.radio("Select mode", ["Normal", "Tournament Mode", "Community Night", "Storm Incoming"], horizontal=True)
if mode == "Tournament Mode":
    st.caption("Anchors major blocks; limits flex to overflow only.")
elif mode == "Community Night":
    st.caption("Tighten price bands and widen cleaning windows.")
elif mode == "Storm Incoming":
    st.caption("Expand indoor shoulder hours and enable flexible rescheduling.")
else:
    st.caption("Standard operating parameters.")

st.divider()
st.subheader("Export Suggested Actions")
if st.button("Generate Suggestions"):
    from modules.rules_engine import suggest_actions
    out = suggest_actions(data_dir)
    st.dataframe(out)
    out.to_csv(data_dir / "actions_log.csv", index=False)
    st.success("Actions written to data/actions_log.csv")

st.divider()
st.subheader("Board Export")
if st.button("Export Ops Report (PDF)"):
    from modules.ops_report_pdf import generate_pdf
    pdf_path = generate_pdf(Path(__file__).resolve().parents[1])
    st.success(f"Report created: {pdf_path.name}")
    st.caption("Find it in the docs/ folder next to the project.")

st.subheader("Email Board 1-Pager")
default_recipients = st.text_input("Recipient emails (comma-separated)", value="board@nationalsportsdome.com")
from_email = st.text_input("From email", value="no-reply@nationalsportsdome.com")
subject = st.text_input("Subject", value="SportAI Ops Report")
body = st.text_area("Message", value="Attached: latest 1-page Ops Report from SportAI FinCast.")

if st.button("Generate & Email PDF"):
    from modules.ops_report_pdf import generate_pdf
    from modules.email_sender import send_pdf_via_sendgrid
    base_dir = Path(__file__).resolve().parents[1]
    pdf_path = generate_pdf(base_dir)
    to_emails = [e.strip() for e in default_recipients.split(",") if e.strip()]
    result = send_pdf_via_sendgrid(
        to_emails=to_emails,
        subject=subject,
        body_text=body,
        pdf_path=pdf_path,
        from_email=from_email,
    )
    if result.get("ok"):
        st.success(result.get("message", "Email sent."))
        st.caption(f"File: {pdf_path.name}")
    else:
        st.error(result.get("message", "Email failed."))
        st.caption("Ensure SENDGRID_API_KEY is set in the environment on the server where Streamlit runs.")

st.divider()
st.subheader("Global Mode (writes to data/policies.json)")
import json
pol_path = Path(__file__).resolve().parents[1] / "data" / "policies.json"
try:
    current_pols = json.loads(pol_path.read_text())
except Exception:
    current_pols = {"active_mode": "Normal"}
current_mode = current_pols.get("active_mode", "Normal")
new_mode = st.radio("Select global mode", ["Normal", "Tournament", "Community"], index=["Normal","Tournament","Community"].index(current_mode), horizontal=True)

if st.button("Update Mode"):
    current_pols["active_mode"] = new_mode
    pol_path.write_text(json.dumps(current_pols, indent=2))
    st.success(f"Mode set to {new_mode}. Future suggestions will honor this.")

st.divider()
st.subheader("SportsKey CSV Import")
st.caption("Drop a SportsKey booking export to auto-build events_hourly.csv (hourly buckets).")
uploaded = st.file_uploader("Upload CSV", type=["csv"])
set_tz = st.text_input("Timezone", value="America/Chicago")
if uploaded is not None and st.button("Import CSV → events_hourly.csv"):
    import pandas as pd, io
    from modules.sportskey_importer import import_sportskey_csv
    tmp_path = Path(st.secrets.get("_tmp_dir", ".")) / "upload_sportskey.csv"
    # Save to temp and run importer
    content = uploaded.read()
    tmp_path.write_bytes(content)
    out_path = Path(__file__).resolve().parents[1] / "data" / "events_hourly.csv"
    map_json = Path(__file__).resolve().parents[1] / "data" / "mappings" / "sportskey_map.json"
    try:
        out = import_sportskey_csv(tmp_path, out_path, map_json, set_tz)
        st.success(f"Imported to {out.name}. Re-run forecast to use the new data.")
    except Exception as e:
        st.error(f"Import failed: {e}")

st.divider()
st.subheader("Signals Loader")
st.caption("Fetch hourly weather (Open-Meteo) and blend with local events to create signals_hourly.csv.")
lat = st.number_input("Latitude", value=46.7470, format="%.6f")
lon = st.number_input("Longitude", value=-92.2243, format="%.6f")
start_date = st.date_input("Start date")
end_date = st.date_input("End date")
uploaded_events = st.file_uploader("Upload local events CSV (optional)", type=["csv"], key="events_upload")
if st.button("Build signals_hourly.csv"):
    from modules.signals_loader import build_signals_csv
    events_path = None
    if uploaded_events is not None:
        tmp = Path(st.secrets.get("_tmp_dir", ".")) / "local_events.csv"
        tmp.write_bytes(uploaded_events.read())
        events_path = tmp
    out_path = Path(__file__).resolve().parents[1] / "data" / "signals_hourly.csv"
    try:
        out = build_signals_csv(float(lat), float(lon), start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), events_path, out_path)
        st.success(f"Signals written to {out.name}.")
    except Exception as e:
        st.error(f"Signals build failed: {e}")
        st.caption("Ensure internet access on the server to call Open-Meteo, and valid date range.")

st.divider()
st.subheader("Run All (One Click)")
st.caption("Validate → (optional) import SportsKey → (optional) build signals → forecast → suggestions → PDF.")
upload_sk = st.file_uploader("Optional: SportsKey CSV", type=["csv"], key="runall_sk")
tz_runall = st.text_input("Timezone for SportsKey", value="America/Chicago", key="runall_tz")
lat_runall = st.number_input("Latitude (optional for signals)", value=46.7470, format="%.6f", key="runall_lat")
lon_runall = st.number_input("Longitude (optional for signals)", value=-92.2243, format="%.6f", key="runall_lon")
start_runall = st.date_input("Signals start (optional)", key="runall_start")
end_runall = st.date_input("Signals end (optional)", key="runall_end")
events_upload_runall = st.file_uploader("Optional: Local events CSV", type=["csv"], key="runall_events")
make_pdf = st.checkbox("Create Ops Report PDF", value=True)

if st.button("Run All Now"):
    from modules.run_all import run_all as run_all_fn
    base_dir = Path(__file__).resolve().parents[1]
    sk_path = None
    if upload_sk is not None:
        tmp_sk = Path(st.secrets.get("_tmp_dir", ".")) / "runall_sportskey.csv"
        tmp_sk.write_bytes(upload_sk.read())
        sk_path = tmp_sk
    ev_path = None
    if events_upload_runall is not None:
        tmp_ev = Path(st.secrets.get("_tmp_dir", ".")) / "runall_events.csv"
        tmp_ev.write_bytes(events_upload_runall.read())
        ev_path = tmp_ev

    # Decide whether to run signals
    latv, lonv = None, None
    sv, ev = None, None
    if start_runall and end_runall:
        sv = start_runall.strftime("%Y-%m-%d")
        ev = end_runall.strftime("%Y-%m-%d")
        latv, lonv = float(lat_runall), float(lon_runall)

    try:
        res = run_all_fn(base_dir, sk_path, tz_runall, latv, lonv, sv, ev, ev_path, make_pdf=make_pdf)
        st.success("Completed pipeline.")
        for s in res.get("steps", []):
            st.write("• " + s)
        if res.get("pdf"):
            st.caption(f"PDF saved: {Path(res['pdf']).name} (see docs/)")
    except Exception as e:
        st.error(f"Run All failed: {e}")
