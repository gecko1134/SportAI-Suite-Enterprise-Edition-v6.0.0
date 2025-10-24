\
    @echo off
    REM Nightly scheduler for SportAI FinCast: Ops (Windows Task Scheduler)
    REM Example Task Scheduler action:
    REM   Program/script:  C:\Windows\System32\cmd.exe
    REM   Add arguments:   /c "C:\path\to\scripts\task_run_all.bat >> C:\path\to\logs\sportai_nightly.log 2>&1"

    setlocal ENABLEDELAYEDEXPANSION
    cd /d %~dp0
    cd ..

    REM Load .env (basic parser for KEY=VALUE lines)
    if exist .env (
        for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
            if not "%%A"=="" set %%A=%%B
        )
    )

    if not exist .venv (
        py -3 -m venv .venv
    )
    call .venv\Scripts\activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt

    python modules\run_all.py --email --email-to %BOARD_EMAILS%
