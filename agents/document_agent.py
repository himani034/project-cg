from rag.rag_service import generate_rag_answer


def document_assistant_agent(question):
    rag_result = generate_rag_answer(question)

    return {
        "agent": "Document Assistant Agent",
        "question": question,
        "answer": rag_result["answer"],
        "sources": rag_result["sources"]
    }