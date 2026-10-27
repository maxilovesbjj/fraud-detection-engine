import polars as pl
from src.config import DATA_PATH, TARGET

def load_and_deduplicate() -> pl.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset no encontrado en: {DATA_PATH}")
    
    # Schema overrides para evitar errores de parseo por notacion cientifica
    schema_overrides = {
        "Time": pl.Float64,
        "Amount": pl.Float64,
        "Class": pl.Int32
    }
    
    df = pl.read_csv(DATA_PATH, schema_overrides=schema_overrides)
    initial_rows = df.height
    df = df.unique()
    print(f"Filas cargadas: {initial_rows} | Duplicados eliminados: {initial_rows - df.height}")
    return df

def temporal_split(df: pl.DataFrame):
    df_sorted = df.sort("Time")
    
    # 48h totales = 172800 seg.
    # Train: 0-32h (115200s) | Val: 32-40h (144000s) | Test: 40-48h
    train_limit = 115200.0
    val_limit = 144000.0
    
    train = df_sorted.filter(pl.col("Time") < train_limit)
    val = df_sorted.filter((pl.col("Time") >= train_limit) & (pl.col("Time") < val_limit))
    test = df_sorted.filter(pl.col("Time") >= val_limit)
    
    print(f"Train: {train.height} filas | Fraudes: {train.filter(pl.col(TARGET) == 1).height}")
    print(f"Val:   {val.height} filas | Fraudes: {val.filter(pl.col(TARGET) == 1).height}")
    print(f"Test:  {test.height} filas | Fraudes: {test.filter(pl.col(TARGET) == 1).height}")
    
    return train, val, test

if __name__ == "__main__":
    df = load_and_deduplicate()
    train, val, test = temporal_split(df)
