class NotificationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    def get_queryset(self):
        """
        Return notifications for the requesting user only
        (i.e. notifications where the user is in inapp_recipients).
        """

    @action(detail=False, methods=["get", "put"], url_path="preferences")
    def preferences(self, request):
        """
        GET: List all notification preferences for the current user.
        PUT: Update notification preferences (expects a list of preferences).
        """


class NotificationPreferenceDetailView(APIView):
    """
    View for updating a single notification preference.
    """


class SystemAlertViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Read-only endpoint returning active, non-expired system alerts."""
