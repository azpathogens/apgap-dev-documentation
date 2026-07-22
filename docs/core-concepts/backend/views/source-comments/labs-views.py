
class LabViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    DetermineLabSerializerMixin,
    viewsets.GenericViewSet,
):
    def get_queryset(self):
        """
        Filter labs that the user has access to view.
        Returns only the labs the user has permission to see based
        on their global permissions, lab membership, or project membership.
        """
        # Use the custom manager to get filtered queryset
        # Add select_related for organization to avoid N+1 queries in serializer

    @action(detail=True, methods=["get"], url_path="build-log")
    def build_log(self, request, pk=None):
        """
        Return the most recent captured GCP/Cloud Build provisioning error
        for the given lab. Empty string when there is no recorded error.
        """

    @action(detail=True, methods=["get"], url_path="project-users")
    def project_users(self, request, pk=None):
        """
        Return a list of users and their project assignments for a given lab.
        """

    @action(detail=True, methods=["post"], url_path="assign-user")
    def assign_user(self, request, pk=None):
        """
        Assign a user to a lab using AssignUserToLabSerializer.
        """

    @action(detail=True, methods=["get"], url_path="members")
    def members(self, request, pk=None):
        """
        Return **all** lab members:
          • lab_users  directors & regular lab members
          • project_users users assigned to projects in the lab
        Directors are removed from project_users to avoid duplicates.
        """

    @action(detail=True, methods=["post"], url_path="remove-user")
    def remove_user(self, request, pk=None):
        """
        Remove a user from a lab.
        Only lab directors for that lab, superusers, and platform admins can do this.
        Permission is checked by LabHierarchicalPermission.

        Lab collaborators who are bioinformatics users in projects within the lab cannot be removed.
        Lab directors can always be removed regardless of project assignments.
        When a lab director is removed, all their project assignments in that lab are automatically deleted.
        """

        # Only check for bioinformatics users in projects if the user is a lab collaborator
        # Lab directors can always be removed regardless of project assignments
        is_lab_director = lab_user.is_lab_admin or lab_user.permission_group.name == PermissionGroups.LAB_DIRECTOR.value

    @action(
        detail=True,
        methods=["delete"],
        url_path="delete-failed",
        permission_classes=[permissions.IsAuthenticated, CanDeleteFailedLab],
    )
    def delete_failed(self, request, pk=None):
        """
        Delete a lab whose GCP build has failed.

        Only labs with build_status FAILURE, TIMEOUT, or CANCELLED can be deleted.
        Triggers GCP resource cleanup via Cloud Build destroy trigger, then removes
        the lab and its associated LabUser records from the database.
        """
