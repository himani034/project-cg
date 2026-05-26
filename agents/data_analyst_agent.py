# import pandas as pd
# from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parents[1]
# DATA_PATH = BASE_DIR / "data" / "final_retail_ml_output.csv"


# def data_analyst_agent(question):
#     df = pd.read_csv(DATA_PATH)

#     total_revenue = round(df["revenue"].sum(), 2)
#     total_units = int(df["units_sold"].sum())
#     top_category = df.groupby("category")["revenue"].sum().idxmax()
#     top_region = df.groupby("region")["revenue"].sum().idxmax()
#     anomaly_count = int(df["model_anomaly_prediction"].sum())

#     return {
#         "agent": "Data Analyst Agent",
#         "question": question,
#         "answer": f"Total revenue is {total_revenue}. Total units sold are {total_units}. Top category is {top_category}. Top region is {top_region}. Total detected anomalies are {anomaly_count}."
#     }



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
    anomaly_count = int(df["model_anomaly_prediction"].sum())

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