# import sys
# from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parents[1]
# sys.path.append(str(BASE_DIR / "backend"))

# from rag.rag_service import generate_rag_answer
# from app.azure_openai_service import generate_agent_answer


# def document_assistant_agent(question):
#     rag_result = generate_rag_answer(question)

#     system_prompt = """
# You are RetailMind AI Document Assistant Agent.
# Use only the provided RAG context from retail PDFs.
# Do not make up information.
# If answer is not available, say it is not available in the knowledge base.
# """

#     final_answer = generate_agent_answer(
#         system_prompt=system_prompt,
#         user_question=question,
#         context=rag_result["answer"]
#     )

#     return {
#         "agent": "Document Assistant Agent",
#         "question": question,
#         "answer": final_answer,
#         "sources": rag_result["sources"]
#     }


import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR / "backend"))

from rag.rag_service import generate_rag_answer
from app.azure_openai_service import generate_agent_answer


def document_assistant_agent(question):
    rag_result = generate_rag_answer(question)

    system_prompt = """
You are RetailMind AI Document Assistant Agent.
Use the given RAG context from retail policy PDFs.
Answer naturally and professionally.
Do not copy the full context directly.
If answer is not available, say it is not available in the knowledge base.
"""

    final_answer = generate_agent_answer(
        system_prompt=system_prompt,
        user_question=question,
        context=rag_result["answer"]
    )

    return {
        "agent": "Document Assistant Agent",
        "question": question,
        "answer": final_answer,
        "sources": rag_result["sources"]
    }