
class UploadListSerializer(serializers.ModelSerializer):
    """Serializer for listing GUI uploads with minimal information."""


class UploadDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed GUI upload information."""


class UploadCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new GUI uploads."""

    def create(self, validated_data):
        """Create a new GUI upload with unique filename generation."""

    def to_representation(self, instance):
        """Include upload_url in the response representation."""


class BatchUploadListSerializer(serializers.ModelSerializer):
    """Serializer for listing batch uploads with minimal information."""

    def get_file_count(self, obj):
        """Get the count of files uploaded in this batch."""


class BatchUploadDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed batch upload information."""

    def get_files(self, obj):
        """Get list of files uploaded in this batch."""


class BatchUploadCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new batch uploads."""

    def create(self, validated_data):
        """Create a new batch upload with auto-generated unique ingest bucket name.

        Bucket naming rules for GCS:
        - Must be 3-63 characters long
        - Must start and end with alphanumeric character
        - Can contain lowercase letters, numbers, and hyphens
        - Cannot contain consecutive hyphens
        - Must be globally unique
        """

        # Generate unique bucket name components

        # Create timestamp in compact format (no hyphens within timestamp)

        # Generate short UUID (8 chars)

        # Get optional prefix from settings or use default

        # Construct bucket name with proper formatting
        # Format: {prefix}-lab{lab_id}-{timestamp}-{uuid}

        # Ensure DNS compliance:
        # 1. Convert to lowercase

        # 2. Replace any invalid characters with hyphens

        # 3. Remove consecutive hyphens

        # 4. Remove leading/trailing hyphens

        # 5. Ensure length constraints (max 63 chars)
        # Truncate timestamp if needed but keep UUID for uniqueness

        # 6. Ensure minimum length (3 chars)

        # Add the generated bucket name to validated data

        # Auto-generate service account secret name if not provided
        # Use the same short UUID for consistency
        # Format: projects/{project_id}/secrets/batch-sa-{uuid}/versions/latest
        # The actual project_id will need to be filled in by the signal handler
