"""
Service functions for deletion and archive operations.
"""


def process_archive_approval(archive_request_id: int, reviewed_by_user) -> None:
    """
    Process an approved archive request.

    This function:
    1. Updates the archive request status to APPROVED
    2. Deletes the GCS blob (if it exists and GCP interactions are enabled)
    3. Updates the File status to ARCHIVED with archive metadata
    4. Creates a Deletion record for audit trail

    Args:
        archive_request_id: ID of the archive request to process
        reviewed_by_user: User who approved the request

    Raises:
        ArchiveRequest.DoesNotExist: If the archive request doesn't exist
        ValueError: If the request is not for a File or is not pending
        Exception: If GCS blob deletion fails
    """
