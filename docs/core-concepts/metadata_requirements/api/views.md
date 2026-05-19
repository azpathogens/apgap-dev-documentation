class OptionalPageNumberPagination(PageNumberPagination):
    """
    Pagination class that only activates when the 'pagination' query parameter is present.
    When pagination is enabled, use 'page' parameter to specify the page number.
    Example: ?pagination=true&page=2
    """


class BaseMetadataViewSet(viewsets.ModelViewSet):
    """
    Abstract base ViewSet providing common functionality for metadata-related views.
    """

    def get_queryset(self):
        """
        Optimize queryset with select_related and prefetch_related.
        Override in subclasses for model-specific optimizations.
        """


class SourceTypeViewSet(BaseMetadataViewSet):
    """
    ViewSet for managing SourceType model.

    Provides CRUD operations for source types with:
    - Filtering by name
    - Searching across name field
    - Ordering by name or id
    - Statistics endpoint for related metadata requirements
    """

    def get_queryset(self):
        """Optimize queryset with requirement counts when needed."""

    @action(detail=True, methods=["get"])
    def requirements(self, request, pk=None):
        """
        Get all metadata requirements for a specific source type.

        Returns a list of metadata requirements that apply to this source type,
        including both specific requirements and universal requirements (where source_type is null).
        """

    @action(detail=False, methods=["get"])
    def statistics(self, request):
        """
        Get statistics about source types and their requirements.

        Returns aggregated data about source types including:
        - Total number of source types
        - Source types with most requirements
        - Source types with no requirements
        """


class MetadataRequirementViewSet(BaseMetadataViewSet):
    """
    ViewSet for managing MetadataRequirement model.

    Provides comprehensive CRUD operations with:
    - Advanced filtering capabilities
    - Nested serialization for related objects
    - Bulk operations support
    - Validation of unique constraints
    """

    def get_queryset(self):
        """Optimize queryset with related object prefetching."""
    # Removed get_filterset_class as we always use MetadataRequirementAdvancedFilter now

    def get_serializer_class(self):
        """Use list serializer for list action, full serializer otherwise."""

    @action(detail=False, methods=["post"])
    def bulk_create(self, request):
        """
        Create multiple metadata requirements at once.

        Expects a list of requirement objects in the request body.
        Validates all requirements before creating any to ensure atomicity.
        """

    @action(detail=False, methods=["delete"])
    def bulk_delete(self, request):
        """
        Delete multiple metadata requirements by their IDs.

        Expects a list of IDs in the request body.
        """

    @action(detail=False, methods=["get"])
    def universal(self, request):
        """
        Get all universal metadata requirements (those that apply to all source types).

        Returns requirements where source_type is null.
        """

    @action(detail=False, methods=["get"])
    def by_source_type(self, request):
        """
        Get metadata requirements grouped by source type.

        Returns a dictionary with source type names as keys and their requirements as values.
        Includes a special "universal" key for requirements that apply to all types.
        """

    @action(detail=True, methods=["post"])
    def duplicate(self, request, pk=None):
        """
        Duplicate an existing metadata requirement.

        Creates a copy of the requirement with optional modifications.
        Accepts optional 'source_type' parameter to change the target source type.
        """


class MetadataTemplateViewSet(BaseMetadataViewSet):
    """
    ViewSet for managing MetadataTemplate model.

    Provides CRUD operations for metadata templates with:
    - Filtering by source_type
    - Nested serialization for related objects (key, options)
    - Ordering by sort_order
    - POST serializer with get-or-create logic for Key and Values
    """

    def get_queryset(self):
        """
        Optimize queryset with related object prefetching.
        Orders template_options alphabetically by value name.
        """

    def filter_queryset(self, queryset):
        """
        Apply filters to queryset.
        """

    def get_serializer_class(self):
        """Use appropriate serializer based on action."""

    def create(self, request, *args, **kwargs):
        """Create a metadata template with enhanced error handling."""

    def update(self, request, *args, **kwargs):
        """Update a metadata template with enhanced error handling."""

    def destroy(self, request, *args, **kwargs):
        """
        Delete a metadata template.
        Prevents deletion of core templates (is_core=True).
        """

    @action(detail=False, methods=["get"])
    def download_csv(self, request):
        """
        Download a CSV template with all metadata keys for a given source type.

        The CSV will have:
        - A 'filename' column as the first column
        - Columns for all metadata keys (both core and source type specific)
        - Optional info row showing field requirements and data types

        Query Parameters:
        - source_type: ID of the source type (optional)
        - include_info_row: Include requirement info row (default: false)

        Returns:
        - CSV file download
        """

    @action(detail=False, methods=["post"])
    def upload_csv(self, request):
        """
        Upload a CSV file to create FileMetadataTag entries for files.

        The CSV must have:
        - A 'filename' column with file paths/names
        - Columns for metadata keys with their values

        Request Body:
        - csv_file: The CSV file to upload
        - lab: ID of the lab for file context
        - source_type: ID of the source type (optional)
        - validate_only: If true, only validate without creating tags

        Returns:
        - Processing results including success count, errors, and warnings
        """
