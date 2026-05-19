"""
Permission classes for user management API endpoints.
"""


class UserManagementPermission(permissions.BasePermission):
    """
    Permission class for user management operations.

    Permissions:
    - Create: Platform Admin only
    - List/Retrieve: Platform Admin, Lab Director (for their lab users), Bioinformatics User (for their project users)
    - Update: Platform Admin only
    - Delete (soft): Platform Admin only
    - Reactivate: Platform Admin only
    """

    def has_permission(self, request, view):
        """
        Check if user has permission to perform the action.
        """

    def has_object_permission(self, request, view, obj):  # noqa: PLR0911
        """
        Check if user has permission to perform the action on a specific user.
        """
