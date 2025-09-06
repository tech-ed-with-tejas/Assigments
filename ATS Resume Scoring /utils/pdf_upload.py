import os
from google.cloud import storage
from google.api_core.exceptions import GoogleAPIError
import os
APP_ENV = os.getenv("APP_ENV", "local")  # local | production


def upload_pdf_to_gcs(
    bucket_name: str,
    source_file_path: str,
    destination_blob_name: str,
    content_type: str = "application/pdf",
    credentials_json_path: str | None = None,
) -> str:
    """
    Uploads a local PDF to a Google Cloud Storage bucket.

    Args:
        bucket_name: Name of the target GCS bucket.
        source_file_path: Local path to the PDF file (e.g., "./resume.pdf").
        destination_blob_name: Path/name in the bucket (e.g., "resumes/user123/resume.pdf").
        content_type: MIME type for the upload; default is "application/pdf".
        credentials_json_path: Optional path to a service account JSON. If None, uses ADC.

    Returns:
        Publicly accessible URL (if bucket/object ACLs allow), or the gs:// URL.
    """
    if not os.path.isfile(source_file_path):
        raise FileNotFoundError(f"Local file not found: {source_file_path}")

    try:
        # Initialize client (uses ADC if credentials_json_path is None)
        if APP_ENV == "production":
            client = storage.Client()
        else:
            credentials_json_path ="./scrects/winter-charmer-381409-387275a6cdee.json"
            if credentials_json_path:
                client = storage.Client.from_service_account_json(credentials_json_path)
            else:
                raise ValueError("In local environment, credentials_json_path must be provided.")


        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        # Upload with proper content type
        blob.upload_from_filename(source_file_path, content_type=content_type)

        # Optional: set cache-control or metadata
        # blob.cache_control = "private, max-age=0, no-transform"
        # blob.patch()

        # Return the gs:// URL by default
        return f"gs://{bucket_name}/{destination_blob_name}"

    except GoogleAPIError as e:
        raise RuntimeError(f"GCS API error: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error uploading to GCS: {e}") from e


if __name__ == "__main__":
    # Example usage
    BUCKET_NAME = "atsresumes"
    LOCAL_PDF = "/Users/tejasa/Desktop/Tejas/Assigments/ATS Resume Scoring /sampledata/1.pdf"
    DEST_PATH = "user_abc/resume.pdf"

    # If using explicit credentials:
    # CREDS = "/path/to/service_account.json"
    CREDS = None  # rely on GOOGLE_APPLICATION_CREDENTIALS or workload identity

    url = upload_pdf_to_gcs(
        bucket_name=BUCKET_NAME,
        source_file_path=LOCAL_PDF,
        destination_blob_name=DEST_PATH,
        credentials_json_path=CREDS,
    )
    print("Uploaded to:", url)
