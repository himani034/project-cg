import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR / "backend"))

from app.azure_openai_service import generate_agent_answer


def ml_expert_agent(question):

    context = """
RetailMind AI ML Details:
- Demand forecasting model: Random Forest Regressor
- Anomaly detection model: Isolation Forest
- Evaluation metrics: MAE and R2 Score
- Model persistence: Pickle files
- Backend integration: FastAPI prediction APIs
"""

    system_prompt = """
You are RetailMind AI ML Expert Agent.
Explain ML concepts and model outputs in simple professional language.
Keep answer suitable for sprint project evaluation.
"""

    final_answer = generate_agent_answer(
        system_prompt=system_prompt,
        user_question=question,
        context=context
    )

    return {
        "agent": "ML Expert Agent",
        "question": question,
        "answer": final_answer
    }