# from rag.vector_store import search_vector_store


# def generate_rag_answer(question):
#     retrieved_docs = search_vector_store(question)

#     context = "\n\n".join(
#         [doc["content"] for doc in retrieved_docs]
#     )

#     sources = [doc["file_name"] for doc in retrieved_docs]

#     return {
#         "question": question,
#         "answer": context,
#         "sources": sources
#     }



from rag.vector_store import search_vector_store


def generate_rag_answer(question):

    retrieved_docs = search_vector_store(question)

    combined_context = "\n".join(
        [doc["content"] for doc in retrieved_docs]
    )

    question_lower = question.lower()

    answer = "No relevant answer found."

    # Return / Refund Questions
    if "refund" in question_lower or "return" in question_lower:

        if "7 days" in combined_context:
            answer = (
                "Customers can return damaged or defective products within 7 days of delivery. "
                "Refunds are processed after product verification."
            )

    # Discount Questions
    elif "discount" in question_lower:

        answer = (
            "Discounts are available during festive campaigns, clearance sales, loyalty offers, "
            "and premium customer programs."
        )

    elif "help" in question_lower or "support" in question_lower:

        answer = (
            "RetailMind AI helps with demand forecasting, anomaly detection, sales analytics, "
            "discount insights, and customer support queries."
        )

    else:
        answer = combined_context[:400]

    return {
        "question": question,
        "answer": answer,
        "sources": [
            doc["file_name"] for doc in retrieved_docs
        ]
    }