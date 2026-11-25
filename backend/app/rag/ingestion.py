from backend.app.rag.document_loader import load_documents
from backend.app.rag.chunking import split_text


def ingest_documents():

    documents = load_documents()

    all_chunks = []

    for document in documents:

        chunks = split_text(document["content"])

        for index, chunk in enumerate(chunks):

            all_chunks.append({
                "chunk_id": (
                    f"{document['customer_id']}_"
                    f"{document['document_type']}_{index}"
                ),
                "chunk_index": index,
                "customer_id": document["customer_id"],
                "filename": document["filename"],
                "document_type": document["document_type"],
                "source_path": document["source_path"],
                "content": chunk
            })

    return all_chunks
