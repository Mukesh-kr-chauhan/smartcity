"""Traffic Intelligence: Predicts expected speed and flags abnormal bottlenecks."""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

class TrafficIntelligenceModel:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=30, random_state=42, max_depth=5)
        self.is_fitted = False

    def fit(self, df: pd.DataFrame):
        df_feat = self._create_features(df)
        X = df_feat[["hour", "is_weekend", "vehicle_count"]]
        y = df_feat["average_speed"]
        self.model.fit(X, y)
        self.is_fitted = True

    def predict_expected_speed(self, df: pd.DataFrame) -> np.ndarray:
        df_feat = self._create_features(df)
        if not self.is_fitted:
            self.fit(df)
        X = df_feat[["hour", "is_weekend", "vehicle_count"]]
        return self.model.predict(X)

    def _create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        temp = df.copy()
        ts = pd.to_datetime(temp["timestamp"])
        temp["hour"] = ts.dt.hour
        temp["is_weekend"] = (ts.dt.weekday >= 5).astype(int)
        return temp