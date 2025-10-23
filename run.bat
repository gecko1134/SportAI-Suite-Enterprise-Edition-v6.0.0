\
    @echo off
    setlocal
    cd /d %~dp0

    if not exist .venv (
        py -3 -m venv .venv
    )

    call .venv\Scripts\activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt

    REM 0) Validate data
    python modules\validate_data.py

    REM 1) Generate forecasts
    python modules\generate_forecast.py

    REM 2) Launch Streamlit dashboard
    streamlit run dashboard/app.py
