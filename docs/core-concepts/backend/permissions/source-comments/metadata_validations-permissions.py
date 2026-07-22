"""
Permissions for validation-rule administration.

Mirrors `MetadataTemplatePermission` in the metadata_requirements app to keep
the admin experience consistent: list/retrieve open to any authenticated user,
mutating actions gated to Platform Admins and Lab Directors.
"""


class ValidationRulePermission(permissions.BasePermission):
    """
    - list / retrieve          : any authenticated user
    - create / update / delete : Platform Admin or Lab Director (is_lab_admin=True)
    """
