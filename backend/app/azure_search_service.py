import os
from pathlib import Path
from dotenv import load_dotenv

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchFieldDataType
)

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX")


def create_search_index():
    index_client = SearchIndexClient(
        endpoint=AZURE_SEARCH_ENDPOINT,
        credential=AzureKeyCredential(AZURE_SEARCH_KEY)
    )

    fields = [
        SimpleField(
            name="id",
            type=SearchFieldDataType.String,
            key=True
        ),
        SearchableField(
            name="content",
            type=SearchFieldDataType.String
        ),
        SimpleField(
            name="source",
            type=SearchFieldDataType.String,
            filterable=True
        )
    ]

    index = SearchIndex(
        name=AZURE_SEARCH_INDEX,
        fields=fields
    )

    index_client.create_or_update_index(index)

    return {
        "message": "Azure AI Search index created successfully",
        "index_name": AZURE_SEARCH_INDEX
    }


def upload_documents_to_search(documents):
    search_client = SearchClient(
        endpoint=AZURE_SEARCH_ENDPOINT,
        index_name=AZURE_SEARCH_INDEX,
        credential=AzureKeyCredential(AZURE_SEARCH_KEY)
    )

    search_docs = []

    for i, doc in enumerate(documents):
        search_docs.append({
            "id": str(i + 1),
            "content": doc["content"],
            "source": doc["file_name"]
        })

    result = search_client.upload_documents(documents=search_docs)

    return {
        "message": "Documents uploaded to Azure AI Search",
        "uploaded_count": len(result)
    }


def search_azure_documents(query):
    search_client = SearchClient(
        endpoint=AZURE_SEARCH_ENDPOINT,
        index_name=AZURE_SEARCH_INDEX,
        credential=AzureKeyCredential(AZURE_SEARCH_KEY)
    )

    results = search_client.search(
        search_text=query,
        top=3
    )

    output = []

    for result in results:
        output.append({
            "content": result["content"],
            "source": result["source"],
            "score": result["@search.score"]
        })

    return output