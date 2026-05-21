class ArchiveRequestQuerySet(models.QuerySet):
    """Custom QuerySet for ArchiveRequest model."""

    def in_active_labs(self):
        """
        Filter archive requests to only include those for files in active labs.
        Since ArchiveRequest uses GenericForeignKey, we filter by File content type
        and file IDs that are in active labs.
        """

    def for_requester(self, user):
        """Filter archive requests created by the specified user."""

    def for_reviewer(self, user):
        """Filter archive requests reviewed by the specified user."""

    def for_lab_director(self, user):
        """
        Filter archive requests for files in labs where the user is a director.
        """

    def for_active_lab_director(self, user):
        """
        Filter archive requests for files in active labs where the user is a director.
        """

    def pending(self):
        """Filter archive requests that are pending."""

    def approved(self):
        """Filter archive requests that are approved."""

    def denied(self):
        """Filter archive requests that are denied."""


class ArchiveRequestManager(models.Manager):
    """Custom Manager for ArchiveRequest model."""

    def in_active_labs(self):
        """Filter archive requests to only include those for files in active labs."""

    def for_requester(self, user):
        """Filter archive requests created by the specified user."""

    def for_reviewer(self, user):
        """Filter archive requests reviewed by the specified user."""

    def for_lab_director(self, user):
        """Filter archive requests for files in labs where the user is a director."""

    def for_active_lab_director(self, user):
        """Filter archive requests for files in active labs where the user is a director."""

    def pending(self):
        """Filter archive requests that are pending."""

    def approved(self):
        """Filter archive requests that are approved."""

    def denied(self):
        """Filter archive requests that are denied."""
