"""
Celery task for cleaning up expired batch uploads.
"""


@shared_task
def cleanup_expired_batch_uploads():
    """
    Periodic task to clean up expired batch uploads.

    This task runs hourly and:
    1. Finds all BatchUpload objects where is_expired is True AND
       batch_service_account_secret_name is not empty
    2. For each BatchUpload found:
       - Deletes the GCS bucket defined in ingest_bucket
       - Deletes the service account key secret defined by batch_service_account_secret_name
       - NOTE: Service accounts are NOT deleted as they may be reused
    3. After successful cleanup, sets batch_service_account_secret_name to empty string

    Returns:
        dict: Summary of cleanup results
    """

    # NOTE: Service accounts are NOT deleted as they may be reused or managed separately

    # Update the batch upload record to clear the secret name
    # Do this even if some cleanup steps failed, to avoid retrying indefinitely
