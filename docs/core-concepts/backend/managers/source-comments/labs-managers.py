
class LabQuerySet(models.QuerySet):
    """
    Custom QuerySet for Lab model to implement chainable filtering methods.
    """

    def active(self):
        """
        Return a queryset of only active labs.

        This method is chainable with other queryset methods.
        Example usage:
            Lab.objects.active().for_user(user)
            Lab.objects.for_user(user).active()
        """

    def for_user(self, user):
        """
        Return a queryset of labs that the user has access to.

        The user can have access to labs in the following ways:
        1. They are directly assigned to the lab (LabUser)
        2. They are a member of a project in the lab (ProjectUser)
        3. They have global access (Platform Admin); they have view_lab on their user model
        4. They are an AZDHS user (can only see AZDHS labs)
        """


class LabModelManager(models.Manager):
    """
    Custom manager for Lab model to implement visibility rules.
    Uses LabQuerySet to provide chainable methods.
    """

    def active(self):
        """
        Return a queryset of only active labs.
        Delegates to the QuerySet method for proper chaining.
        """

    def for_user(self, user):
        """
        Return a queryset of labs that the user has access to.
        Delegates to the QuerySet method for proper chaining.
        """
