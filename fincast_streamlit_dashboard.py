
import json
import pandas as pd
import numpy as np
import math
import streamlit as st

st.set_page_config(page_title="SportAI FinCast — Digital Twin", layout="wide")

st.title("SportAI FinCast — Digital Twin (Starter)")

config_path = st.text_input("Config JSON path", "fincast_config.json")
data_path = st.text_input("Sample Data (xlsx) path", "fincast_sample_data.xlsx")

@st.cache_data
def load_config(path):
    with open(path, "r") as f:
        return json.load(f)

@st.cache_data
def load_data(path):
    xls = pd.ExcelFile(path)
    dfs = {}
    for name in xls.sheet_names:
        dfs[name] = pd.read_excel(path, sheet_name=name)
    return dfs

try:
    cfg = load_config(config_path)
    dfs = load_data(data_path)
    st.success("Config and data loaded.")
except Exception as e:
    st.error(f"Failed to load files: {e}")
    st.stop()

# Controls
st.sidebar.header("Board Controls")
prime_util = st.sidebar.slider("Prime Utilization Δ", -0.2, 0.2, 0.0, 0.01)
nonprime_util = st.sidebar.slider("Non-Prime Utilization Δ", -0.2, 0.2, 0.0, 0.01)
price_bump = st.sidebar.slider("Pricing Δ", -0.2, 0.2, 0.0, 0.01)
sponsor_delta = st.sidebar.slider("Sponsorship Close Rate Δ", -0.2, 0.2, 0.0, 0.01)
debt_rate_delta = st.sidebar.slider("Debt Rate Δ (bps)", -300, 300, 0, 25)

# Basic quick calc (illustrative, replace with full model as needed)
util = cfg["modules"]["utilization"]
price = cfg["modules"]["pricing"]
debt = cfg["modules"]["debt"]
opex = cfg["modules"]["opex"]
sponsor = cfg["modules"]["sponsorship"]

prime_hours = (util["prime_hours_per_day"] * util["days_per_month"])
nonprime_hours = (util["nonprime_hours_per_day"] * util["days_per_month"])

months = len(dfs["Drivers"])

# Adjusted utilization/pricing
prime_util_adj = max(0.0, min(1.0, util["prime_utilization_pct"] + prime_util))
nonprime_util_adj = max(0.0, min(1.0, util["nonprime_utilization_pct"] + nonprime_util))
court_prime_rate = price["court_prime_rate_per_hr"] * (1 + price_bump)
court_nonprime_rate = price["court_nonprime_rate_per_hr"] * (1 + price_bump)
turf_full_prime_rate = price["turf_full_prime_rate_per_hr"] * (1 + price_bump)
turf_full_nonprime_rate = price["turf_full_nonprime_rate_per_hr"] * (1 + price_bump)

# Revenue from courts
court_units = util["court_units"]
court_rev_mo = (
    court_units * (prime_hours * prime_util_adj) * court_prime_rate +
    court_units * (nonprime_hours * nonprime_util_adj) * court_nonprime_rate
)

# Revenue from turf (assume full-field rentals equivalent, conservative)
turf_units = util["turf_units"]
turf_rev_mo = (
    turf_units * (prime_hours * prime_util_adj) * turf_full_prime_rate +
    turf_units * (nonprime_hours * nonprime_util_adj) * turf_full_nonprime_rate
)

# Sponsorship (probability-weighted close rate)
pipeline_close = max(0.0, min(1.0, sponsor["pipeline_close_rate"] + sponsor_delta))
sponsor_rev_mo = sponsor["inventory_value_monthly_base"] * pipeline_close

total_rev_mo = court_rev_mo + turf_rev_mo + sponsor_rev_mo

# Opex
fixed_opex = opex["fixed_monthly"]
var_opex = total_rev_mo * opex["variable_pct_of_revenue"]
total_opex_mo = fixed_opex + var_opex

# Debt Service (approx; interest-only period then amortizing)
rate = (debt["interest_rate_annual_pct"]/100.0) + (debt_rate_delta/10000.0)
loan = debt["loan_amount"]
io_months = debt["interest_only_months"]
amort_months = debt["amort_years"]*12

interest_only_pmt = (loan * rate) / 12.0
# Level payment after IO (standard mortgage formula)
r = rate/12.0
amort_payment = loan * (r * (1 + r)**amort_months) / ((1 + r)**amort_months - 1)

# Average monthly debt payment across 36-month horizon
months_horizon = min(months, io_months + amort_months)
ds_payments = []
for m in range(months):
    if m < io_months:
        ds_payments.append(interest_only_pmt)
    else:
        ds_payments.append(amort_payment)
avg_debt_service = np.mean(ds_payments[:months])

ebitda_mo = total_rev_mo - total_opex_mo
dscr = (ebitda_mo) / avg_debt_service if avg_debt_service > 0 else np.nan

col1, col2, col3, col4 = st.columns(4)
col1.metric("Monthly Revenue (est.)", f"${total_rev_mo:,.0f}")
col2.metric("Monthly OpEx (est.)", f"${total_opex_mo:,.0f}")
col3.metric("EBITDA / mo (est.)", f"${ebitda_mo:,.0f}")
col4.metric("DSCR (est.)", f"{dscr:.2f}", help="EBITDA / Debt Service")

st.divider()
st.caption("This is a starter model. Replace/extend with your detailed calculations, seasonality curves, events, memberships, and grants draws.")

# Table preview
preview = pd.DataFrame({
    "Metric": ["Courts Rev/mo","Turf Rev/mo","Sponsorship/mo","Total Rev/mo","Fixed OpEx/mo","Var OpEx/mo","Total OpEx/mo","Avg Debt Service/mo","EBITDA/mo","DSCR"],
    "Value": [court_rev_mo, turf_rev_mo, sponsor_rev_mo, total_rev_mo, fixed_opex, var_opex, total_opex_mo, avg_debt_service, ebitda_mo, dscr]
})
st.dataframe(preview)
