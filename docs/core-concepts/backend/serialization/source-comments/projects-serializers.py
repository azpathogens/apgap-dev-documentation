class ProjectListSerializer(serializers.ModelSerializer):
    """
    List / nested payload: never touch GCS (avoids timeouts when many rows load at once).

    ``output_bucket`` is derived only from ``_cached_seqera_output_bucket``; if the cache
    is empty and GCP is enabled, returns ``null`` until the cache is warmed (e.g. after build).
    """


class ProjectSerializer(serializers.ModelSerializer):
    output_bucket = serializers.SerializerMethodField()
    has_build_error = serializers.SerializerMethodField()

    def get_output_bucket(self, obj):
        """Get the Seqera output bucket, handling any potential errors."""


class ProjectDetailSerializer(ProjectSerializer):
    """Serializer for detailed project information including Seqera URLs."""

    def get_vertex_notebook_uri(self, obj):
        """Get the Vertex Notebook URI, handling any potential API errors."""

    def get_seqera_launchpad_url(self, obj):
        """Get the Seqera Launchpad URL, handling any potential API errors."""


class ProjectPostPatchSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating projects."""

    def create(self, validated_data):
        """Attach `created_by` user before saving."""


class ProjectUserCreateSerializer(serializers.ModelSerializer):


class ProjectUserPatchSerializer(serializers.ModelSerializer):
    permission_group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.exclude(
            name=PermissionGroups.PLATFORM_ADMIN.value),
    )

    def validate_permission_group(self, group):
        """Ensure the Platform Admin group is not assigned."""


class ProjectArchiveSerializer(serializers.Serializer):
    """Archive accepts an empty JSON body (see project archive tests)."""


class ProjectHardDeleteSerializer(serializers.Serializer):
    """Hard delete requires ``deletion_justification`` (min length enforced in service)."""
