@receiver(m2m_changed, sender=AccessRequest.approvers.through)
def notify_approvers_of_new_access_request(sender, instance, action, pk_set, **kwargs):
    """
    Notify approvers (lab directors) when they are assigned to a new access request.

    This notifies the approvers that a user has requested access to a file
    in an analytical dataset and needs their approval.

    Uses m2m_changed signal to ensure approvers are added before sending notification.
    """
    # Only process after approvers are added (post_add)

    # Skip if the request is not PENDING (e.g., auto-approved)

    # Skip if no approvers were added

    # Check if a notification for this access request already exists
    # (avoid duplicate notifications if approvers are added in batches)

    # Get all approvers for this request

    # Filter by preferences

    # Create notification


@receiver(post_save, sender=AccessRequest)
def check_dataset_approval_status(sender, instance, created, **kwargs):
    """
    Signal to check analytical dataset approval status.
    - If any request is REJECTED, mark dataset as DENIED and notify requester.
    - If all files are APPROVED, mark dataset as APPROVED and notify requester.
    """
    user = instance.user
    dataset = instance.analytical_dataset

    # Case 1: Request Rejected -> Deny Dataset

    # Update dataset approval status

    # Filter by preferences

    # Create notification for rejection

    # Case 2: Request Approved -> Check if ALL are approved, then copy files


def _copy_file_if_not_exists(access_request):
    """
    Copy the file from an approved access request to the analytical dataset.

    Only copies if the file hasn't been copied yet.

    Args:
        access_request: The approved AccessRequest instance
    """
