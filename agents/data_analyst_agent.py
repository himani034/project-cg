import sys
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR / "backend"))

from app.azure_openai_service import generate_agent_answer

DATA_PATH = BASE_DIR / "data" / "final_retail_ml_output.csv"


def data_analyst_agent(question):
    df = pd.read_csv(DATA_PATH)

    total_revenue = round(df["revenue"].sum(), 2)
    total_units = int(df["units_sold"].sum())
    top_category = df.groupby("category")["revenue"].sum().idxmax()
    top_region = df.groupby("region")["revenue"].sum().idxmax()

    if "model_anomaly_prediction" in df.columns:
        anomaly_count = int((df["model_anomaly_prediction"] == -1).sum())

    elif "anomaly_prediction" in df.columns:
        anomaly_count = int((df["anomaly_prediction"] == -1).sum())

    elif "is_anomaly" in df.columns:
        anomaly_count = int(df["is_anomaly"].sum())

    else:
        anomaly_count = 0

    context = f"""
Retail Analytics Summary:
- Total revenue: {total_revenue}
- Total units sold: {total_units}
- Highest revenue category: {top_category}
- Highest revenue region: {top_region}
- Total detected anomalies: {anomaly_count}
"""

    system_prompt = """
You are RetailMind AI Data Analyst Agent.
Answer using only the provided retail analytics summary.
Keep the answer short, clear, and professional.
"""

    final_answer = generate_agent_answer(
        system_prompt=system_prompt,
        user_question=question,
        context=context
    )

    return {
        "agent": "Data Analyst Agent",
        "question": question,
        "answer": final_answer
    }