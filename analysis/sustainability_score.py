"""Computes the overarching City Sustainability Score across all domains."""
import pandas as pd
from typing import Dict, Tuple
from utils.config import SUSTAINABILITY_WEIGHTS

def compute_city_sustainability_score(evaluated_data: Dict[str, pd.DataFrame]) -> Tuple[float, Dict[str, float]]:
    # Traffic Efficiency (0 - 100)
    trf = evaluated_data["traffic"].tail(50)
    avg_speed = trf["average_speed"].mean()
    traffic_eff = float(min(100.0, max(20.0, (avg_speed / 45.0) * 100.0)))

    # Energy Efficiency (0 - 100)
    eng = evaluated_data["energy"].tail(50)
    energy_eff = float(eng["energy_efficiency_indicator"].mean())

    # Water Efficiency (0 - 100)
    wtr = evaluated_data["water"].tail(50)
    wtr_dev = abs((wtr["water_consumption"] - wtr["historical_average"]) / (wtr["historical_average"] + 1e-4)).mean()
    water_eff = float(max(20.0, min(100.0, (1.0 - wtr_dev) * 100.0)))

    # Waste Efficiency (0 - 100)
    wst = evaluated_data["waste"].tail(50)
    util = (wst["waste_generated"] / (wst["collection_capacity"] + 1e-4)).mean()
    waste_eff = float(max(25.0, min(100.0, (1.1 - util) * 100.0)))

    # Air Quality (0 - 100)
    air = evaluated_data["air_quality"].tail(50)
    avg_aqi = air["AQI"].mean()
    aqi_eff = float(max(15.0, min(100.0, (1.0 - (avg_aqi / 200.0)) * 100.0)))

    sub_scores = {
        "traffic": round(traffic_eff, 1),
        "energy": round(energy_eff, 1),
        "water": round(water_eff, 1),
        "waste": round(waste_eff, 1),
        "air_quality": round(aqi_eff, 1),
    }

    w = SUSTAINABILITY_WEIGHTS
    overall = (
        sub_scores["traffic"] * w["traffic"] +
        sub_scores["energy"] * w["energy"] +
        sub_scores["water"] * w["water"] +
        sub_scores["waste"] * w["waste"] +
        sub_scores["air_quality"] * w["air_quality"]
    )
    return round(overall, 1), sub_scores