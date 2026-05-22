import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "final_retail_ml_output.csv"


def data_analyst_agent(question):
    df = pd.read_csv(DATA_PATH)

    total_revenue = round(df["revenue"].sum(), 2)
    total_units = int(df["units_sold"].sum())
    top_category = df.groupby("category")["revenue"].sum().idxmax()
    top_region = df.groupby("region")["revenue"].sum().idxmax()
    anomaly_count = int(df["model_anomaly_prediction"].sum())

    return {
        "agent": "Data Analyst Agent",
        "question": question,
        "answer": f"Total revenue is {total_revenue}. Total units sold are {total_units}. Top category is {top_category}. Top region is {top_region}. Total detected anomalies are {anomaly_count}."
    }