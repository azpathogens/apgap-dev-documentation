from rest_framework import serializers

from asu_apgap.notifications.models import Notification
from asu_apgap.notifications.models import NotificationType
from asu_apgap.notifications.models import SystemAlert
from asu_apgap.notifications.models import UserNotificationPreference


class NotificationSerializer(serializers.ModelSerializer):
    content_object = serializers.SerializerMethodField()
    content_type_model = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            "id",
            "title",
            "status",
            "created_at",
            "details",
            "content_type",
            "content_type_model",
            "object_id",
            "notification",
            "content_object",
        ]

    def get_content_type_model(self, obj):
        """Return the model name for the content type."""
        if obj.content_type:
            return obj.content_type.model
        return None

    def get_content_object(self, obj):
        """
        Return a serialized representation of the related content object.
        Returns None if no content object exists or if the object was deleted.

        Note: This method has many branches due to handling different model types.
        The noqa comments suppress complexity warnings since refactoring would
        reduce readability without meaningful benefit.
        """

    def _serialize_content_object(self, model_name, content_obj):
        """Serialize content object based on its model type."""

    def _serialize_inline(self, model_name, content_obj):
        """Serialize models that don't have dedicated serializers."""


class NotificationPreferenceSerializer(serializers.Serializer):
    """
    Serializer for reading notification preferences.
    Returns all applicable notification types with their current status.
    In-app notifications are always enabled and are not included in this response.
    """


class NotificationPreferenceUpdateSerializer(serializers.Serializer):
    """
    Serializer for updating a single notification preference.
    Only email preferences can be updated; in-app notifications are always enabled.
    """
