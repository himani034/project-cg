def ml_expert_agent(question):
    return {
        "agent": "ML Expert Agent",
        "question": question,
        "answer": "The system uses Random Forest Regressor for demand forecasting and Isolation Forest for anomaly detection. The models were trained on cleaned retail data, evaluated using MAE and R2 score, saved using pickle, and integrated with FastAPI APIs."
    }