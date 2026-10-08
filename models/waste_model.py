"""Waste Intelligence: Forecasts capacity utilization and flags overflow hazards."""
import pandas as pd

class WasteIntelligenceModel:
    def evaluate_capacity_risk(self, df: pd.DataFrame) -> pd.DataFrame:
        res = df.copy()
        res["capacity_utilization"] = (res["waste_generated"] / (res["collection_capacity"] + 1e-4)) * 100.0
        res["overflow_risk"] = res["capacity_utilization"] > 90.0
        return res