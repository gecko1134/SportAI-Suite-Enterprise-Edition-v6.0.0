#!/usr/bin/env python3
"""
SportsKey → SportAI Reverse Export Utility
=========================================
Exports Zones/Slots/Pricing from SportsKey into:
  1) CSV (sportskey_import_template.csv compatible)
  2) JSON (sportskey_starter_config.json compatible shell)

Two modes:
- LIVE: Pulls from SportsKey REST API using env vars (SPORTSKEY_API_BASE, SPORTSKEY_API_TOKEN).
- OFFLINE: Reads a local JSON file that matches the starter config ("--offline path/to/config.json").

Usage:
  LIVE:
    export SPORTSKEY_API_BASE="https://api.sportskey.example/v1"
    export SPORTSKEY_API_TOKEN="YOUR_TOKEN"
    python sportskey_reverse_export.py --out-dir ./out

  OFFLINE (demo with existing config):
    python sportskey_reverse_export.py --offline ./sportskey_starter_config.json --out-dir ./out

Outputs (in --out-dir):
  - sportskey_export.csv
  - sportskey_export.json

Notes:
- This script doesn't know your exact SportsKey object model. Update the fetch_* functions to match your API.
- CSV columns mirror the import template used earlier.
"""

import os, sys, json, csv, argparse, time, datetime
from typing import Dict, Any, List, Optional

CSV_FIELDS = [
    "facility_id","zone_id","zone_name","group","sport","slot_id","duration_min",
    "prime","price_band","credit_cost_base","fmv_hr","visibility","member_tier_required",
    "splittable","children","merge_rule","setup_buffer_min"
]

def _now_iso() -> str:
    return datetime.datetime.utcnow().isoformat() + "Z"

# ---------- LIVE FETCH PLACEHOLDERS (customize to your API) ----------
def fetch_facilities_live() -> List[Dict[str, Any]]:
    """Call your SportsKey API to fetch facilities. Placeholder returns []."""
    # Example:
    # resp = requests.get(f"{BASE}/facilities", headers=HEADERS).json()
    return []

def fetch_zones_live(facility_id: str) -> List[Dict[str, Any]]:
    """Call your SportsKey API to fetch zones per facility. Placeholder returns []."""
    return []

def fetch_slots_live(zone_id: str) -> List[Dict[str, Any]]:
    """Call your SportsKey API to fetch slot templates per zone. Placeholder returns []."""
    return []

# ---------- OFFLINE: Read from our starter config ----------
def load_offline_config(path: str) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

# ---------- TRANSFORMERS ----------
def compose_records_from_config(cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    fmv_map = cfg.get("pricing_engine", {}).get("fmv", {})
    for fac in cfg.get("facilities", []):
        facility_id = fac.get("facility_id", "")
        for z in fac.get("zones", []):
            zone_id = z.get("zone_id")
            zone_name = z.get("name")
            group = z.get("group")
            cap = z.get("capabilities", {})
            sports = cap.get("sports", ["general"])
            setup_buffer_min = cap.get("setup_buffer_min", 0)
            split = z.get("split_merge", {})
            splittable = split.get("splittable", False)
            children = "|".join(split.get("children", [])) if split.get("children") else ""
            merge_rule = split.get("merge_rule", "manual")
            fmv_hr = fmv_map.get(group, fmv_map.get(zone_id, 0))
            for s in z.get("slots", []):
                slot_id = s.get("slot_id")
                duration_min = s.get("duration_min")
                prime = str(bool(s.get("prime", False))).upper()
                price_band = s.get("price_band", "")
                credit_cost_base = s.get("credit_cost_base", 0)
                # choose first sport as primary for the CSV row
                sport = sports[0] if sports else "general"
                # visibility defaults (could be enhanced by your visibility rules)
                visibility = "public"
                member_tier_required = ""
                records.append({
                    "facility_id": facility_id,
                    "zone_id": zone_id,
                    "zone_name": zone_name,
                    "group": group,
                    "sport": sport,
                    "slot_id": slot_id,
                    "duration_min": duration_min,
                    "prime": prime,
                    "price_band": price_band,
                    "credit_cost_base": credit_cost_base,
                    "fmv_hr": fmv_hr,
                    "visibility": visibility,
                    "member_tier_required": member_tier_required,
                    "splittable": str(bool(splittable)).upper(),
                    "children": children,
                    "merge_rule": merge_rule,
                    "setup_buffer_min": setup_buffer_min
                })
    return records

def to_json_shell(cfg: Dict[str, Any]) -> Dict[str, Any]:
    """Return a minimal JSON shell reflecting the starter schema (useful for audits)."""
    shell = {
        "meta": {
            "version": cfg.get("meta", {}).get("version", "1.0.0"),
            "exported_at": _now_iso(),
            "source": "SportsKey",
            "facility_name": cfg.get("meta", {}).get("facility_name", ""),
        },
        "facilities": cfg.get("facilities", []),
        "pricing_engine": cfg.get("pricing_engine", {}),
        "fairness_guards": cfg.get("fairness_guards", {}),
        "visibility": cfg.get("visibility", {}),
        "automation": cfg.get("automation", {})
    }
    return shell

# ---------- OUTPUT WRITERS ----------
def write_csv(path: str, rows: List[Dict[str, Any]]) -> None:
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow(r)

def write_json(path: str, obj: Dict[str, Any]) -> None:
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)

# ---------- CLI ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", help="Path to local config JSON (starter schema). If set, runs in offline mode.")
    ap.add_argument("--out-dir", default="./out", help="Output directory for CSV/JSON.")
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    csv_out = os.path.join(args.out_dir, "sportskey_export.csv")
    json_out = os.path.join(args.out_dir, "sportskey_export.json")

    if args.offline:
        cfg = load_offline_config(args.offline)
        rows = compose_records_from_config(cfg)
        shell = to_json_shell(cfg)
    else:
        # LIVE mode — wire these to your SportsKey API
        facilities = fetch_facilities_live()
        cfg_like = {
            "meta": {"version": "1.0.0", "facility_name": "Unknown (LIVE)", "exported_at": _now_iso()},
            "facilities": [],
            "pricing_engine": {"fmv": {}}, # fill from your pricing sources
            "fairness_guards": {},
            "visibility": {},
            "automation": {}
        }
        # Example structure builder (fill in from actual API objects)
        for fac in facilities:
            fac_obj = {"facility_id": fac["id"], "name": fac["name"], "timezone": fac.get("timezone", "UTC"), "zones": []}
            for z in fetch_zones_live(fac["id"]):
                zone_obj = {
                    "zone_id": z["id"], "name": z["name"], "group": z.get("group",""),
                    "capabilities": {
                        "sports": z.get("sports", ["general"]),
                        "min_party_size": z.get("min_party_size", 1),
                        "max_party_size": z.get("max_party_size", 50),
                        "equipment": z.get("equipment", []),
                        "clear_height_ft": z.get("clear_height_ft", 0),
                        "setup_buffer_min": z.get("setup_buffer_min", 0)
                    },
                    "split_merge": {
                        "splittable": z.get("splittable", False),
                        "children": z.get("children", []),
                        "merge_rule": z.get("merge_rule", "manual"),
                        "min_block_min": z.get("min_block_min", 30)
                    },
                    "slots": []
                }
                for s in fetch_slots_live(z["id"]):
                    zone_obj["slots"].append({
                        "slot_id": s["slot_id"],
                        "duration_min": s.get("duration_min", 60),
                        "prime": s.get("prime", False),
                        "start_times": s.get("start_times", []),
                        "price_band": s.get("price_band",""),
                        "credit_cost_base": s.get("credit_cost_base", 0)
                    })
                fac_obj["zones"].append(zone_obj)
            cfg_like["facilities"].append(fac_obj)
        cfg = cfg_like
        rows = compose_records_from_config(cfg)
        shell = to_json_shell(cfg)

    write_csv(csv_out, rows)
    write_json(json_out, shell)
    print(f"Wrote: {csv_out}")
    print(f"Wrote: {json_out}")

if __name__ == "__main__":
    main()
