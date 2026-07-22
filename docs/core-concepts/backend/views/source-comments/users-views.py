

class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by("name", "email")

    def get_queryset(self):
        """
        Return optimized queryset based on the action.
        - For list: prefetch organization
        - For detail/me: prefetch groups, lab_memberships, project_memberships
        """
    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """
        Return the authenticated user's details.
        Uses prefetched queryset to avoid N+1 queries.
        """

    @action(
        detail=False,
        methods=["get", "post"],
        url_path="orientation",
        permission_classes=[permissions.IsAuthenticated],
    )
    def orientation(self, request):
        """GET returns the current orientation flag, POST flips it to True (idempotent)."""
    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated, UserManagementPermission])
    def reactivate(self, request, pk=None):
        """
        Reactivate a deactivated user by:
        - Setting is_active to True
        - Removing "(Deleted)" suffix from name
        - Recording who reactivated the user

        If user is already active, no action is taken.
        """

    def perform_destroy(self, instance):
        """
        Mark the user as deleted by setting the deleted_by field,
        appending "(Deleted)" to the last name (or name field if last_name is missing),
        and disabling the account.

        Also removes the user's lab associations, project associations, and roles.
        The user is not actually deleted from the database.
        """
