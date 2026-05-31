from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rag.document_loader import load_documents

documents = load_documents()

texts = [doc["content"] for doc in documents]

vectorizer = TfidfVectorizer()

document_vectors = vectorizer.fit_transform(texts)


def search_vector_store(query, top_k=2):

    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(
        query_vector,
        document_vectors
    ).flatten()

    top_indexes = similarities.argsort()[::-1][:top_k]

    results = []

    for index in top_indexes:
        results.append(documents[index])

    return results