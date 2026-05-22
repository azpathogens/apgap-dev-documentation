class ProjectQuerySet(models.QuerySet):
    """Custom QuerySet for Project model with reusable filtering methods."""

    def in_active_lab(self):
        """Filter to only include projects that are in an active lab."""


class ProjectModelManager(models.Manager):

    def in_active_lab(self):
        """Filter to only include projects that are in an active lab."""

    def active(self):
        """Return only active (non-archived) projects."""
        # Import here to avoid circular import: models.py imports ProjectModelManager,
        # and ProjectStatus is defined in models.py

    def archived(self):
        """Return only archived projects."""
        # Import here to avoid circular import: models.py imports ProjectModelManager,
        # and ProjectStatus is defined in models.py

    def for_user(self, user, *, include_archived=False):
        """
        Return a queryset of projects that the user has access to.

        The user can have access to projects in the following ways:
        1. Platform Admin - see all projects
        2. Lab member with view_project permission - see all projects in labs where they have that permission
        3. Project member (ProjectUser) - see only projects they're members of with view_project permission
        """

        # Check if user is a Platform Admin - they see all projects (only from active labs)

        # Check if user is a lab member (director or reader) with view_project permission

        # Check if the permission group has view_project permission

        # Lab members with view_project permission see all projects in those labs (only from active labs)

        # Regular users: only see projects they're members of

        # Deduplicate the list
