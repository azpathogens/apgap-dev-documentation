def get_platform_admin_users():
    """Helper function to get all platform admin users."""


@receiver(post_save, sender="users.User")
def notify_platform_admins_of_user_creation(sender, instance, created, **kwargs):
    """Create a notification when a new user is created."""


@receiver(post_delete, sender="users.User")
def notify_platform_admins_of_user_deletion(sender, instance, **kwargs):
    """
    Create a notification when a user is deleted.

    Note: The content_type and object_id are stored for consistency, but since
    this is a post_delete signal, the user no longer exists in the database.
    The content_object will return null when the notification is serialized.
    """


def _check_soft_deletion(instance):
    """
    Helper function to check if a user is being soft deleted.
    Returns (is_soft_deletion, previous_user) tuple.
    """

    # Check if this is a soft deletion
    # Soft deletion is detected when:
    # 1. deleted_by changes from None to a value, OR
    # 2. is_active changes from True to False (and user wasn't already deleted)


@receiver(pre_save, sender=User)
def detect_soft_deletion(sender, instance, **kwargs):
    """Detect soft deletion and set a flag on the instance."""


@receiver(post_save, sender="users.User")
def notify_user_soft_deleted(sender, instance, created, **kwargs):
    """Create a notification when a user is soft deleted."""
