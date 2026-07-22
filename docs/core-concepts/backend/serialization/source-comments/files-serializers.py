class FileUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for uploading files to GCS and creating File instances.
    Similar to DatasetFileSerializer but for lab files.
    """

    def get_lab_gcs_bucket(self, lab):
        """
        Get the GCS bucket for a lab.
        This could be configured per lab or use a default bucket with lab-specific prefixes.
        """
        # Use a default labs bucket from settings if it exists
        # Otherwise, use the DataOps bucket as fallback


class FilePostSerializer(serializers.ModelSerializer):
    """
    Serializer for creating file metadata (not for uploads).
    """


class FilePatchSerializer(serializers.ModelSerializer):
    """
    Serializer for updating file metadata via PATCH.
    Validates gcs_file_path uniqueness and restricts changes to DRAFT files.
    """

    def _extract_filename(self, gcs_file_path: str) -> str:
        """Extract the filename from a GCS file path."""

    def validate_gcs_file_path(self, value):
        """
        Validate that the new gcs_file_path has a globally unique filename.
        Only files in DRAFT status can have their path changed.
        """


class FileListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing files.
    """

    def get_batch_upload_id(self, obj):
        """
        Get the batch upload ID associated with this file.
        Uses prefetched uploads data to avoid N+1 queries.
        """

    def get_batch_upload_name(self, obj):
        """
        Get the batch upload name (ingest bucket) associated with this file.
        Uses prefetched uploads data with select_related batch_upload to avoid N+1 queries.
        """

    def get_copied_to_datasets(self, obj):
        """
        Get the analytical datasets this file has been copied to.
        Uses prefetched copies data with select_related to avoid N+1 queries.
        Returns a list of datasets with their id and name.
        """


class FileDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for file information.
    """

    def get_gcs_url(self, obj):
        """
        Generate the full GCS URL for the file.
        """

    def get_metadata_tags(self, obj):
        """
        Get all metadata tags associated with this file.
        Groups multi-select values (same key, different values) into arrays.
        """

    def get_meets_retention_requirement(self, obj):
        """
        Check if the file meets the minimum retention requirement for archiving.
        Returns True if the file has been stored for at least SEQUENCE_RETENTION_YEARS.
        """

    def get_copied_to_datasets(self, obj):
        """
        Get the analytical datasets this file has been copied to.
        Uses prefetched copies data with select_related to avoid N+1 queries.
        Returns a list of datasets with their id and name.
        """


class MetadataAssociationSerializer(serializers.Serializer):
    """
    Serializer for associating metadata tags with files.
    """

    def validate(self, attrs):
        """
        Validate that key and value are not empty strings.
        """


class FileDeleteSerializer(serializers.Serializer):
    """
    Serializer for file deletion requests.
    Requires a justification for audit purposes.
    """

    def validate_justification(self, value):
        """
        Validate that justification is meaningful.
        """


class BulkFileDeleteSerializer(serializers.Serializer):
    """
    Serializer for bulk file deletion requests.

    Bulk deletion only accepts non-PRIMARY files (DRAFT/FAILED/PII_DETECTED),
    where the per-file Deletion.justification is derived from the file's
    status rather than supplied by the caller.
    """


class MetadataCSVSerializer(serializers.Serializer):
    """Validates the body for FileViewSet.metadata_csv

    file_ids is optional: when omitted the view falls back to filtering by the
    request's query params (same FileFilter the list endpoint uses).
    """
