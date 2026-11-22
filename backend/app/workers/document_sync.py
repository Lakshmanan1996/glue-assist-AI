
import hashlib
import json

from pathlib import Path


DOCUMENTS_DIR = Path(
    "/opt/glue-assist-ai/data/documents"
)

STATE_FILE = Path(
    "/opt/glue-assist-ai/data/processed/document_state.json"
)


def calculate_file_hash(file_path: Path) -> str:

    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:

        for block in iter(lambda: file.read(65536), b""):
            sha256.update(block)

    return sha256.hexdigest()


def load_previous_state() -> dict:

    if not STATE_FILE.exists():
        return {}

    with STATE_FILE.open("r", encoding="utf-8") as file:
        state = json.load(file)

    if not isinstance(state, dict):
        raise ValueError("Document state must be a JSON object")

    return state


def scan_documents() -> dict:

    previous_state = load_previous_state()

    current_state = {}

    new_files = []
    modified_files = []
    unchanged_files = []

    for file_path in DOCUMENTS_DIR.rglob("*.txt"):

        filename = file_path.name.lower()

        # Ignore README files
        if filename.startswith("readme"):
            continue

        # Only process supported document types
        if (
            "ticket_process" not in filename
            and "patch_process" not in filename
        ):
            continue

        file_hash = calculate_file_hash(file_path)

        relative_path = str(
            file_path.relative_to(DOCUMENTS_DIR)
        )

        current_state[relative_path] = file_hash

        if relative_path not in previous_state:

            new_files.append(relative_path)

        elif previous_state[relative_path] != file_hash:

            modified_files.append(relative_path)

        else:

            unchanged_files.append(relative_path)

    deleted_files = sorted(
        set(previous_state) - set(current_state)
    )

    return {
        "new": sorted(new_files),
        "modified": sorted(modified_files),
        "unchanged": sorted(unchanged_files),
        "deleted": deleted_files,
        "current_state": current_state
    }


def save_current_state(current_state: dict):

    STATE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    temporary_file = STATE_FILE.with_suffix(".tmp")

    with temporary_file.open("w", encoding="utf-8") as file:

        json.dump(current_state, file, indent=4)

    temporary_file.replace(STATE_FILE)
