"""Estimates potential environmental benefits if proposed decision-support actions are implemented."""
from typing import List, Dict, Any

def estimate_remediation_impact(problems: List[Dict[str, Any]]) -> Dict[str, Any]:
    impact = {
        "water_saved_liters_day": 0.0,
        "energy_saved_kwh_day": 0.0,
        "emissions_reduced_kg_co2": 0.0,
        "idle_time_saved_hours": 0.0,
        "collection_efficiency_gain_pct": 0.0,
    }

    for p in problems:
        cat = p.get("category")
        dev = max(0.0, p.get("deviation_percent", 0.0))

        if cat == "Water":
            excess_lph = max(0.0, p["detected_value"] - p["expected_value"])
            impact["water_saved_liters_day"] += excess_lph * 18.0

        elif cat == "Energy":
            excess_kwh = max(0.0, p["detected_value"] - p["expected_value"])
            saved_kwh = excess_kwh * 10.0
            impact["energy_saved_kwh_day"] += saved_kwh
            impact["emissions_reduced_kg_co2"] += saved_kwh * 0.42

        elif cat == "Traffic":
            evidence = p.get("supporting_evidence", {})
            idle = evidence.get("idle_time_min", 4.0)
            veh = evidence.get("vehicle_count", 800)
            saved_idle_hrs = (idle * 0.4 * veh) / 60.0
            impact["idle_time_saved_hours"] += saved_idle_hrs
            impact["emissions_reduced_kg_co2"] += saved_idle_hrs * 2.1

        elif cat == "Waste":
            impact["collection_efficiency_gain_pct"] += min(25.0, dev * 0.5)

        elif cat == "Air Quality":
            impact["emissions_reduced_kg_co2"] += 450.0

    return {
        "water_saved_liters_day": round(impact["water_saved_liters_day"], 0),
        "energy_saved_kwh_day": round(impact["energy_saved_kwh_day"], 1),
        "emissions_reduced_kg_co2": round(impact["emissions_reduced_kg_co2"], 1),
        "idle_time_saved_hours": round(impact["idle_time_saved_hours"], 1),
        "collection_efficiency_gain_pct": round(min(impact["collection_efficiency_gain_pct"], 35.0), 1),
        "note": "Estimated impact based on simulated data and model assumptions."
    }