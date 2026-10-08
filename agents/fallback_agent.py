"""High-reliability, deterministic rule-based decision agent."""
from typing import Dict, Any

def generate_rule_based_recommendation(problem: Dict[str, Any]) -> Dict[str, Any]:
    cat = problem.get("category", "")
    zone = problem.get("zone", "City")
    dev = problem.get("deviation_percent", 0.0)

    if cat == "Water":
        action = (
            f"Dispatch diagnostic team to inspect {zone} sub-surface flow sensors "
            f"and verify pressure relief valves in district distribution line."
        )
        reason = (
            f"Water consumption is currently {dev:.1f}% above baseline with correlated pressure decline, "
            f"indicating probable pipeline breach or unmetered utility tap."
        )
        benefit = "Immediate curtailment of unmetered water losses and stabilization of hydraulic pressure."
        confidence = 0.88

    elif cat == "Traffic":
        action = (
            f"Switch {zone} arterial signal controllers to dynamic congestion mitigation cycle "
            f"and push navigational rerouting notices to public transit displays."
        )
        reason = f"Average vehicle velocity dropped {dev:.1f}% below modeled corridor baseline."
        benefit = "Expected 20-30% reduction in vehicle idle duration and localized exhaust accumulation."
        confidence = 0.84

    elif cat == "Energy":
        action = (
            f"Initiate load shedding protocol for secondary municipal loads in {zone} "
            f"and activate battery energy storage systems (BESS)."
        )
        reason = f"Electricity consumption exceeded expected baseline by {dev:.1f}% during peak tariff hours."
        benefit = "Prevention of localized transformer overload and reduction in peak power acquisition costs."
        confidence = 0.86

    elif cat == "Air Quality":
        action = (
            f"Enforce low-emission perimeter protocols in {zone}, deploy mobile misting trucks, "
            f"and restrict heavy freight transit corridors."
        )
        reason = f"AQI spiked {dev:.1f}% above municipal health thresholds, driven by elevated particulate matter."
        benefit = "Mitigation of immediate cardiovascular/respiratory exposure risks for urban population."
        confidence = 0.89

    elif cat == "Waste":
        action = (
            f"Reroute 2 reserve high-capacity collection compactors to {zone} commercial bin hubs."
        )
        reason = f"Waste generation exceeded standard bin collection capacity by {dev:.1f}%."
        benefit = "Prevention of sidewalk accumulation overflow and street sanitation hazards."
        confidence = 0.82

    else:
        action = f"Perform on-site multi-sensor diagnostic verification across {zone}."
        reason = "Unclassified sensor variance flagged by central anomaly detection."
        benefit = "Clarification of physical infrastructure operational integrity."
        confidence = 0.75

    return {
        "problem_id": problem.get("problem_id"),
        "zone": zone,
        "category": cat,
        "action": action,
        "reason": reason,
        "expected_benefit": benefit,
        "confidence": confidence,
        "human_verification": True,
        "provider": "Rule-Based Decision Engine"
    }