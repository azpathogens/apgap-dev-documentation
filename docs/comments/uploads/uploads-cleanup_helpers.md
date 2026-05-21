"""
Helper functions for cleaning up GCP resources associated with batch uploads.
"""


def delete_gcs_bucket(bucket_name: str) -> bool:
    """
    Delete a GCS bucket.

    Args:
        bucket_name: The name of the bucket to delete

    Returns:
        bool: True if successful, False otherwise
    """


def delete_secret(secret_name: str) -> bool:
    """
    Delete a secret from GCP Secret Manager.

    Args:
        secret_name: The full resource name of the secret to delete

    Returns:
        bool: True if successful, False otherwise
    """


def delete_service_account_keys(service_account_email: str) -> bool:
    """
    Delete all keys for a service account.

    Args:
        service_account_email: The email address of the service account to delete

    Returns:
        bool: True if successful, False otherwise
    """


def delete_service_account(service_account_email: str) -> bool:
    """
    Delete a GCP service account.

    Args:
        service_account_email: The email address of the service account to delete

    Returns:
        bool: True if successful, False otherwise
    """
