class NotificationType(models.TextChoices):
    """Enum of all notification types in the system."""

    # User notifications
    WELCOME = "welcome", "Welcome Message"
    USER_CREATED = "user_created", "New User Created"
    USER_UPDATED = "user_updated", "User Profile Updated"
    USER_DELETED = "user_deleted", "User Deleted"

    # Lab notifications
    LAB_CREATED = "lab_created", "Lab Created"
    LAB_USER_ADDED = "lab_user_added", "Added to Lab"

    # Project notifications
    PROJECT_CREATED = "project_created", "Project Created"
    PROJECT_ARCHIVED = "project_archived", "Project Archived"
    PROJECT_DELETED = "project_deleted", "Project Deleted"
    PROJECT_USER_ADDED = "project_user_added", "Added to Project"

    # File notifications
    FILE_UPLOADED = "file_uploaded", "File Uploaded"
    FILE_PII_DETECTED = "file_pii_detected", "File PII Detected"
    FILE_FAILED = "file_failed", "File Processing Failed"
    FILE_DELETED = "file_deleted", "File Deleted"

    # Dataset notifications
    DATASET_CREATED = "dataset_created", "Dataset Created"
    DATASET_FILE_STATUS = "dataset_file_status", "Dataset File Status Changed"

    # Access & Archive notifications
    ACCESS_REQUEST = "access_request", "Access Request"
    ACCESS_REQUEST_APPROVED = "access_request_approved", "Access Request Approved"
    ACCESS_REQUEST_DENIED = "access_request_denied", "Access Request Denied"
    ARCHIVE_REQUEST = "archive_request", "Archive Request"


class NotificationAudience(models.TextChoices):
    """Defines which users can potentially receive a notification type."""

    ALL_USERS = "all_users", "All Users"
    PLATFORM_ADMIN = "platform_admin", "Platform Admins Only"
    LAB_MEMBER = "lab_member", "Lab Members (Directors & Readers)"
    LAB_DIRECTOR = "lab_director", "Lab Directors Only"


# Mapping of notification types to their potential audience
# This determines which preferences are shown to which users
# Note: WELCOME is excluded because it's sent at account creation before users can set preferences

class UserNotificationPreference(models.Model):
    """
    Stores user preferences for notification types.

    Preferences are created on-demand when a user explicitly changes a setting.
    Missing preferences are treated as enabled (default behavior).
    """

    def get_applicable_notification_types(cls, user):
        """
        Get notification types applicable to this user based on their roles.

        Returns a list of NotificationType values that the user could potentially receive.
        """

    def get_user_preferences(cls, user):
        """
        Get all applicable notification preferences for a user.

        Returns a list of dicts with notification type info and current preference status.
        Missing preferences default to enabled.
        In-app notifications are always enabled and cannot be opted out.
        """

    @classmethod
    def is_email_enabled_for_user(cls, user, notification):
        """Check if email is enabled for a user and notification type."""


class SystemAlertManager(models.Manager):
    def active(self):
        """Return alerts that are active and not expired."""


class SystemAlert(models.Model):
    """
    Platform-wide system alerts created by admins via Django admin.
    Displayed to all authenticated users as dismissable popups.
    """
