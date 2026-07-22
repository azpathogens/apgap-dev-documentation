"""
Permission classes for metadata requirements API endpoints.
"""


class MetadataRequirementPermission(permissions.BasePermission):
    """
    Permission class for metadata requirement operations.

    Permissions:
    - Create: Platform Admin, Lab Director
    - List/Retrieve: Platform Admin, Lab Director, Lab Collaborator, Bioinformatics User
    - Update: Platform Admin, Lab Director
    - Delete: Platform Admin, Lab Director
    """

    def has_permission(self, request, view):
        """
        Check if user has permission to perform the action.
        """

    def has_object_permission(self, request, view, obj):
        """
        Check if user has permission to perform the action on a specific metadata requirement.
        """


class SourceTypePermission(permissions.BasePermission):
    """
    Permission class for source type operations.

    Permissions:
    - Create: Platform Admin, Lab Director
    - List/Retrieve: Platform Admin, Lab Director, Lab Collaborator, Bioinformatics User
    - Update: Platform Admin, Lab Director
    - Delete: Platform Admin, Lab Director
    """

    def has_permission(self, request, view):
        """
        Check if user has permission to perform the action.
        """

    def has_object_permission(self, request, view, obj):
        """
        Check if user has permission to perform the action on a specific source type.
        """


class MetadataTemplatePermission(permissions.BasePermission):
    """
    Permission class for metadata template operations.

    Permissions:
    - Create: Platform Admin, Lab Director
    - List/Retrieve: Platform Admin, Lab Director, Lab Collaborator, Bioinformatics User
    - Update: Platform Admin, Lab Director
    - Delete: Platform Admin, Lab Director
    """

    def has_permission(self, request, view):
        """
        Check if user has permission to perform the action.
        """

    def has_object_permission(self, request, view, obj):
        """
        Check if user has permission to perform the action on a specific metadata template.

        Note: MetadataTemplate does not have a 'lab' field — templates are global.
        Permission is governed by role alone (Platform Admin or Lab Director).
        """
