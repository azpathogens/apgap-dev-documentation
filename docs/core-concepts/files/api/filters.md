
class FileFilter(django_filters.FilterSet):
    """
    Filter for File model.
    """

    def _is_user_privileged_for_lab(self, user, lab_id=None):
        """
        Check if the requesting user is privileged (can see all drafts).
        A user is privileged if they are:
        - A superuser
        - A platform admin
        - A lab director for the relevant lab
        """

    def filter_by_created_by(self, queryset, name, value):
        """
        Filter files by created_by with special handling for different statuses.

        This filter only applies to list actions. For retrieve (detail) actions,
        any authenticated user can access any file.

        For non-privileged users:
        - Files are filtered to only labs where the user is an active member
        - All PRIMARY status files are returned (regardless of who created them)
        - DRAFT and PROCESSING files are only returned if created by the specified user
        - Other statuses are excluded

        For privileged users (superuser, platform admin, or lab director for the relevant lab):
        - All files are shown (no filtering by created_by or lab membership)
        """

    def filter_by_source_type(self, queryset, name, value):
        """
        Filter files by source_type ID(s).

        Supports both single and multiple source_type IDs:
        - Single: ?source_type=1
        - Multiple: ?source_type=1&source_type=2
        """

    def filter_by_metadata_tags(self, queryset, name, value):
        """
        Filter files by metadata tags.

        Query parameters:
        - metadata_filters: JSON-encoded array of filter conditions
        - metadata_filter_logic: "AND" or "OR" (defaults to "AND")

        Filter condition format:
        {
            "key": "Sex",
            "operator": "=",
            "value": "Male"
        }

        Supported operators by data type:
        - TEXT: =, <>, contains
        - NUMBER: =, <>, <, >, <=, >=
        - DATE: =, <>, <, >, <=, >=
        - SELECT: =, <>, includes, doesn't_include
        - GPS: =, <>, contains
        - LIST: =, <>, includes, doesn't_include, contains

        Delegated to :mod:`asu_apgap.files.api.metadata_filter_eval` so the
        same logic is shared with the dynamic-dataset subscription evaluator.
        """
