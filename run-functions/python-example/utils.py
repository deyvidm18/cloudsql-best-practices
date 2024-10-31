from google.cloud import secretmanager
import os

def access_secret_version(secret_name: str, version_id: str = "latest") -> str:
    """
    Accesses the payload for the given secret version if one exists.
    The version can be a version number as a string (e.g. "5")
    or an alias (e.g. "latest").
    """

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{os.environ['PROJECT_ID']}/secrets/{secret_name}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})

    # Return the decoded payload.
    return response.payload.data.decode("UTF-8")