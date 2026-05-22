import pandas as pd
from pathlib import Path

# DATA_PATH = Path("../data/final_retail_ml_output.csv")

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "final_retail_ml_output.csv"

def load_data():
    return pd.read_csv(DATA_PATH)

def get_dataset_summary():
    df = load_data()
    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": list(df.columns)
    }

def get_sales_overview():
    df = load_data()
    return {
        "total_revenue": round(float(df["revenue"].sum()), 2),
        "total_units_sold": int(df["units_sold"].sum()),
        "average_conversion_rate": round(float(df["conversion_rate"].mean()), 4),
        "total_anomalies": int(df["model_anomaly_prediction"].sum())
    }