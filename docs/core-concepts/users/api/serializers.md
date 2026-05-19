
   def get_project_memberships(self, obj):
        """
        Get all projects the user is assigned to, filtering out projects in inactive labs.
        Uses prefetched project_memberships to avoid N+1 queries.
        """

    def get_lab_memberships(self, obj):
        """
        Get all labs the user is directly assigned to, filtering out inactive labs.
        Uses prefetched lab_memberships and project_memberships to avoid N+1 queries.
        """
