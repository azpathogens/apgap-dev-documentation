

@shared_task
def trigger_dlp_scan(file_id):
    """
    Trigger DLP scan for the given file ID.

    Args:
        file_id: The ID of the File object to scan

    Returns:
        str: Status message or None if failed
    """


@shared_task
def batch_dlp_scan(lab_id, file_ids=None):
    """
    Trigger DLP scans for multiple files in a lab.

    Args:
        lab_id: The ID of the lab
        file_ids: Optional list of specific file IDs to scan.
                 If None, scans all PROCESSING files in the lab.

    Returns:
        dict: Summary of scan results
    """


@shared_task
def cleanup_stuck_files(lab_id=None, older_than_hours=8):
    """
    Set files that are stuck in PROCESSING state for too long to FAILED.

    Args:
        lab_id: Optional lab ID to limit cleanup to specific lab
        older_than_hours: Only clean up files older than this many hours

    Returns:
        dict: Summary of cleanup results
    """
