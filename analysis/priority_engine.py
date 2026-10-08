"""Calculates the transparent Sustainability Priority Score (0-100)."""
from typing import List, Dict, Any
from utils.config import PRIORITY_WEIGHTS, ZONE_PROFILES

def score_problem_priority(p: Dict[str, Any], cross_domain_insights: List[Dict[str, Any]]) -> Dict[str, Any]:
    dev = abs(float(p.get("deviation_percent", 0.0)))
    category = p.get("category", "")
    zone = p.get("zone", "")
    pop_ratio = ZONE_PROFILES.get(zone, {}).get("base_pop", 30000) / 70000.0

    # 1. Severity Sub-Score (0-100)
    sev_map = {"CRITICAL": 95, "HIGH": 75, "MEDIUM": 50, "LOW": 25}
    base_sev = sev_map.get(p.get("severity", "MEDIUM"), 50)
    severity_score = min(100, base_sev + min(dev * 0.2, 10))

    # 2. Environmental Impact (0-100)
    env_baseline = {"Air Quality": 90, "Water": 85, "Energy": 80, "Traffic": 70, "Waste": 65}
    env_impact = env_baseline.get(category, 60)

    # 3. Urgency Sub-Score (0-100)
    urgency = 80 if p.get("severity") == "CRITICAL" else 60
    if category in ["Water", "Air Quality"]:
        urgency += 15

    # Cross-domain reinforcement check
    has_synergy = any(s["zone"] == zone and category in s["domains_involved"] for s in cross_domain_insights)
    if has_synergy:
        urgency = min(100, urgency + 15)
        severity_score = min(100, severity_score + 10)

    # 4. Resource Waste (0-100)
    res_waste = min(100, 40 + dev * 0.8)

    # 5. Affected Area / Population footprint (0-100)
    affected_score = round(pop_ratio * 100, 1)

    weights = PRIORITY_WEIGHTS
    final_score = (
        severity_score * weights["severity"] +
        urgency * weights["urgency"] +
        env_impact * weights["environmental_impact"] +
        res_waste * weights["resource_waste"] +
        affected_score * weights["affected_area"]
    )

    final_score = round(min(100.0, max(0.0, final_score)), 1)
    status = "CRITICAL" if final_score >= 81 else "HIGH" if final_score >= 61 else "MEDIUM" if final_score >= 31 else "LOW"

    p["priority_score"] = final_score
    p["priority_status"] = status
    p["priority_breakdown"] = {
        "severity": round(severity_score, 1),
        "urgency": round(urgency, 1),
        "environmental_impact": round(env_impact, 1),
        "resource_waste": round(res_waste, 1),
        "affected_area": round(affected_score, 1),
    }
    return p

def prioritize_all_problems(problems: List[Dict[str, Any]], cross_insights: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    scored = [score_problem_priority(p, cross_insights) for p in problems]
    return sorted(scored, key=lambda x: x["priority_score"], reverse=True)