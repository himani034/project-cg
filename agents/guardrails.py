def is_allowed_question(question):
    allowed_keywords = [
        "sales", "revenue", "forecast", "demand", "anomaly",
        "product", "category", "region", "policy", "refund",
        "return", "discount", "customer", "inventory", "stock",
        "campaign", "conversion", "retail", "model", "prediction"
    ]

    question = question.lower()

    return any(keyword in question for keyword in allowed_keywords)


def blocked_response():
    return {
        "selected_agent": "Guardrail",
        "agent_response": {
            "answer": "I can only answer questions related to retail analytics, demand forecasting, anomaly detection, product policies, and customer support."
        }
    }