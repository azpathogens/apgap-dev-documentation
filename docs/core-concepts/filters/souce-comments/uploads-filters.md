class UploadFilter(django_filters.FilterSet):
    """
    Filter class for Upload model.
    Provides filtering by lab, user, status, and other fields.
    """

    def filter_by_lab_names(self, queryset, name, value):
        """Filter by lab display names (supports multiple values via repeated parameters)."""

    def filter_by_user_emails(self, queryset, name, value):
        """Filter by user emails (supports multiple values via repeated parameters)."""


class BatchUploadFilter(django_filters.FilterSet):
    """
    Filter class for BatchUpload model.
    Provides filtering by lab, user, and other fields.
    """

    def filter_has_uploads(self, queryset, name, value):
        """Custom filter method to check if batch has uploads."""

    def filter_by_lab_names(self, queryset, name, value):
        """Filter by lab display names (supports multiple values via repeated parameters)."""

    def filter_by_user_emails(self, queryset, name, value):
        """Filter by user emails (supports multiple values via repeated parameters)."""
