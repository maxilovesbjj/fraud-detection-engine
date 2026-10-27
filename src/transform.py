import joblib
import numpy as np
import polars as pl
from sklearn.preprocessing import RobustScaler
from src.config import SCALER_PATH, ALL_FEATURES, TARGET
from src.ingesta import load_and_deduplicate, temporal_split

class FeatureTransformer:
    def __init__(self):
        self.scaler = RobustScaler()
        self.is_fitted = False

    def fit(self, df_train: pl.DataFrame):
        amount_matrix = df_train.select("Amount").to_numpy()
        self.scaler.fit(amount_matrix)
        self.is_fitted = True
        SCALER_PATH.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.scaler, SCALER_PATH)

    def transform(self, df: pl.DataFrame) -> pl.DataFrame:
        if not self.is_fitted and SCALER_PATH.exists():
            self.scaler = joblib.load(SCALER_PATH)
            self.is_fitted = True
        elif not self.is_fitted:
            raise RuntimeError("El transformador debe ajustarse antes de transformar.")

        # Ciclo circadiano de 24 horas (86400 segundos)
        time_arr = df.select("Time").to_numpy().ravel()
        seconds_in_day = 86400.0
        time_sin = np.sin(2 * np.pi * time_arr / seconds_in_day)
        time_cos = np.cos(2 * np.pi * time_arr / seconds_in_day)

        amount_scaled = self.scaler.transform(df.select("Amount").to_numpy()).ravel()

        return df.with_columns([
            pl.Series("Amount", amount_scaled, dtype=pl.Float64),
            pl.Series("time_sin", time_sin, dtype=pl.Float64),
            pl.Series("time_cos", time_cos, dtype=pl.Float64)
        ])

def prepare_datasets():
    df = load_and_deduplicate()
    train, val, test = temporal_split(df)
    
    transformer = FeatureTransformer()
    transformer.fit(train)
    
    return transformer.transform(train), transformer.transform(val), transformer.transform(test)

if __name__ == "__main__":
    prepare_datasets()
