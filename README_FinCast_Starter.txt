
SportAI FinCast — Digital Twin Starter (Individual Files)
=========================================================

Files:
- fincast_config.json — global drivers and defaults
- fincast_sample_data.xlsx — inputs across tabs (Drivers, Rates, CapEx, Debt, OpEx, Events, Sponsorship, Grants, Scenarios, Outputs)
- fincast_streamlit_dashboard.py — Streamlit board dashboard stub
- fincast_board_brief_template.md — board-ready summary (print to PDF)
- fincast_board_brief_template.xlsx — same brief in spreadsheet form

How to use:
1) Streamlit
   - `pip install streamlit pandas numpy`
   - Place all files in the same folder.
   - Run: `streamlit run fincast_streamlit_dashboard.py`
   - Adjust sliders and review KPIs. Replace stub math with your deeper model when ready.

2) Excel / Google Sheets
   - Open `fincast_sample_data.xlsx` and customize Drivers, Rates, etc.
   - Open `fincast_board_brief_template.xlsx` and link cells to your calc sheet to auto-populate KPIs.
   - To use Google Sheets: Upload both .xlsx files to Drive and convert to Sheets format.

Notes:
- Defaults reflect the NXS complex: 1.5 turf units, 4 courts, peak/non-peak pricing, sponsorship pipeline.
- Debt logic includes 12 months interest-only, then amortization.
- Seasonality indices are placeholders—replace with your empirical patterns.
- DSCR is shown as EBITDA / Debt Service; adapt if you prefer NOI-based covenant tracking.

