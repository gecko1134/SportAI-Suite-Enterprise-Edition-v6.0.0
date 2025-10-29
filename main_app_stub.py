
import streamlit as st
from modules.ops import revpah_integrity

st.set_page_config(page_title="SportAI – Ops Tools", layout="wide")
st.sidebar.title("SportAI")
role = st.sidebar.selectbox("Role", ["Admin","Board","Ops","Finance","Analyst","Director","Sponsor","Member"])
category = st.sidebar.selectbox("Category", ["Ops Tools","Sponsorship Tools","Finance Tools","Membership Tools"])

st.title("SportAI – Demo Loader")
if category == "Ops Tools":
    st.subheader("RevPAH Integrity")
    revpah_integrity.run(user_role=role)
else:
    st.info("Select 'Ops Tools' to view RevPAH Integrity.")
