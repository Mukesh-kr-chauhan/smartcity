"""Executes all domain ML models to append expectation and anomaly labels."""
import pandas as pd
from typing import Dict
from models.traffic_model import TrafficIntelligenceModel
from models.energy_model import EnergyIntelligenceModel
from models.water_model import WaterIntelligenceModel
from models.waste_model import WasteIntelligenceModel
from models.air_quality_model import AirQualityIntelligenceModel

def run_all_anomaly_models(data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    traffic_model = TrafficIntelligenceModel()
    energy_model = EnergyIntelligenceModel()
    water_model = WaterIntelligenceModel()
    waste_model = WasteIntelligenceModel()
    aqi_model = AirQualityIntelligenceModel()

    # Traffic
    traffic_df = data["traffic"].copy()
    traffic_df["expected_speed"] = traffic_model.predict_expected_speed(traffic_df)
    traffic_df["speed_deficit"] = traffic_df["expected_speed"] - traffic_df["average_speed"]
    traffic_df["is_anomaly"] = (traffic_df["speed_deficit"] > 14.0) & (traffic_df["congestion_level"] == "High")

    # Energy
    energy_df = data["energy"].copy()
    energy_df["expected_consumption"] = energy_model.predict_expected(energy_df)
    energy_df["energy_ratio"] = energy_df["electricity_consumption"] / (energy_df["expected_consumption"] + 1e-4)
    energy_df["is_anomaly"] = energy_df["energy_ratio"] >= 1.30

    # Water
    water_df = water_model.detect_anomalies(data["water"])

    # Waste
    waste_df = waste_model.evaluate_capacity_risk(data["waste"])

    # Air Quality
    air_df = aqi_model.detect_spikes(data["air_quality"])

    return {
        "traffic": traffic_df,
        "energy": energy_df,
        "water": water_df,
        "waste": waste_df,
        "air_quality": air_df
    }