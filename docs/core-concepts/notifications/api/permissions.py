"""
Permission classes for notification API endpoints.
"""


class NotificationPermission(permissions.BasePermission):
    """
    Permission class for notification operations.

    Permissions:
    - List/Retrieve: All authenticated users (their own notifications)
    - Update preferences: All authenticated users (their own preferences)
    """

    def has_permission(self, request, view):
        """
        Check if user has permission to perform the action.
        All authenticated users can access their own notifications.
        """

        # For APIView (NotificationPreferenceDetailView), check request method
        # For ViewSet (NotificationViewSet), check action

    def has_object_permission(self, request, view, obj):
        """
        Check if user has permission to perform the action on a specific notification.
        Users can only access their own notifications.
        """
