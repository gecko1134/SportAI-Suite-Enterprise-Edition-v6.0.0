from __future__ import annotations
import os
from pathlib import Path
try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

DEFAULTS = {
    "BOARD_EMAILS": "board@nationalsportsdome.com",
    "FROM_EMAIL": "no-reply@nationalsportsdome.com",
    "DEFAULT_LAT": "46.7470",
    "DEFAULT_LON": "-92.2243",
    "DEFAULT_TIMEZONE": "America/Chicago",
    "DEFAULT_CITY": "Proctor, MN",
    "DEFAULT_ACTIVE_MODE": "Normal",
}

def get_config(base_dir: Path) -> dict:
    env_path = base_dir / ".env"
    if load_dotenv and env_path.exists():
        load_dotenv(env_path)
    cfg = {}
    for k, v in DEFAULTS.items():
        cfg[k] = os.getenv(k, v)
    # also pass through SENDGRID_API_KEY if present
    if os.getenv("SENDGRID_API_KEY"):
        cfg["HAS_SENDGRID"] = "1"
    else:
        cfg["HAS_SENDGRID"] = "0"
    return cfg
