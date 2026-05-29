

class OptionalPageNumberPagination(PageNumberPagination):
    """
    Pagination class that only activates when the 'pagination' query parameter is present.
    When pagination is enabled, use 'page' parameter to specify the page number.
    Example: ?pagination=true&page=2
    """


class DatasetViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    A ViewSet for creating and retrieving Datasets.
    List and retrieve actions only require authentication.
    Create, update, and delete actions require hierarchical permissions.
    """

    def get_permissions(self):
        """
        Return the appropriate permission classes based on the action.
        List and retrieve only require authentication.
        Other actions require hierarchical permissions.
        """
        # All other actions, including custom actions, require hierarchical permissions

    @action(detail=True, methods=["post"], url_path="project-assignments")
    def project_assignments(self, request, pk=None):
        """
        Assign a project to a dataset.
        Requires:
        - change_dataset permission for the dataset (direct or through project/lab
          membership with appropriate permissions)
        """

    @action(detail=True, methods=["post"], url_path="request-access")
    def request_access(self, request, pk=None):
        """
        Request access to a dataset for a project.
        Creates a notification for the Lab Directors of the project.

        Required payload:
        {
            "project_id": <project_id>,
            "message": "<request message>"
        }
        """

        def format_requester_name(user):
            """Format the requester's name, handling None values gracefully."""

    def get_queryset(self):
        """
        Optionally filter datasets by metadata tags.

        Query parameters:
        - metadata_tags: List of metadata tag IDs to filter by
        - metadata_tag_match_partial: Boolean to determine AND/OR matching
            - True: Match datasets with ANY of the specified tags (OR)
            - False: Match datasets with ALL of the specified tags (AND)
        - owning_project: Filter by owning project ID
        - assigned_projects: Filter by assigned project ID
            If both owning_project and assigned_projects are provided, returns datasets
            that match either condition (OR match)
        """

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the action.
        """

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a dataset with detailed information.
        Uses DatasetDetailSerializer which accesses the model's all_files property.
        """

    def partial_update(self, request, *args, **kwargs):
        """
        Patch only the description of the dataset.
        """

    @action(detail=True, methods=["get"])
    def download_service_account_keyfile(self, request, pk=None):
        """
        Download the service account keyfile for a batch dataset.
        Returns the keyfile as a downloadable JSON file.
        Only works for batch datasets that have a service account.
        """

    @action(detail=True, methods=["get"])
    def blade_view(self, request, pk=None):
        """
        Provides detailed dataset information formatted for the blade view in the frontend.

        Returns:
            - Dataset name and description
            - Metadata key:value tags
            - File list preview (first 3 files)
            - Owning project (Lab Name/Project Name)
            - List of projects with access
            - Number of files
        """


class DatasetFileViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    A ViewSet for creating, retrieving, and updating DatasetFiles.
    Uses hierarchical permissions to check access at global, lab, and project levels.
    """

    def get_queryset(self):
        """
        Filter files by dataset if dataset_pk is provided in the URL.
        """

    def perform_create(self, serializer):
        """
        Set the dataset from the URL parameter when creating a new file.
        """

    def perform_update(self, serializer):
        """
        Set status to PROCESSING on any PATCH request.
        """


class BatchIngestNotificationViewSet(viewsets.ViewSet):
    """
    A ViewSet for handling pub/sub push notifications for batch ingest buckets.
    Triggers DLP scans for uploaded files.
    """

    permission_classes = []  # No additional permissions required since we verify the token

    def create(self, request, dataset_id=None):
        """
        Handle pub/sub push notifications for batch ingest bucket.
        Triggers DLP scan for the uploaded file.
        """
