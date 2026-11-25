from qdrant_client import models
from langchain_core.documents import Document

from backend.app.rag.vector_store import open_vector_store


def retrieve_relevant_chunks(
    question: str,
    customer_id: str,
    document_type: str = None,
    limit: int = 5
):
    """
    Retrieve customer-specific knowledge.

    Topic cards:
        Retrieve all chunks in original document order.

    General chat:
        Retrieve semantically relevant chunks.
    """

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    if not customer_id.strip():
        raise ValueError("Customer ID cannot be empty.")

    conditions = [
        models.FieldCondition(
            key="metadata.customer_id",
            match=models.MatchValue(value=customer_id)
        )
    ]

    if document_type:
        conditions.append(
            models.FieldCondition(
                key="metadata.document_type",
                match=models.MatchValue(value=document_type)
            )
        )

    query_filter = models.Filter(must=conditions)

    vector_store, client = open_vector_store()

    try:

        # Topic card: retrieve the complete document.
        if document_type:

            all_documents = []
            offset = None

            while True:

                points, offset = client.scroll(
                    collection_name="glue_assist_lab",
                    scroll_filter=query_filter,
                    limit=100,
                    offset=offset,
                    with_payload=True,
                    with_vectors=False
                )

                for point in points:

                    payload = point.payload or {}
                    metadata = payload.get("metadata", {})

                    all_documents.append(
                        Document(
                            page_content=payload.get("page_content", ""),
                            metadata=metadata
                        )
                    )

                if offset is None:
                    break

            all_documents.sort(
                key=lambda doc: doc.metadata.get("chunk_index", 0)
            )

            return all_documents

        # General chat: semantic retrieval.
        results = vector_store.similarity_search(
            query=question,
            k=limit,
            filter=query_filter
        )

        return results

    finally:
        client.close()
