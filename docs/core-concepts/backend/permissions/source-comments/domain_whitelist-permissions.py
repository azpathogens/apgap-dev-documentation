"""
Permission classes for domain whitelist API endpoints.
"""


class DomainWhitelistPermission(permissions.BasePermission):
    """
    Permission class for domain whitelist operations.

    Permissions:
    - Create: Platform Admin only
    - List/Retrieve: All authenticated users
    - Update: Platform Admin only
    - Delete: Platform Admin only
    """

    def has_permission(self, request, view):
        """
        Check if user has permission to perform the action.
        """

    def has_object_permission(self, request, view, obj):
        """
        Check if user has permission to perform the action on a specific domain whitelist entry.
        """
