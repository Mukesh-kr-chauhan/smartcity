"""Automated unit and integration test suite for SmartCity AI."""
import pytest
import pandas as pd

from analysis.preprocessing import clean_dataframe, merge_city_data
from analysis.problem_detection import detect_structured_problems
from analysis.priority_engine import score_problem_priority, prioritize_all_problems
from analysis.sustainability_score import compute_city_sustainability_score
from analysis.impact_estimation import estimate_remediation_impact
from agents.fallback_agent import generate_rule_based_recommendation
from scenarios.simulator import inject_scenario

@pytest.fixture
def mock_clean_data():
    ts = pd.date_range("2026-01-01", periods=10, freq="h")
    zones = ["Zone A", "Zone B"]
    records = []
    for z in zones:
        for t in ts:
            records.append({
                "zone_id": z,
                "timestamp": t,
                "vehicle_count": 800,
                "average_speed": 40.0,
                "congestion_level": "Low",
                "travel_time": 15.0,
                "idle_time": 2.0,
                "electricity_consumption": 4000.0,
                "peak_demand": 4500.0,
                "renewable_generation": 500.0,
                "energy_efficiency_indicator": 75.0,
                "water_consumption": 6000.0,
                "water_flow": 2.5,
                "pressure": 3.8,
                "historical_average": 6000.0,
                "waste_generated": 300.0,
                "waste_collected": 280.0,
                "collection_capacity": 1000.0,
                "PM2_5": 20.0,
                "PM10": 35.0,
                "CO2": 410.0,
                "NO2": 20.0,
                "AQI": 45
            })
    df = pd.DataFrame(records)
    return {
        "traffic": df[["zone_id", "timestamp", "vehicle_count", "average_speed", "congestion_level", "travel_time", "idle_time"]],
        "energy": df[["zone_id", "timestamp", "electricity_consumption", "peak_demand", "renewable_generation", "energy_efficiency_indicator"]],
        "water": df[["zone_id", "timestamp", "water_consumption", "water_flow", "pressure", "historical_average"]],
        "waste": df[["zone_id", "timestamp", "waste_generated", "waste_collected", "collection_capacity"]],
        "air_quality": df[["zone_id", "timestamp", "PM2_5", "PM10", "CO2", "NO2", "AQI"]]
    }

def test_preprocessing_and_merge(mock_clean_data):
    merged = merge_city_data(mock_clean_data)
    assert not merged.empty
    assert "zone_id" in merged.columns
    assert "vehicle_count" in merged.columns
    assert "water_consumption" in merged.columns

def test_priority_engine():
    dummy_problem = {
        "problem_id": "TEST-01",
        "category": "Water",
        "zone": "Zone B",
        "severity": "CRITICAL",
        "detected_value": 12000,
        "expected_value": 6000,
        "deviation_percent": 100.0,
        "explanation": "Test water anomaly."
    }
    scored = score_problem_priority(dummy_problem, [])
    assert "priority_score" in scored
    assert 0 <= scored["priority_score"] <= 100
    assert scored["priority_status"] in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]

def test_fallback_recommendation():
    dummy_problem = {
        "problem_id": "TEST-02",
        "category": "Water",
        "zone": "Zone B",
        "deviation_percent": 56.0
    }
    rec = generate_rule_based_recommendation(dummy_problem)
    assert "action" in rec
    assert "human_verification" in rec
    assert rec["human_verification"] is True

def test_scenario_injection(mock_clean_data):
    scen_data = inject_scenario(mock_clean_data, "Water Leak Scenario")
    zone_b_water = scen_data["water"][scen_data["water"]["zone_id"] == "Zone B"]
    assert zone_b_water["water_consumption"].max() > 6000.0

def test_impact_estimation():
    problems = [{
        "category": "Water",
        "deviation_percent": 50.0,
        "detected_value": 15000,
        "expected_value": 10000,
        "supporting_evidence": {}
    }]
    impact = estimate_remediation_impact(problems)
    assert impact["water_saved_liters_day"] > 0
    assert "note" in impact