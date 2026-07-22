@receiver(m2m_changed, sender=Notification.email_recipients.through)
def handle_email_recipients_changed(sender, instance, action, **kwargs):
    """
    Trigger email sending when email_recipients are added to a notification.

    The email_recipients field should already contain only users who have
    enabled email notifications for this notification type.
    """
