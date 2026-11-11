
import os

from google.cloud import secretmanager


def get_secret(secret_id: str) -> str:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        raise RuntimeError("Google Cloud project ID is not configured")

    client = secretmanager.SecretManagerServiceClient()

    secret_name = (
        f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    )

    response = client.access_secret_version(
        request={"name": secret_name}
    )

    return response.payload.data.decode("UTF-8")
