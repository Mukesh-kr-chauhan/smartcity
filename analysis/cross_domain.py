"""Correlates inter-domain synergies (e.g. traffic idle times amplifying NO2/AQI)."""
import pandas as pd
from typing import List, Dict, Any

def analyze_cross_domain_synergies(merged_df: pd.DataFrame) -> List[Dict[str, Any]]:
    insights = []
    recent_merged = merged_df.sort_values("timestamp").groupby("zone_id").last().reset_index()

    for _, row in recent_merged.iterrows():
        zone = row["zone_id"]
        # Synergy 1: Traffic Idling + Air Quality Degradation
        if row["idle_time"] > 6.0 and row["PM2_5"] > 45.0 and row["NO2"] > 35.0:
            insights.append({
                "zone": zone,
                "synergy_type": "Transport-Emissions Hotspot",
                "severity": "CRITICAL" if row["AQI"] > 140 else "HIGH",
                "domains_involved": ["Traffic", "Air Quality"],
                "description": (
                    f"Traffic congestion in {zone} (idle time: {row['idle_time']} min) is strongly associated "
                    f"with elevated vehicle emissions (NO2: {row['NO2']} µg/m³, PM2.5: {row['PM2_5']} µg/m³)."
                ),
                "recommendation_seed": "Deploy dynamic signal retiming and route diversion to cut vehicular idling.",
                "metrics": {
                    "idle_time": row["idle_time"],
                    "vehicle_count": row["vehicle_count"],
                    "NO2": row["NO2"],
                    "PM2_5": row["PM2_5"],
                    "AQI": row["AQI"]
                }
            })

        # Synergy 2: Energy & High Water consumption (possible heat-related utility strain)
        if row["electricity_consumption"] > 7000 and row["water_consumption"] > 10000:
            insights.append({
                "zone": zone,
                "synergy_type": "Compound Utility Surge",
                "severity": "HIGH",
                "domains_involved": ["Energy", "Water"],
                "description": (
                    f"Concurrently high energy ({row['electricity_consumption']:.0f} kWh) and water usage "
                    f"({row['water_consumption']:.0f} L) in {zone} indicates compound municipal resource pressure."
                ),
                "recommendation_seed": "Inspect primary HVAC chillers and industrial cooling loops for dual utility waste.",
                "metrics": {
                    "electricity_kwh": row["electricity_consumption"],
                    "water_liters": row["water_consumption"]
                }
            })

        # Synergy 3: Waste Generation with Traffic Congestion
        if row["waste_generated"] > 600 and row["congestion_level"] == "High":
            insights.append({
                "zone": zone,
                "synergy_type": "Logistics Bottleneck Risk",
                "severity": "MEDIUM",
                "domains_involved": ["Traffic", "Waste"],
                "description": (
                    f"High waste accumulation ({row['waste_generated']:.0f} kg) coincides with road gridlock "
                    f"in {zone}, threatening missed collection windows."
                ),
                "recommendation_seed": "Reschedule municipal collection runs to off-peak night traffic windows.",
                "metrics": {
                    "waste_kg": row["waste_generated"],
                    "speed_kmh": row["average_speed"]
                }
            })

    return insights