class Organization(models.Model):

    def delete(self, *args, **kwargs):
        """
        Prevent deletion if organization has any users in labs or projects.
        """

    def has_users(self):
        """
        Check if organization has any users in labs or projects.
        Returns True if there are:
        - Direct users (User.organization)
        - Lab users (LabUser where lab.organization = this)
        - Project users (ProjectUser where project.lab.organization = this)
        """
