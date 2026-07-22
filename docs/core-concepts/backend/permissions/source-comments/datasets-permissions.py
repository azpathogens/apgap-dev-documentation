
class DatasetHierarchicalPermission(permissions.BasePermission):
    """
    Permission class that checks if the user has permissions at any level:
    1. Global - Direct user permissions
    2. Lab level - Via lab membership
    3. Project level - Via project membership (either owning project or assigned projects)

    Only checks permissions for create, update, and delete operations.
    List and retrieve permissions are handled at the viewset level.
    """

    def has_permission(self, request, view):  # noqa: PLR0911
        """
        Check if user has permission to perform the action at any level.
        """
        # Exit early if user not authenticated

        # Get the permission needed for this action

        # Exit early if no permission mapping

        # For list/retrieve, defer to get_queryset

        # Check global permission first

        # Log all user permissions

        # Log user groups

        # Check project level permissions

        # For object-specific actions, check permissions at dataset level

        # Default to deny for any other actions

    def _is_object_specific_action(self, action):
        """Helper method to check if action is object-specific."""

    def _check_object_specific_permissions(self, request, view, permission_codename):  # noqa: PLR0911
        """Helper method to check permissions for object-specific actions."""

        # Handle lab directors
        # For non AZDHS users, only lab directors can assign datasets to projects

        # If AZDHS user, they can only assign datasets to projects in their jurisdiction

        # Default to deny for all other users

        # Special case for downloading service account keyfiles
        # Only allow users with permissions on the owning project

        # Check permissions on the OWNING PROJECT only
        # Check project-level permission for the OWNING project only
        # Check lab-level permission for the dataset's lab

        # Check permissions in hierarchy (project, lab, platform admin)

    def _has_project_permission(self, user, project, permission_codename):
        """Helper method to check project-level permissions."""
        # Log all project memberships

    def _has_lab_permission(self, user, lab, permission_codename):
        """Helper method to check lab-level permissions."""

    def has_object_permission(self, request, view, obj):
        """
        Check if user has permission to perform the action on a specific dataset.
        """

        # Get the permission needed for this action
        # Default to allow for actions not in permission_map

        # Check all possible permissions in one return statement
        # Check global permission
        # Check project-level permission for owning project
        # Check lab-level permission
        # Special handling for AZDHS users
        # Check platform admin


class DatasetFileHierarchicalPermission(permissions.BasePermission):
    """
    Permission class that checks access at global, lab, and project levels.
    Also checks access to the parent dataset before allowing file operations.
    """

    def has_permission(self, request, view):  # noqa: PLR0911, C901
        """
        Check if user has permission to perform the requested action.
        """

        # Check dataset access first

        # For file uploads (create/POST), only allow users with access to the OWNING project

        # For other actions, check general dataset access

        # Map REST actions to Django permission codenames

        # Get the required permission for this action

        # Check global permission
        # For list/retrieve, if user has dataset access, they can view files

        # For other actions, check specific permissions
        # Check lab membership with specific permission (not just any lab user)

        # Check if user is lab admin (lab admin has all permissions)

        # Check project permissions

    def has_object_permission(self, request, view, obj):  # noqa: PLR0911
        """
        Check if user has permission to perform the requested action on this file.
        """

        # For file creation, check upload access to the dataset

        # For other actions, check dataset access first

        # Map REST actions to Django permission codenames

        # Get the required permission for this action

        # Check global permission

        # Check lab membership with specific permission (not just any lab user)

        # Check if user is lab admin (lab admin has all permissions)

        # Check project membership (both owning and assigned projects)

    def has_dataset_access(self, user, dataset):
        """
        Check if user has access to the dataset through any means:
        - Global permissions
        - Lab Director membership
        - Project membership (owning or assigned project)
        """

        # Check global permission

        # Check lab membership (any lab user can access datasets in their lab)

        # Check project membership
        # Check assigned projects

    def has_dataset_upload_access(self, user, dataset):
        """
        Check if user has access to upload files to the dataset.
        Only users with access to the OWNING project can upload files.
        """

        # Check global permission

        # Check platform admin

        # Check lab membership with upload permission

        # Check ONLY owning project membership (not assigned projects)
