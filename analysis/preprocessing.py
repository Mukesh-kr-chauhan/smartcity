"""Preprocessing pipeline for cleaning, timestamp conversion, and zone-level alignment."""
import pandas as pd
import numpy as np
from typing import Dict

def clean_dataframe(df: pd.DataFrame, num_cols: list) -> pd.DataFrame:
    df = df.copy()
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.drop_duplicates(subset=["zone_id", "timestamp"]).sort_values("timestamp")
    
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
            df[c] = df[c].fillna(df[c].median())
    return df

def preprocess_city_data(raw_dict: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    cleaned = {}
    cleaned["traffic"] = clean_dataframe(
        raw_dict["traffic"], ["vehicle_count", "average_speed", "travel_time", "idle_time"]
    )
    cleaned["energy"] = clean_dataframe(
        raw_dict["energy"], ["electricity_consumption", "peak_demand", "renewable_generation", "energy_efficiency_indicator"]
    )
    cleaned["water"] = clean_dataframe(
        raw_dict["water"], ["water_consumption", "water_flow", "pressure", "historical_average"]
    )
    cleaned["waste"] = clean_dataframe(
        raw_dict["waste"], ["waste_generated", "waste_collected", "collection_capacity"]
    )
    cleaned["air_quality"] = clean_dataframe(
        raw_dict["air_quality"], ["PM2_5", "PM10", "CO2", "NO2", "AQI"]
    )
    return cleaned

def merge_city_data(clean_dict: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Merges all 5 domains on (zone_id, timestamp) for unified multi-domain reasoning."""
    base = clean_dict["traffic"][["zone_id", "timestamp", "vehicle_count", "average_speed", "congestion_level", "travel_time", "idle_time"]]
    
    merged = base.merge(
        clean_dict["energy"][["zone_id", "timestamp", "electricity_consumption", "peak_demand", "renewable_generation", "energy_efficiency_indicator"]],
        on=["zone_id", "timestamp"], how="inner"
    )
    merged = merged.merge(
        clean_dict["water"][["zone_id", "timestamp", "water_consumption", "water_flow", "pressure", "historical_average"]],
        on=["zone_id", "timestamp"], how="inner"
    )
    merged = merged.merge(
        clean_dict["waste"][["zone_id", "timestamp", "waste_generated", "waste_collected", "collection_capacity"]],
        on=["zone_id", "timestamp"], how="inner"
    )
    merged = merged.merge(
        clean_dict["air_quality"][["zone_id", "timestamp", "PM2_5", "PM10", "CO2", "NO2", "AQI"]],
        on=["zone_id", "timestamp"], how="inner"
    )
    return merged