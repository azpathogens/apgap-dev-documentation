"""
CSV export handler for metadata templates.
"""


class CSVExportHandler:
    """Handles export of metadata templates to CSV format."""

    @staticmethod
    def generate_template_csv(
        source_type: SourceType | None = None,
        base_queryset: QuerySet | None = None,
    ) -> str:
        """
        Generate a CSV template with columns for all metadata keys.

        Args:
            source_type: The source type to get templates for. If None, only core templates are included.
            base_queryset: Optional pre-optimized queryset with select_related/prefetch_related.
                          If not provided, creates a new queryset with basic select_related.

        Returns:
            CSV string with header row containing 'filename' and all key names.
        """
        # Use provided queryset or create one with select_related for key
        # Get both core templates and source type specific templates
        # Use Q objects to properly handle the OR condition with null values
        # Get only core templates

        # Order by sort_order to maintain consistent column order

        # Build header row
        # First column is always filename
        # Track which template each key comes from for reference

        # Add empty rows for user to fill in (optional - could be omitted)
        # For now, just return the header

    @staticmethod
    def add_metadata_info_row(csv_content: str, templates: list[MetadataTemplate]) -> str:
        """
        Add a metadata info row to help users understand requirements.

        Args:
            csv_content: The existing CSV content
            templates: List of templates to get metadata from

        Returns:
            CSV with an additional info row
        """
