class FileQuerySet(models.QuerySet):
    """
    Custom QuerySet for File model to enable method chaining.
    """

    def active_lab(self):
        """
        Return a queryset of files that belong to active labs only.

        This method is chainable with other queryset methods.
        Example usage:
            File.objects.active_lab().for_user(user)
            File.objects.for_user(user).active_lab()
        """

    def for_user(self, user):
        """
        Return a queryset of files that the user has access to.

        The user can have access to files in the following ways:
        1. They are directly assigned to the lab that owns the file (LabUser)
        2. They are a member of a project in the lab that owns the file (ProjectUser)
        3. They have global access (Platform Admin); they have view_file on their user model
        4. They created the file
        """

    def get_unique_by_lab_and_path(self):
        """
        Return files that are unique by lab and gcs_file_path combination,
        keeping only the most recent version (by updated_at) for each unique combination.

        This method ensures that if multiple versions of the same file exist
        in the same lab, only the most recent one is returned.

        Returns:
            QuerySet: Files ordered by updated_at (most recent first),
                     with only the latest version of each lab/gcs_file_path combination.
        """

    def with_status_ordering(self):
        """
        Annotate and order the queryset by status priority.

        Priorities:
        1. DRAFT
        2. PRIMARY (Primary)
        3. Others

        Secondary ordering is by batch_upload ID, and then created_at.
        """


class FileModelManager(models.Manager):
    """
    Custom manager for File model to implement visibility rules.
    """

    def active_lab(self):
        """
        Return a queryset of files that belong to active labs only.
        Delegates to the QuerySet method for chaining support.
        """

    def for_user(self, user):
        """
        Return a queryset of files that the user has access to.
        Delegates to the QuerySet method for chaining support.
        """

    def get_unique_by_lab_and_path(self):
        """
        Return files that are unique by lab and gcs_file_path combination.
        Delegates to the QuerySet method for chaining support.
        """

    def with_status_ordering(self):
        """
        Annotate and order the queryset by status priority.
        Delegates to the QuerySet method for chaining support.
        """
