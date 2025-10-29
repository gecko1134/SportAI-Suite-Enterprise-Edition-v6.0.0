
# RevPAH Integrity Loader (Option B layout)

This bundle ingests CSVs from `./datasets/` and computes:
- Fill %, Avg Rate, RevPAH
- Gap Minutes (buffer-aware)
- Labor $/hr
- **Integrity Index (0–100)**
- **Top 10 Reallocation Suggestions** (5–10 min nudges)

## Folder Layout
```
NXS_RevPAH_Integrity_Loader/
  revpah_loader.py
  streamlit_app_stub.py
  datasets/
    Bookings.csv
    Ops.csv
    Calendars.csv
    Membership.csv
  schemas/
    bookings.schema.json
    ops.schema.json
    calendars.schema.json
    membership.schema.json
```

## Quick Start (CLI)
```bash
cd NXS_RevPAH_Integrity_Loader
python3 revpah_loader.py
```

## Quick Start (Streamlit)
```bash
cd NXS_RevPAH_Integrity_Loader
streamlit run streamlit_app_stub.py
```
Set `Data directory` to `./datasets` (default).

## CSV Schemas (Draft)
See files under `schemas/`. These follow JSON Schema draft 2020-12 for basic validation.

## Integration Notes
- **Parent capacity** is honored in parent summaries (e.g., `FullTurf-1` with 2 half units).
- **Credit value mapping** is inferred from `Membership.csv` (`tier` → `credit_value_usd`).
- **Buffers**: `Ops.csv.buffer_min` subtracted when computing gap minutes.
- **Labor drag**: approximated as `labor_cost_per_hour × booked_hours` for each asset-hour.
- **Integrity Index** weights: RevPAH 40%, Fill 30%, Gap 20% (lower=better), Labor 10% (lower=better).

Tune these in `revpah_loader.py` if desired.
