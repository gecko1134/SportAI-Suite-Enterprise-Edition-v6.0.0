
# === BEGIN: Forecast Accuracy — Sport Mode wiring ============================
# Place this near your other tab/module registrations in main_app.py

# 1) Import the dashboard tab's run() entrypoint
try:
    from forecast_accuracy_dashboard import run as forecast_accuracy_run
except ImportError:
    # If you placed files under modules/ai/, use a dynamic import helper or fix PYTHONPATH:
    # from modules.ai.forecast_accuracy_dashboard import run as forecast_accuracy_run
    import importlib.util, sys, os
    _p = os.path.join(os.path.dirname(__file__), "modules", "ai", "forecast_accuracy_dashboard.py")
    spec = importlib.util.spec_from_file_location("forecast_accuracy_dashboard", _p)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["forecast_accuracy_dashboard"] = mod
    spec.loader.exec_module(mod)  # type: ignore
    forecast_accuracy_run = mod.run

# 2) Define default roles and category
FORECAST_ACCURACY_TOOL = {
    "name": "Forecast Accuracy — Sport Mode",
    "id": "forecast_accuracy_sport_mode",
    "category": "Finance Tools",  # You can also place under "Ops Tools"
    "roles": ["Admin","Board","Analyst"],  # grant additional roles as needed
    "run": lambda: forecast_accuracy_run(),
    # Optional: provide a help tooltip for your UI
    "help": "Gamified accuracy: MAPE, Bias, Hit Rate, WAPE by daypart, Surprise Index, Revenue Accuracy, streaks & alerts."
}

# 3A) If you use a TOOLS list:
try:
    TOOLS.append(FORECAST_ACCURACY_TOOL)
except NameError:
    # 3B) Or if you use a MODULES dict keyed by name:
    try:
        MODULES["Forecast Accuracy — Sport Mode"] = {
            "path": "modules/ai/forecast_accuracy_dashboard.py",   # update if placed elsewhere
            "category": FORECAST_ACCURACY_TOOL["category"],
            "roles": FORECAST_ACCURACY_TOOL["roles"],
            "run": FORECAST_ACCURACY_TOOL["run"]
        }
    except NameError:
        # 3C) Or a generic registry function
        try:
            register_tool(FORECAST_ACCURACY_TOOL)
        except Exception:
            # As a last resort, define TOOLS and append
            TOOLS = [FORECAST_ACCURACY_TOOL]

# 4) Role-based gate (if your app uses a filter function)
def _user_can_access_forecast_accuracy(current_user_role: str) -> bool:
    return current_user_role in FORECAST_ACCURACY_TOOL["roles"]

# 5) Optional: sidebar quick link (example)
try:
    add_sidebar_link(
        label="Forecast Accuracy — Sport Mode",
        tool_id="forecast_accuracy_sport_mode",
        icon="📈",
        visible_if=lambda role: _user_can_access_forecast_accuracy(role)
    )
except Exception:
    pass
# === END: Forecast Accuracy — Sport Mode wiring ==============================
