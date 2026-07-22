"""Utility functions for notifications."""


def filter_recipients_by_preferences(all_recipients, notification_type):
    """
    Filter recipients by their notification preferences.

    Args:
        all_recipients: A list or set of User objects to filter
        notification_type: A NotificationType value

    Returns:
        A tuple of (email_recipients, inapp_recipients), where each is a list
        of User objects filtered by their notification preferences.
        In-app notifications are always enabled for all recipients.
    """
