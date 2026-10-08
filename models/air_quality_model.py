"""Air Quality Intelligence: IsolationForest and threshold model for hazardous AQI."""
import pandas as pd
from sklearn.ensemble import IsolationForest

class AirQualityIntelligenceModel:
    def __init__(self):
        self.iso = IsolationForest(contamination=0.05, random_state=42)

    def detect_spikes(self, df: pd.DataFrame) -> pd.DataFrame:
        res = df.copy()
        feats = res[["PM2_5", "NO2", "AQI"]].fillna(0)
        res["anomaly_flag"] = self.iso.fit_predict(feats)
        res["is_aqi_anomaly"] = (res["anomaly_flag"] == -1) | (res["AQI"] > 140)
        return res