
import os, io, json, zipfile, time
import pandas as pd
from datetime import datetime
import streamlit as st
from revpah_loader import run_all

EXPORT_DIR_DEFAULT = "./exports"
ROLE_CAN_PUSH = {"Admin","Ops","Director"}

def _export_frames(kpi_df: pd.DataFrame, parent_df: pd.DataFrame, suggestions: list, export_dir: str):
    os.makedirs(export_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    kpi_path = os.path.join(export_dir, f"revpah_kpi_{ts}.csv")
    parent_path = os.path.join(export_dir, f"revpah_parent_{ts}.csv")
    sugg_path = os.path.join(export_dir, f"revpah_suggestions_{ts}.json")
    kpi_df.to_csv(kpi_path, index=False)
    if isinstance(parent_df, pd.DataFrame) and len(parent_df):
        parent_df.to_csv(parent_path, index=False)
    else:
        parent_path = None
    with open(sugg_path, "w") as f:
        json.dump(suggestions, f, indent=2)
    return kpi_path, parent_path, sugg_path

def _build_zip_bundle(paths: dict) -> bytes:
    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for label, p in paths.items():
            if p and os.path.exists(p):
                z.write(p, arcname=os.path.basename(p))
    mem_zip.seek(0)
    return mem_zip.read()

def _post_webhook_with_retry(webhook_url: str, payload: dict, retries: int = 3, backoff_sec: float = 1.0, dry_run: bool = False):
    if dry_run:
        return True, f"DRY-RUN ok (payload bytes={len(json.dumps(payload))})"
    try:
        import urllib.request, urllib.error
        data = json.dumps(payload).encode("utf-8")
        last_err = None
        for attempt in range(1, retries+1):
            try:
                req = urllib.request.Request(webhook_url, data=data, headers={"Content-Type":"application/json"})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    code = resp.getcode()
                    if 200 <= code < 300:
                        return True, f"HTTP {code} on attempt {attempt}"
                    else:
                        last_err = Exception(f"HTTP {code}")
            except Exception as e:
                last_err = e
            time.sleep(backoff_sec * (2 ** (attempt-1)))
        return False, f"Failed after {retries} attempts: {last_err}"
    except Exception as e:
        return (False, str(e))

def run(user_role: str = "Admin"):
    st.header("RevPAH Integrity (Ops Tools)")
    data_dir = st.text_input("Data directory", "./datasets")
    export_dir = st.text_input("Export directory", EXPORT_DIR_DEFAULT)

    tab1, tab2 = st.tabs(["Analysis","Integrations"])

    with tab2:
        st.subheader("⚙️ Integrations")
        col_ws1, col_ws2 = st.columns([3,1])
        with col_ws1:
            webhook_url = st.text_input("SportsKey Webhook URL (POST suggestions as JSON)", value=os.environ.get("SPORTSKEY_WEBHOOK_URL",""))
        with col_ws2:
            enable_webhook = st.checkbox("Enable Webhook", value=False)
        dry_run = st.checkbox("Dry-Run Webhook (no POST)", value=True)
        if enable_webhook and user_role not in ROLE_CAN_PUSH:
            st.warning(f"Your role '{user_role}' cannot push to webhook. Allowed: {', '.join(sorted(ROLE_CAN_PUSH))}")

    with tab1:
        colA, colB, colC = st.columns(3)
        with colA:
            compute = st.button("Compute KPIs")
        with colB:
            auto_export = st.checkbox("Auto-export CSV/JSON", value=True)
        with colC:
            bundle_btn = st.button("Export Bundle (.zip)")

        if "latest_paths" not in st.session_state:
            st.session_state["latest_paths"] = {}

        if compute:
            with st.spinner("Computing RevPAH KPIs..."):
                kpi, parent, suggestions = run_all(data_dir)

            st.subheader("Asset × Hour KPIs")
            st.dataframe(kpi)
            if isinstance(parent, pd.DataFrame) and len(parent):
                st.subheader("Parent Asset Summaries")
                st.dataframe(parent)

            st.subheader("Top 10 Reallocation Suggestions")
            if suggestions:
                st.json(suggestions)
            else:
                st.info("No suggestions generated with current data.")

            latest = {}
            if auto_export:
                kpi_path, parent_path, sugg_path = _export_frames(kpi, parent, suggestions, export_dir)
                latest = {"kpi": kpi_path, "parent": parent_path, "suggestions": sugg_path}
                st.success("Exports saved.")
                st.write(f"- KPIs: `{kpi_path}`")
                if parent_path:
                    st.write(f"- Parents: `{parent_path}`")
                st.write(f"- Suggestions: `{sugg_path}`")
            st.session_state["latest_paths"] = latest

            if enable_webhook and user_role in ROLE_CAN_PUSH and webhook_url:
                payload = {"source":"SportAI.RevPAH","generated_at": datetime.utcnow().isoformat()+"Z","actions": suggestions}
                ok, msg = _post_webhook_with_retry(webhook_url, payload, retries=3, backoff_sec=1.0, dry_run=dry_run)
                if ok:
                    st.success(f"Webhook result: {msg}")
                else:
                    st.warning(f"Webhook error: {msg}")

        if bundle_btn:
            paths = st.session_state.get("latest_paths", {})
            if not paths:
                st.info("Run 'Compute KPIs' first to generate files.")
            else:
                data = _build_zip_bundle(paths)
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.download_button(label="Download RevPAH Export Bundle", data=data, file_name=f"revpah_export_{ts}.zip", mime="application/zip")

    st.caption("Weights: RevPAH 40%, Fill 30%, Gaps 20%, Labor 10%. Buffers and parent capacity respected.")
