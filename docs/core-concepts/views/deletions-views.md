

class OptionalPageNumberPagination(PageNumberPagination):
    """
    Only paginate if ?pagination=true is present.
    Otherwise return full list.
    """


class ArchiveRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing archive requests.

    Provides CRUD operations for archive requests with appropriate permissions:
    - Users can create archive requests for files they uploaded
    - Users can view their own archive requests
    - Lab Directors can view and approve/deny requests for their labs
    - Global admins can view and manage all archive requests

    Features:
    - Filtering by status, requested_by, content_type
    - Searching by justification, requester email
    - Optional pagination
    - Custom actions for approving and denying requests

    Only returns archive requests for files in active labs.
    """

    def get_serializer_class(self):
        """
        Return the appropriate serializer based on the action.
        """

    def get_queryset(self):
        """
        Filter archive requests to only those the user has access to view.
        Uses the User model's get_archive_requests() method for consistent permission filtering.
        """

    def perform_create(self, serializer):
        """
        Log archive request creation.
        """

    @action(detail=True, methods=["post"], url_path="approve")
    def approve(self, request, pk=None):
        """
        Approve an archive request.

        Only Lab Directors of the file's lab can approve requests.
        When approved, the GCS file is deleted and the File status is set to ARCHIVED.
        """

    @action(detail=True, methods=["post"], url_path="deny")
    def deny(self, request, pk=None):
        """
        Deny an archive request.

        Only Lab Directors of the file's lab can deny requests.
        """
    @action(detail=False, methods=["get"], url_path="my-requests")
    def my_requests(self, request):
        """
        Get all archive requests created by the current user.
        Only returns requests for files in active labs.
        """

    @action(detail=False, methods=["get"], url_path="pending-approvals")
    def pending_approvals(self, request):
        """
        Get all pending archive requests that the current user can approve.
        (Requests for files in active labs where user is a Lab Director)
        Only returns requests for files in active labs.
        """


class DeletionViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    ViewSet for viewing deletion records.
    Read-only access to deletion audit trail.
    """

    def get_serializer_class(self):
        """
        Use summary serializer for list view, full serializer for detail view.
        """

    def get_queryset(self):
        """
        Optionally filter deletions by date range.
        """
