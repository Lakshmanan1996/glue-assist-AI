from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, models

from backend.app.rag.ingestion import ingest_documents


# Persistent Qdrant database
QDRANT_PATH = "/opt/glue-assist-ai/data/qdrant_db"

# Lab collection
COLLECTION_NAME = "glue_assist_lab"

# BGE-M3 output dimensions
VECTOR_SIZE = 1024


def get_embedding_model():
    """Load the locally cached BGE-M3 embedding model."""

    return HuggingFaceEmbeddings(
        model="BAAI/bge-m3",
        model_kwargs={"device": "cpu"},
        encode_kwargs={
            "normalize_embeddings": True,
            "batch_size": 8
        },
        show_progress=True
    )


def build_vector_store(recreate: bool = True):
    """Create the Qdrant collection and store all document chunks."""

    Path(QDRANT_PATH).mkdir(parents=True, exist_ok=True)

    chunks = ingest_documents()

    if not chunks:
        raise ValueError("No document chunks found.")

    client = QdrantClient(path=QDRANT_PATH)

    try:
        # Recreate the lab collection to avoid duplicate chunks.
        if client.collection_exists(COLLECTION_NAME):
            if not recreate:
                raise RuntimeError(
                    f"Collection {COLLECTION_NAME} already exists."
                )

            client.delete_collection(COLLECTION_NAME)

        # Create a collection matching BGE-M3 dimensions.
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=VECTOR_SIZE,
                distance=models.Distance.COSINE
            )
        )

        embedding_model = get_embedding_model()

        vector_store = QdrantVectorStore(
            client=client,
            collection_name=COLLECTION_NAME,
            embedding=embedding_model
        )

        # Convert our existing chunks into LangChain Documents.
        documents = [
            Document(
                page_content=chunk["content"],
                metadata={
                    "chunk_id": chunk["chunk_id"],
                    "chunk_index": chunk["chunk_index"],
                    "customer_id": chunk["customer_id"],
                    "filename": chunk["filename"],
                    "document_type": chunk["document_type"],
                    "source_path": chunk["source_path"]
                }
            )
            for chunk in chunks
        ]

        document_ids = [
            str(uuid5(NAMESPACE_URL, chunk["chunk_id"]))
            for chunk in chunks
        ]

        print(f"Storing {len(documents)} documents in Qdrant...")

        vector_store.add_documents(
            documents=documents,
            ids=document_ids
        )

        stored_count = client.count(
            collection_name=COLLECTION_NAME,
            exact=True
        ).count

        if stored_count != len(documents):
            raise RuntimeError(
                f"Expected {len(documents)} vectors, "
                f"but found {stored_count}."
            )

        return {
            "collection": COLLECTION_NAME,
            "stored_count": stored_count,
            "vector_dimensions": VECTOR_SIZE,
            "database_path": QDRANT_PATH
        }

    finally:
        client.close()


def open_vector_store():
    """Open an existing Qdrant collection for retrieval."""

    client = QdrantClient(path=QDRANT_PATH)

    if not client.collection_exists(COLLECTION_NAME):
        client.close()
        raise RuntimeError("Qdrant collection does not exist.")

    vector_store = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=get_embedding_model()
    )

    return vector_store, client


if __name__ == "__main__":
    result = build_vector_store()

    print("\n========== QDRANT INGESTION RESULTS ==========")
    for key, value in result.items():
        print(f"{key}: {value}")

    print("\nQDRANT VECTOR STORAGE SUCCESSFUL!")
