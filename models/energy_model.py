"""Energy Intelligence: Random Forest baseline for expected power demand."""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

class EnergyIntelligenceModel:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=30, random_state=42, max_depth=5)
        self.is_fitted = False

    def fit(self, df: pd.DataFrame):
        feat = self._extract(df)
        X = feat[["hour", "day_of_week"]]
        y = feat["electricity_consumption"]
        self.model.fit(X, y)
        self.is_fitted = True

    def predict_expected(self, df: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted:
            self.fit(df)
        feat = self._extract(df)
        return self.model.predict(feat[["hour", "day_of_week"]])

    def _extract(self, df: pd.DataFrame) -> pd.DataFrame:
        t = df.copy()
        ts = pd.to_datetime(t["timestamp"])
        t["hour"] = ts.dt.hour
        t["day_of_week"] = ts.dt.dayofweek
        return t