
from pathlib import Path


DOCUMENTS_DIR = Path(
    "/opt/glue-assist-ai/data/documents"
)


def load_documents():

    documents = []

    for file_path in DOCUMENTS_DIR.rglob("*.txt"):

        filename = file_path.name.lower()

        # Ignore README files
        if filename.startswith("readme"):
            continue

        # Identify document type
        if "ticket_process" in filename:
            document_type = "ticket_process"

        elif "patch_process" in filename:
            document_type = "patch_process"

        else:
            continue

        # Extract customer ID from filename
        customer_id = filename.split("_")

        if len(customer_id) < 4:
            continue

        customer_id = "_".join(customer_id[1:-2])

        content = file_path.read_text(encoding="utf-8")

        if not content.strip():
            continue

        documents.append({
            "customer_id": customer_id,
            "filename": file_path.name,
            "document_type": document_type,
            "source_path": str(file_path),
            "content": content
        })

    return documents
