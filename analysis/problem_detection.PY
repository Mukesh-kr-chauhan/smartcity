"""Aggregates raw anomalies into structured, explainable Problem Candidates."""
import pandas as pd
from typing import List, Dict, Any

def detect_structured_problems(evaluated_data: Dict[str, pd.DataFrame]) -> List[Dict[str, Any]]:
    problems = []

    # 1. Water Anomalies
    water_df = evaluated_data["water"]
    recent_water = water_df.sort_values("timestamp").groupby("zone_id").last().reset_index()
    for _, r in recent_water.iterrows():
        if r.get("is_anomaly", False):
            dev = ((r["water_consumption"] - r["expected_consumption"]) / r["expected_consumption"]) * 100.0
            problems.append({
                "problem_id": f"WTR-{r['zone_id'].replace(' ', '')}-{pd.to_datetime(r['timestamp']).strftime('%H%M')}",
                "category": "Water",
                "zone": r["zone_id"],
                "timestamp": str(r["timestamp"]),
                "severity": "CRITICAL" if dev >= 45.0 else "HIGH",
                "detected_value": round(float(r["water_consumption"]), 1),
                "expected_value": round(float(r["expected_consumption"]), 1),
                "deviation_percent": round(float(dev), 1),
                "explanation": f"Water consumption in {r['zone_id']} is {dev:.1f}% above historical baseline with a detected pressure drop.",
                "priority_candidate": True,
                "supporting_evidence": {
                    "pressure_bar": float(r.get("pressure", 3.5)),
                    "flow_rate": float(r.get("water_flow", 2.0)),
                    "historical_baseline": round(float(r["expected_consumption"]), 1)
                }
            })

    # 2. Traffic Bottlenecks
    traffic_df = evaluated_data["traffic"]
    recent_traffic = traffic_df.sort_values("timestamp").groupby("zone_id").last().reset_index()
    for _, r in recent_traffic.iterrows():
        if r.get("is_anomaly", False):
            dev = ((r["expected_speed"] - r["average_speed"]) / r["expected_speed"]) * 100.0
            problems.append({
                "problem_id": f"TRF-{r['zone_id'].replace(' ', '')}-{pd.to_datetime(r['timestamp']).strftime('%H%M')}",
                "category": "Traffic",
                "zone": r["zone_id"],
                "timestamp": str(r["timestamp"]),
                "severity": "HIGH" if r["average_speed"] < 15.0 else "MEDIUM",
                "detected_value": round(float(r["average_speed"]), 1),
                "expected_value": round(float(r["expected_speed"]), 1),
                "deviation_percent": round(float(dev), 1),
                "explanation": f"Severe congestion in {r['zone_id']} - average velocity is {dev:.1f}% below statistical model baseline.",
                "priority_candidate": True,
                "supporting_evidence": {
                    "vehicle_count": int(r["vehicle_count"]),
                    "idle_time_min": float(r["idle_time"]),
                    "congestion_level": r["congestion_level"]
                }
            })

    # 3. Energy Demand Spikes
    energy_df = evaluated_data["energy"]
    recent_energy = energy_df.sort_values("timestamp").groupby("zone_id").last().reset_index()
    for _, r in recent_energy.iterrows():
        if r.get("is_anomaly", False):
            dev = ((r["electricity_consumption"] - r["expected_consumption"]) / r["expected_consumption"]) * 100.0
            problems.append({
                "problem_id": f"ENG-{r['zone_id'].replace(' ', '')}-{pd.to_datetime(r['timestamp']).strftime('%H%M')}",
                "category": "Energy",
                "zone": r["zone_id"],
                "timestamp": str(r["timestamp"]),
                "severity": "HIGH" if dev > 40.0 else "MEDIUM",
                "detected_value": round(float(r["electricity_consumption"]), 1),
                "expected_value": round(float(r["expected_consumption"]), 1),
                "deviation_percent": round(float(dev), 1),
                "explanation": f"Electricity draw in {r['zone_id']} exceeds forecasted demand by {dev:.1f}%.",
                "priority_candidate": True,
                "supporting_evidence": {
                    "peak_demand_kw": float(r["peak_demand"]),
                    "renewable_generation_kw": float(r["renewable_generation"]),
                    "efficiency_idx": float(r["energy_efficiency_indicator"])
                }
            })

    # 4. Air Quality Degradation
    air_df = evaluated_data["air_quality"]
    recent_air = air_df.sort_values("timestamp").groupby("zone_id").last().reset_index()
    for _, r in recent_air.iterrows():
        if r.get("is_aqi_anomaly", False):
            problems.append({
                "problem_id": f"AQI-{r['zone_id'].replace(' ', '')}-{pd.to_datetime(r['timestamp']).strftime('%H%M')}",
                "category": "Air Quality",
                "zone": r["zone_id"],
                "timestamp": str(r["timestamp"]),
                "severity": "CRITICAL" if r["AQI"] > 160 else "HIGH",
                "detected_value": round(float(r["AQI"]), 1),
                "expected_value": 75.0,
                "deviation_percent": round(((r["AQI"] - 75.0) / 75.0) * 100.0, 1),
                "explanation": f"Hazardous air pollutant concentrations observed in {r['zone_id']} with AQI at {int(r['AQI'])}.",
                "priority_candidate": True,
                "supporting_evidence": {
                    "PM2_5": float(r["PM2_5"]),
                    "NO2": float(r["NO2"]),
                    "CO2": float(r["CO2"])
                }
            })

    # 5. Waste Overflow Risk
    waste_df = evaluated_data["waste"]
    recent_waste = waste_df.sort_values("timestamp").groupby("zone_id").last().reset_index()
    for _, r in recent_waste.iterrows():
        if r.get("overflow_risk", False):
            problems.append({
                "problem_id": f"WST-{r['zone_id'].replace(' ', '')}-{pd.to_datetime(r['timestamp']).strftime('%H%M')}",
                "category": "Waste",
                "zone": r["zone_id"],
                "timestamp": str(r["timestamp"]),
                "severity": "HIGH" if r["capacity_utilization"] > 115 else "MEDIUM",
                "detected_value": round(float(r["waste_generated"]), 1),
                "expected_value": round(float(r["collection_capacity"]), 1),
                "deviation_percent": round(float(r["capacity_utilization"] - 100.0), 1),
                "explanation": f"Waste generation in {r['zone_id']} reached {r['capacity_utilization']:.1f}% of collection capacity.",
                "priority_candidate": True,
                "supporting_evidence": {
                    "capacity_kg": float(r["collection_capacity"]),
                    "generated_kg": float(r["waste_generated"])
                }
            })

    return problems