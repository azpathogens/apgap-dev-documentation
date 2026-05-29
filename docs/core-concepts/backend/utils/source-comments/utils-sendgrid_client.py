def send_notification_email(notification):
    """
    Send email notification to all email_recipients.

    The email_recipients field should already contain only users who have
    enabled email notifications for this notification type. No additional
    preference filtering is done here.

    If the notification has a csv_attachment, it will be attached to the email.
    """
