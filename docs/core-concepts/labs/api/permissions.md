class LabHierarchicalPermission(permissions.BasePermission):
    """
    Permission class that checks if the user has permissions at any level:
    1. Global - Direct user permissions
    2. Lab level - Via lab membership
    3. Project level - Via project membership in a lab

    Maps REST actions to Django permission codenames:
    - GET (list/retrieve) -> view_lab
    - POST (create) -> add_lab
    - PUT/PATCH (update) -> change_lab
    - DELETE (destroy) -> delete_lab
    """

    def has_permission(self, request, view):  # noqa: PLR0911
        """
        Check if user has permission to perform the action at any level.
        """

    def _check_remove_user_permission(self, request, obj):
        """Check if user has permission to remove users from a lab."""

    def _check_lab_level_permission(self, request, view, obj, permission_codename, lab_user):
        """Check if user has lab-level permission."""

    def _check_project_level_permission(self, request, obj):
        """Check if user has project-level permission to view the lab."""

    def has_object_permission(self, request, view, obj):  # noqa: PLR0911
        """
        Check if user has permission to perform the action on a specific lab.
        """


class CanDeleteFailedLab(permissions.BasePermission):
    """
    Only Platform Administrators can delete failed labs.
    """
