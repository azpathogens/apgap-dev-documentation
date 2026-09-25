class User(AbstractUser):
    """
    Default custom user model for ASU APGAP.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    @property
    def can_assign_to_lab_or_project(self):
        """
        Check if user can be assigned to a lab or project.
        Platform admins and data analysts cannot be assigned to labs or projects.

        Checks both boolean fields and permission groups to ensure consistency.

        Returns:
            bool: True if user can be assigned, False otherwise
        """

    def get_restricted_role_name(self):
        """
        Get the name of the restricted role if user is a platform admin or data analyst.
        Checks both boolean fields and permission groups.

        Returns:
            str: "Platform Admin" or "Data Analyst" if user has restricted role, None otherwise
        """

    def save(self, *args, **kwargs):
        """
        Custom save method to handle group assignments for platform admin and data analyst roles.
        """

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})

    def get_absolute_api_url(self) -> str:
        """Get URL for user's reactivate API endpoint.

        Returns:
            str: URL for user reactivation endpoint.

        """
        return reverse("api:user-detail", kwargs={"pk": self.id})

    @property
    def is_domain_allowed(self) -> bool:
        """
        Existing users: always allowed.
        New users: allowed only if their email domain is in the domain allowlist.
        """

    def get_projects(self, lab=None):
        """
        Get projects that the user has access to.
        If lab is provided, return projects in the lab.
        If lab is not provided, return projects in all labs the user has access to.
        Projects in inactive labs are always filtered out.

        Access rules:
        - Superusers and Platform Admins: See all projects
        - Lab Directors: See all projects in their labs (where is_lab_admin=True)
        - Others: See only projects they are directly assigned to
        """

    def get_accessible_batch_uploads(self):
        """
        Get batch uploads that the user has access to based on their role.

        Access rules:
        - Superusers and Platform Admins: See all batch uploads
        - Lab Directors: See all batch uploads in their labs (where is_lab_admin=True)
        - Others: See only batch uploads they created
        """

    def get_active_lab_memberships(self):
        """
        Get lab memberships for this user, filtered to only include active labs.

        Returns:
            QuerySet[LabUser]: LabUser queryset filtered by active labs.
        """

    def get_active_project_memberships(self):
        """
        Get project memberships for this user, filtered to only include projects in active labs.

        Returns:
            QuerySet[ProjectUser]: ProjectUser queryset filtered by active labs.
        """

    def get_analytical_datasets(self):
        """
        Get analytical datasets that the user has access to based on their role.

        Access rules:
        - Superusers and Platform Admins: See all analytical datasets in active labs
        - Lab Directors: See all analytical datasets in projects within their labs
        - Others: See analytical datasets in projects they are assigned to

        Returns:
            QuerySet[AnalyticalDataset]: Analytical datasets the user can access.
        """

    def get_access_requests(self):
        """
        Get access requests that the user has access to based on their role.

        Access rules:
        - Superusers, Staff, and Platform Admins: See all access requests in active labs
        - Others: See requests where user is the requester OR an approver

        Returns:
            QuerySet[AccessRequest]: Access requests the user can access.
        """

    def get_archive_requests(self):
        """
        Get archive requests that the user has access to based on their role.

        Access rules:
        - Superusers, Staff, and Platform Admins: See all archive requests in active labs
        - Lab Directors: See requests for files in labs where they are director
        - Others: See requests they created

        Returns:
            QuerySet[ArchiveRequest]: Archive requests the user can access.
        """

    def get_saved_searches(self):
        """
        Get saved searches visible to this user.

        Visibility rules:
        - Searches created by this user (private or shared)
        - Searches shared with a lab the user is a member of

        Returns:
            QuerySet[SavedSearch]: Saved searches the user can see.
        """
