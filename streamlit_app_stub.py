
import streamlit as st
import pandas as pd
from revpah_loader import run_all

st.set_page_config(page_title="RevPAH Integrity", layout="wide")

st.title("RevPAH Integrity Index – Loader & What-If Stub")
data_dir = st.text_input("Data directory", "./datasets")
if st.button("Compute KPIs"):
    with st.spinner("Computing..."):
        kpi, parent, suggestions = run_all(data_dir)
    st.subheader("Asset × Hour KPIs")
    st.dataframe(kpi)
    if isinstance(parent, pd.DataFrame) and len(parent):
        st.subheader("Parent Asset Summaries")
        st.dataframe(parent)
    st.subheader("Top Suggestions")
    if suggestions:
        st.json(suggestions)
    else:
        st.info("No suggestions generated with current data.")
