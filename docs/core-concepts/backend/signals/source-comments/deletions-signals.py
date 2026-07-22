"""
Signal handlers for archive request notifications.
"""


@receiver(post_save, sender=ArchiveRequest)
def notify_archive_request_status_change(sender, instance, created, **kwargs):
    """
    Send notifications for archive request status changes.

    - On creation: Notify Lab Directors that a new archive request needs review
    - On approval: Notify the requester that their request was approved
    - On denial: Notify the requester that their request was denied
    """


def _get_file_from_archive_request(archive_request):
    """
    Get the File object from an archive request.
    Returns None if the archive request is not for a File.
    """


def _notify_lab_directors_of_new_request(archive_request):
    """
    Notify Lab Directors and Platform Admins when a new archive request is submitted for their lab.
    """


def _notify_requester_of_approval(archive_request):
    """
    Notify the requester when their archive request is approved.
    """


def _notify_requester_of_denial(archive_request):
    """
    Notify the requester when their archive request is denied.
    """
