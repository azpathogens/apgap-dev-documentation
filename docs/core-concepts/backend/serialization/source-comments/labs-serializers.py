class LabSerializer(serializers.ModelSerializer):

    def get_projects(self, lab):
        """
        Filter projects based on user permissions:
        1. If user has global permissions or direct lab assignment, return all projects
        2. If user only has project assignments in this lab, return only those projects
        3. If no permissions, return empty list

        Applies the same archived project filtering as ProjectFilter by reusing the filter.

        Nested projects use :class:`~asu_apgap.projects.api.serializers.ProjectListSerializer` so
        ``GET /api/labs/`` (and lab payloads that embed projects) do not read Terraform state from GCS
        per row - that would hit storage once per project and log 404s for builds still in progress. Use
        ``GET /api/projects/<id>/`` for full fields that may lazy-load from state.
        """


class LabListSerializer(LabSerializer):
    """
    Lab list: avoid GCS on ``project_id`` (use DB cache only). Nested projects use
    ``ProjectListSerializer`` (see ``LabSerializer.get_projects``).
    """


class LabProjectUserSerializer(serializers.ModelSerializer):

    def get_project_assignments(self, obj):
        """
        Get all project assignments for this user in this lab.
        Uses prefetched data from context to avoid N+1 queries.
        """
