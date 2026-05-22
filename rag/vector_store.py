# import numpy as np
# from sentence_transformers import SentenceTransformer
# from rag.document_loader import load_documents

# embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# documents = load_documents()
# texts = [doc["content"] for doc in documents]

# document_embeddings = embedding_model.encode(texts)
# document_embeddings = np.array(document_embeddings)


# def cosine_similarity(a, b):
#     return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# def search_vector_store(query, top_k=2):
#     query_embedding = embedding_model.encode(query)

#     scores = []

#     for index, doc_embedding in enumerate(document_embeddings):
#         score = cosine_similarity(query_embedding, doc_embedding)
#         scores.append((score, documents[index]))

#     scores = sorted(scores, key=lambda x: x[0], reverse=True)

#     return [doc for score, doc in scores[:top_k]]


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