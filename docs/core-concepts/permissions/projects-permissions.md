
class ProjectHierarchicalPermission(permissions.BasePermission):
    """
    Permission class that checks if the user has permissions at any level:
    1. Global - Direct user permissions
    2. Lab level - Via lab membership
    3. Project level - Via project membership

    Maps REST actions to Django permission codenames:
    - GET (list/retrieve) -> view_project
    - POST (create) -> add_project
    - PUT/PATCH (update) -> change_project
    - DELETE (destroy) -> delete_project
    """

    def _check_lab_permission(self, user, lab, permission_codename):
        """Check if user has the required permission via LabUser membership."""

    def _check_project_permission(self, user, project, permission_codename):
        """Check if user has the required permission via ProjectUser membership."""

    def has_object_permission(self, request, view, obj):


class ProjectUserHierarchicalPermission(permissions.BasePermission):
    """
    Permission class that checks if the user has permissions at any level:
    1. Global - Direct user permissions
    2. Lab level - Via lab membership
    3. Project level - Via project membership

    Maps REST actions to Django permission codenames:
    - GET (list/retrieve) -> view_projectuser
    - POST (create) -> add_projectuser
    - PUT/PATCH (update) -> change_projectuser
    - DELETE (destroy) -> delete_projectuser
    """

    def has_permission(self, request, view):  # noqa: PLR0911
        """
        Check if user has permission to perform the action at any level.
        """

    def has_object_permission(self, request, view, obj):
        """
        Check if user has permission to perform the action on a specific project user.
        """


class CanArchiveProject(permissions.BasePermission):
    """
    Permission class that allows users with archive_project permission to archive projects.

    This permission is assigned to:
    - Lab Directors (via their permission group)
    - Platform Administrators (via their permission group)
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if user can archive this project.

        Users must have the 'projects.archive_project' permission, which is granted to
        Lab Directors and Platform Administrators via their permission groups.
        """


class CanHardDeleteProject(permissions.BasePermission):
    """
    Permission class that allows users with hard_delete_project permission to hard delete projects.

    This permission is assigned to:
    - Platform Administrators (via their permission group)
    """

    def has_permission(self, request, view):
        """
        Check if user can hard delete projects.

        Users must have the 'projects.hard_delete_project' permission, which is granted to
        Platform Administrators via their permission group.
        """

    def has_object_permission(self, request, view, obj):
        """
        Check if user can hard delete this specific project.

        Users must have the 'projects.hard_delete_project' permission, which is granted to
        Platform Administrators via their permission group.
        """
