class OptionalPageNumberPagination(PageNumberPagination):
    """
    Only paginate if ?pagination=true is present.
    Otherwise return full list.
    """


class FileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing files with GCS upload capability.

    Provides CRUD operations for files with appropriate permissions:
    - Global admins can create, update, and delete files
    - Lab members can view and manage files in their labs
    - Project members can view files in labs with their projects
    - File creators can manage their own files

    Features:
    - Direct file upload to GCS
    - Filtering by lab, file type, and status
    - Searching by GCS file path
    - Optional pagination
    - Support for file overwrite on duplicate names
    """

    def get_permissions(self):
        """
        Return the appropriate permission classes based on the action.
        List and retrieve only require authentication.
        Other actions require hierarchical permissions.
        """

    def get_serializer_class(self):
        """
        Return the appropriate serializer based on the action and request.
        """

    def _get_optimized_queryset(self, queryset):
        """
        Apply select_related and prefetch_related optimizations to reduce N+1 queries.
        """

    def get_queryset(self):
        """
        Filter files that the user has access to view.

        For list actions:
        - Returns unique files (filters out copied files)
        - The created_by filter applies special logic for DRAFT/PROCESSING visibility

        For retrieve (detail) actions:
        - Any authenticated user can access any file
        - No filtering restrictions applied
        """

    def create(self, request, *args, **kwargs):
        """
        Handle file creation with GCS upload.
        If a file is provided, it will be uploaded to GCS.
        """

    @action(detail=False, methods=["post"], url_path="upload")
    def upload(self, request):
        """
        Dedicated endpoint for file uploads.

        Expected form data:
        - file: The file to upload (required)
        - lab: The lab ID to associate the file with (required)
        """

    @action(detail=True, methods=["get"], url_path="download-url")
    def download_url(self, request, pk=None):
        """
        Generate a signed URL for downloading the file from GCS.
        This is a placeholder - actual implementation would generate
        a time-limited signed URL for secure file access.
        """

    def _validate_metadata_input(self, data):
        """Validate that the request body is in the correct format."""

    def _process_metadata_item(self, item, file_id):
        """Process a single metadata item and return tags and associations."""

    def _create_metadata_tag(self, key_name, value_name, value_data, source_type=None, *, include_source_type=False):
        """Create or get a metadata tag for a key-value pair."""

    def _get_existing_tuples(self, file_obj):
        """Get existing associations as (tag_id, source_type_id) tuples."""

    def _process_tags_to_associate(self, tags_to_associate):
        """Process tags and return new tuples and tag-to-source mapping."""

    def _remove_old_associations(self, file_obj, tuples_to_remove):
        """Remove old associations that are no longer needed."""

    def _create_new_associations(self, file_obj, tags_to_associate, tuples_to_add, tag_source_map):
        """Create new associations."""

    def _update_file_associations(self, file_obj, tags_to_associate):
        """Update the file's metadata associations with source_type support."""

    def _update_file_source_type(self, file_obj, first_source_type_id):
        """Update file's source_type to the first source_type seen in metadata."""

    def _trigger_status_check_signal(self, file_obj, stats):
        """Trigger m2m_changed signal to ensure file status is checked."""

    @action(detail=True, methods=["post"], url_path="associate-metadata")
    def associate_metadata(self, request, pk=None):
        """
        Set metadata tags for a file (complete replacement).

        This endpoint replaces all existing metadata associations with the provided ones.
        If you want to keep some existing metadata, you must include it in the request.

        Expected format:
        [
            {
                "key": "experiment_type",
                "value": "RNA-Seq",  # Single value
                "source_type": 1  # Optional: ID of the SourceType
            },
            {
                "key": "platforms",
                "value": ["illumina", "pacbio"],  # Multi-select (array)
                "source_type": 2  # Optional: ID of the SourceType
            }
        ]
        """

    @action(detail=True, methods=["get"], url_path="metadata-tags")
    def metadata_tags(self, request, pk=None):
        """
        Get all metadata tags associated with a file.

        Returns a list of metadata tags with their keys and values.
        Groups multi-select values (same key, different values) into arrays.
        """

    def _remove_single_metadata(self, file_obj, key_name, value_name, user_id):
        """Remove a single metadata tag association from a file."""

    def _process_removal_item(self, file_obj, item, user_id):
        """Process a single removal request item."""

    @action(detail=True, methods=["post"], url_path="remove-metadata")
    def remove_metadata(self, request, pk=None):
        """
        Remove metadata tags from a file.

        Expected payload:
        [
            {"key": "key1name", "value": "value1name"},
            {"key": "key2name", "value": ["value2a", "value2b"]},  # Multi-select - removes all
            {"key": "key3name", "value": "value3name"}
        ]

        This endpoint will remove the specified metadata tag associations from the file.
        """

    @action(detail=False, methods=["post"], url_path="metadata_csv")
    def metadata_csv(self, request):
        """
        Returns a CSV file download response for files containing:
        - filename
        - file upload status
        - all metadata tags

        Two ways to filter:
        - body {"file_ids": [1, 2, 3]} exports exactly those files
        - omit file_ids and pass the same query params the list endpoint accepts

        Files the requesting user can't see (e.g. inactive labs, draft visibility rules)
        are silently dropped and an empty result returns 404
        """

    def perform_create(self, serializer):
        """
        Set the created_by field when creating a file.
        """

    def perform_update(self, serializer):
        """
        Log file updates.
        """

    def destroy(self, request, *args, **kwargs):
        """
        Delete a file record permanently.

        A justification (for audit purposes) is required only when deleting a PRIMARY file.
        This will also delete the file from GCS and send a notification to the uploader.
        """

    @action(detail=False, methods=["post"], url_path="bulk-delete")
    def bulk_delete(self, request):
        """
        Hard-delete a batch of files asynchronously.

        Body: ``{ "file_ids": [int, ...], "justification": str (optional) }``

        Pre-validates synchronously:
        - each file must exist
        - all files must belong to the same lab
        - the caller must have delete permission
        - none may be PRIMARY
        - files cannot have dataset copies or have been copied into a dataset

        If any file fails validation, nothing is deleted and an error response
        is returned with 400.

        On acceptance the task is enqueued and a 202 is returned. Completion
        (and any per-file failures that arise during the task) are reported
        via an aggregated in-app/email notification.
        """

    @action(detail=True, methods=["post"], url_path="set-primary")
    def set_primary(self, request, pk=None):
        """
        Manually set a file's status to PRIMARY.

        Runs the full metadata validation engine. Errors block promotion; warnings
        block until explicitly acknowledged. The client may opt into acknowledging
        warnings by POSTing:

            { "acknowledged_warning_ids": ["<issue_hash>", ...] }

        Acknowledgement hashes are bound to the content of the rule + offending
        values; any change invalidates the acknowledgement.

        Only files in DRAFT status can be promoted to PRIMARY.

        Returns:
            200: File successfully promoted to PRIMARY
            400: errors, unacknowledged warnings, missing metadata, wrong status
        """

    @action(detail=True, methods=["post"], url_path="validate")
    def validate_metadata(self, request, pk=None):
        """
        Preview metadata validation for this file *without* changing state.

        Returns errors + warnings + the eligibility verdict the UI can use to
        show/hide the "Set Primary" button. Safe to call repeatedly.
        """

    @action(detail=True, methods=["get"], url_path="validation-runs")
    def validation_runs(self, request, pk=None):
        """Return the audit history of validation runs for this file."""
