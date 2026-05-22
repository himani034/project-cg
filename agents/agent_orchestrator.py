from agents.guardrails import is_allowed_question, blocked_response
from agents.data_analyst_agent import data_analyst_agent
from agents.document_agent import document_assistant_agent
from agents.ml_expert_agent import ml_expert_agent


def route_to_agent(question):
    q = question.lower()

    if not is_allowed_question(question):
        return blocked_response()

    if "policy" in q or "refund" in q or "return" in q or "discount" in q:
        return {
            "selected_agent": "Document Assistant Agent",
            "agent_response": document_assistant_agent(question)
        }

    if "model" in q or "forecast" in q or "prediction" in q or "anomaly" in q:
        return {
            "selected_agent": "ML Expert Agent",
            "agent_response": ml_expert_agent(question)
        }

    return {
        "selected_agent": "Data Analyst Agent",
        "agent_response": data_analyst_agent(question)
    }