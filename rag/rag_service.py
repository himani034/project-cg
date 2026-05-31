from rag.vector_store import search_vector_store


def generate_rag_answer(question):
    retrieved_docs = search_vector_store(question)

    context = "\n\n".join(
        [doc["content"] for doc in retrieved_docs]
    )

    sources = [
        doc["file_name"] for doc in retrieved_docs
    ]

    return {
        "question": question,
        "answer": context,
        "sources": sources
    }