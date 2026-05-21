class ProjectFilter(django_filters.FilterSet):
    """
    FilterSet for Project model.

    Supports filtering by:
    - status: Filter by project status (ACTIVE, ARCHIVED)
    - include_archived: Boolean flag to include archived projects (default: false)
    """

    def filter_queryset(self, queryset):
        """
        Override filter_queryset to apply default exclusion of archived projects.

        By default, archived projects are excluded unless:
        1. include_archived=True is explicitly provided, OR
        2. status=ARCHIVED is explicitly provided
        """

    def filter_include_archived(self, queryset, name, value):
        """
        Filter to include or exclude archived projects.

        This method is called when include_archived parameter is explicitly provided.
        The default exclusion logic is handled in filter_queryset.
        """
