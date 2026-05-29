"""
Permission classes for upload API endpoints.
"""


class UploadPermission(permissions.BasePermission):
    """
    Permission class for upload operations.

    Permissions:
    - Create: Platform Admin, Lab Director, Lab Collaborator
    - List/Retrieve: Platform Admin, Lab Director, Lab Collaborator,
      Bioinformatics User (for uploads in their project labs)
    - Update: Platform Admin, Lab Director, Lab Collaborator (for their own uploads)
    - Delete: Platform Admin, Lab Director, Lab Collaborator (for their own uploads)
    """

    def has_permission(self, request, view):  # noqa: PLR0911
        """
        Check if user has permission to perform the action.
        """

    def has_object_permission(self, request, view, obj):
        """
        Check if user has permission to perform the action on a specific upload.
        """


class BatchUploadPermission(permissions.BasePermission):
    """
    Permission class for batch upload operations.

    Permissions:
    - Create: Platform Admin, Lab Director, Lab Collaborator
    - List/Retrieve: Platform Admin, Lab Director, Lab Collaborator,
      Bioinformatics User (for uploads in their project labs)
    - Update: Platform Admin, Lab Director, Lab Collaborator (for their own uploads)
    - Delete: Platform Admin, Lab Director, Lab Collaborator (for their own uploads)
    """

    def has_permission(self, request, view):  # noqa: PLR0911
        """
        Check if user has permission to perform the action.
        """

    def has_object_permission(self, request, view, obj):
        """
        Check if user has permission to perform the action on a specific batch upload.
        """
