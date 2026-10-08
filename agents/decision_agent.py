"""AI Decision Support Agent using Google Gemini SDK with fallback."""
import json
from typing import Dict, Any, List
from utils.config import GEMINI_API_KEY, GEMINI_MODEL
from agents.fallback_agent import generate_rule_based_recommendation

def generate_decision_support(
    problem: Dict[str, Any],
    cross_insights: List[Dict[str, Any]] = None
) -> Dict[str, Any]:
    # Fallback immediately if no API key is provided
    if not GEMINI_API_KEY:
        return generate_rule_based_recommendation(problem)

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=GEMINI_API_KEY)

        prompt_context = {
            "problem": problem,
            "applicable_cross_domain_insights": [
                s for s in (cross_insights or []) if s.get("zone") == problem.get("zone")
            ]
        }

        system_instruction = (
            "You are the SmartCity AI Decision-Support Agent for a sustainable city platform. "
            "Synthesize city anomalies into clear, explainable, and responsible recommendations. "
            "Never claim to control infrastructure directly. Always insist on human verification. "
            "Output strictly valid JSON with keys: 'action', 'reason', 'expected_benefit', 'confidence'."
        )

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.1,
            response_mime_type="application/json"
        )

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=json.dumps(prompt_context),
            config=config
        )

        content = json.loads(response.text)
        return {
            "problem_id": problem.get("problem_id"),
            "zone": problem.get("zone"),
            "category": problem.get("category"),
            "action": content.get("action"),
            "reason": content.get("reason"),
            "expected_benefit": content.get("expected_benefit"),
            "confidence": float(content.get("confidence", 0.90)),
            "human_verification": True,
            "provider": f"Gemini Agent ({GEMINI_MODEL})"
        }

    except Exception as e:
        fallback = generate_rule_based_recommendation(problem)
        fallback["provider"] = f"Rule-Based (Gemini Fallback: {str(e)[:30]}...)"
        return fallback