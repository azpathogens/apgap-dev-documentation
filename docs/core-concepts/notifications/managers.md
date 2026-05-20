from django.db import models


class NotificationManager(models.Manager):

    def for_user(self, user):
        """
        Returns notifications that are assigned to the specified user for in-app display,
        ordered from most recent to least recent.

        The inapp_recipients field already contains only users who have enabled
        in-app notifications for this notification type, so no additional filtering
        is needed.

        Args:
            user: The user to get notifications for
        """
