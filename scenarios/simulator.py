"""Scenario injector for interactive competition demonstrations."""
import pandas as pd
from typing import Dict

def inject_scenario(cleaned_data: Dict[str, pd.DataFrame], scenario_name: str) -> Dict[str, pd.DataFrame]:
    data = {k: v.copy() for k, v in cleaned_data.items()}
    
    if scenario_name == "Water Leak Scenario":
        # Force water burst in Zone B (56% surge, pressure collapse)
        mask = (data["water"]["zone_id"] == "Zone B")
        tail_idx = data["water"][mask].tail(8).index
        data["water"].loc[tail_idx, "water_consumption"] *= 1.56
        data["water"].loc[tail_idx, "pressure"] *= 0.52

    elif scenario_name == "Traffic Congestion Scenario":
        # Gridlock in Zone A
        mask = (data["traffic"]["zone_id"] == "Zone A")
        tail_idx = data["traffic"][mask].tail(8).index
        data["traffic"].loc[tail_idx, "vehicle_count"] = 2450
        data["traffic"].loc[tail_idx, "average_speed"] = 11.2
        data["traffic"].loc[tail_idx, "congestion_level"] = "High"
        data["traffic"].loc[tail_idx, "idle_time"] = 16.5

    elif scenario_name == "Energy Peak Scenario":
        # Critical industrial surge in Zone C
        mask = (data["energy"]["zone_id"] == "Zone C")
        tail_idx = data["energy"][mask].tail(8).index
        data["energy"].loc[tail_idx, "electricity_consumption"] *= 1.48
        data["energy"].loc[tail_idx, "peak_demand"] *= 1.55

    elif scenario_name == "Waste Overflow Scenario":
        # Waste buildup in Zone D
        mask = (data["waste"]["zone_id"] == "Zone D")
        tail_idx = data["waste"][mask].tail(8).index
        data["waste"].loc[tail_idx, "waste_generated"] *= 1.85

    elif scenario_name == "Air Pollution Scenario":
        # Severe smog in Zone B
        mask = (data["air_quality"]["zone_id"] == "Zone B")
        tail_idx = data["air_quality"][mask].tail(8).index
        data["air_quality"].loc[tail_idx, "PM2_5"] = 145.0
        data["air_quality"].loc[tail_idx, "NO2"] = 88.0
        data["air_quality"].loc[tail_idx, "AQI"] = 185

    elif scenario_name == "Combined Sustainability Scenario":
        # Compound multi-system failure across Zone B and Zone A
        mask_w = (data["water"]["zone_id"] == "Zone B")
        tail_w = data["water"][mask_w].tail(8).index
        data["water"].loc[tail_w, "water_consumption"] *= 1.56
        data["water"].loc[tail_w, "pressure"] *= 0.52

        mask_t = (data["traffic"]["zone_id"] == "Zone A")
        tail_t = data["traffic"][mask_t].tail(8).index
        data["traffic"].loc[tail_t, "vehicle_count"] = 2300
        data["traffic"].loc[tail_t, "average_speed"] = 12.0
        data["traffic"].loc[tail_t, "congestion_level"] = "High"
        data["traffic"].loc[tail_t, "idle_time"] = 15.0

        mask_a = (data["air_quality"]["zone_id"] == "Zone A")
        tail_a = data["air_quality"][mask_a].tail(8).index
        data["air_quality"].loc[tail_a, "PM2_5"] = 125.0
        data["air_quality"].loc[tail_a, "NO2"] = 75.0
        data["air_quality"].loc[tail_a, "AQI"] = 170

    return data