"""Water Intelligence: Compares consumption against dynamic and historical baselines."""
import pandas as pd

class WaterIntelligenceModel:
    def detect_anomalies(self, df: pd.DataFrame, threshold_ratio: float = 1.35) -> pd.DataFrame:
        res = df.copy()
        if "historical_average" not in res.columns or res["historical_average"].isnull().all():
            res["expected_consumption"] = res.groupby("zone_id")["water_consumption"].transform(lambda x: x.rolling(24, min_periods=3).mean())
            res["expected_consumption"] = res["expected_consumption"].fillna(res["water_consumption"].median())
        else:
            res["expected_consumption"] = res["historical_average"]

        res["consumption_ratio"] = res["water_consumption"] / (res["expected_consumption"] + 1e-4)
        res["is_anomaly"] = res["consumption_ratio"] >= threshold_ratio
        return res