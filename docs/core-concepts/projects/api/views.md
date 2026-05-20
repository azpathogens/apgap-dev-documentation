
class ProjectViewSet(
    ProjectQuerysetMixin,
    DetermineProjectSerializerMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.UpdateModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    A ViewSet for creating and retrieving Projects.
    Users must be in the project hierarchy (global perms, lab member, or project member) to view projects.
    """

    def get_permissions(self):
        """
        Override get_permissions to ensure we use the filtered queryset for permission checks.
        """

    def get_queryset(self):
        """
        Filter projects that the user has access to view.
        Returns only the projects the user has permission to see based
        on their global, lab, and project permissions.
        """

    def get_object(self):
        """
        Override get_object to ensure archived projects are accessible for archive/hard-delete actions.
        For archive and hard-delete actions, we need to access projects even if they're archived.
        """

    @action(detail=False, methods=["get"], url_path="permission-groups")
    def permission_groups(self, request):
        """
        Return the list of valid permission groups for projects.
        Excludes the Platform Admin and Lab Director groups.
        """

    @action(detail=False, methods=["get"], url_path="manage-access-project-list")
    def manage_access_project_list(self, request):
        """
        Return all projecfts in the system.
        Specifically for Lab Directors to manage access to projects.
        """

    def _get_output_bucket(self, project):
        """Get the Seqera output bucket, returning empty string on any error."""

    @action(detail=True, methods=["get"], url_path="resource-detail")
    def resource_detail(self, request, pk=None):
        """
        Return the detailed information for a project, including users, datasets, and Seqera links.
        """

    @action(detail=True, methods=["get"], url_path="build-status")
    def build_status(self, request, pk=None):
        """
        Return the Cloud Build status for the given project.
        """

    @action(detail=True, methods=["get"], url_path="build-log")
    def build_log(self, request, pk=None):
        """
        Return the most recent captured GCP/Cloud Build provisioning error
        for the given project. Empty string when there is no recorded error.
        """

    @action(
        detail=True,
        methods=["post"],
        url_path="archive",
        permission_classes=[permissions.IsAuthenticated, CanArchiveProject],
    )
    def archive(self, request, pk=None):
        """
        Archive a project (Lab Director only).

        This action:
        - Updates the project status to ARCHIVED
        - Deletes all analytical datasets
        - Triggers cleanup of GCP resources and Seqera workspace (async)
        - Project remains visible in the list but with ARCHIVED status
        """

    @action(
        detail=True,
        methods=["post"],
        url_path="hard-delete",
        permission_classes=[permissions.IsAuthenticated, CanHardDeleteProject],
    )
    def hard_delete(self, request, pk=None):
        """
        Hard delete a project (Platform Administrator only).

        This action:
        - Requires deletion_justification in request body
        - Deletes all analytical datasets
        - Triggers cleanup of GCP resources and Seqera workspace (async)
        - Permanently removes the project from the database
        """


class ProjectUserViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        """
        Add the user to the lab as a lab collaborator if they aren't already in the lab.

        Assignment restrictions stay in ``ProjectUserCreateSerializer`` so validation
        messages are produced consistently by DRF serializers.
        """

    def _get_optimized_queryset(self, queryset):
        """
        Apply select_related and prefetch_related optimizations to reduce N+1 queries.
        """

    def get_queryset(self):
        """
        Filter project users that the user has access to view.
        Returns only the project users that the user has permission to see based
        on their global permissions, lab membership, or project membership.
        """
