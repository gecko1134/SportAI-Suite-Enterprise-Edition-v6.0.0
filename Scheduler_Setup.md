# Nightly Scheduler Setup

## Linux/macOS (cron)
1. Edit `.env` and set `BOARD_EMAILS`, `SENDGRID_API_KEY`, and defaults.
2. Make the script executable:
   ```bash
   chmod +x scripts/cron_run_all.sh
   ```
3. Open your crontab:
   ```bash
   crontab -e
   ```
4. Add a nightly entry (10:15pm local time):
   ```
   15 22 * * * /absolute/path/to/cron_run_all.sh >> /absolute/path/to/cron_run_all.log 2>&1
   ```
5. Check `cron_run_all.log` for output.

## Windows (Task Scheduler)
1. Open Task Scheduler → Create Task.
2. Triggers → New… → Daily at your chosen time.
3. Actions → New…
   - Program/script: `C:\Windows\System32\cmd.exe`
   - Add arguments: `/c "C:\path\to\scripts\task_run_all.bat >> C:\path\to\logs\sportai_nightly.log 2>&1"`
   - Start in: `C:\path\to\project\root`
4. Ensure `.env` contains `BOARD_EMAILS` and `SENDGRID_API_KEY`.
5. Run task once manually to confirm email is sent.

## Notes
- Both scripts will create a virtual environment `.venv` if missing and install dependencies from `requirements.txt`.
- The run pipeline uses the `.env` values for recipients and SendGrid key.
- To disable email, remove `--email` or unset `BOARD_EMAILS`.
