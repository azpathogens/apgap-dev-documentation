

class FileHierarchicalPermission(permissions.BasePermission):
    """
    Permission class that checks if the user has permissions at any level:
    1. Global - Direct user permissions
    2. Lab level - Via lab membership
    3. Project level - Via project membership in a lab
    4. Creator level - User created the file

    Maps REST actions to Django permission codenames:
    - GET (list/retrieve) -> view_file
    - POST (create) -> add_file
    - PUT/PATCH (update) -> change_file
    - DELETE (destroy) -> delete_file

    - PRIMARY sequences can only be deleted by Platform Admins
    """

    def has_permission(self, request, view):
        """
        Check if user has permission to perform the action at any level.
        """

    def has_object_permission(self, request, view, obj):
        """
        Check if user has permission to perform the action on a specific file.
        """

    def _log_object_permission_check(self, request, view, obj):
        """Log debug information for object permission check."""

    def _check_destroy_permission(self, request, obj):
        """Check if user has permission to destroy the file."""

    def _check_general_permission(self, request, obj, permission_codename):
        """Check general (non-destroy) permissions for file access."""

    def _check_lab_permission(self, lab_user, permission_codename, user, obj):
        """Check if lab user has the required permission."""

    def _check_project_permission(self, user, obj, project_model, project_user_model):
        """Check if user has project-level permission to view the file."""
