"""
CSV import handler for metadata templates.
"""


class CSVImportHandler:
    """Handles import of CSV data to create FileMetadataTag entries."""

    def __init__(self, lab: Lab):
        """
        Initialize the import handler.

        Args:
            lab: The lab context for file lookups
        """

    def process_csv(self, csv_content: str, source_type: SourceType | None = None) -> dict:
        """
        Process uploaded CSV and create FileMetadataTag entries.

        Args:
            csv_content: The CSV content as a string
            source_type: Optional source type for validation

        Returns:
            Dictionary with results including success count, errors, and warnings
        """

    def _is_info_row(self, second_row: list[str] | None) -> bool:
        """
        Check if the second row looks like an info row.

        Args:
            second_row: The 2nd row of the CSV as a list of values, or None

        Returns:
            True if it appears to be an info row, False otherwise
        """

    def _build_expected_info_row(
        self,
        fieldnames: list[str],
        templates: list[MetadataTemplate],
    ) -> list[str]:
        """
        Build the expected info row based on templates.

        Args:
            fieldnames: List of column names from the CSV header
            templates: List of metadata templates to validate against

        Returns:
            List of expected values for the info row
        """

    def _compare_info_rows(
        self,
        actual_row: list[str],
        expected_row: list[str],
        fieldnames: list[str],
    ) -> list[str]:
        """
        Compare actual info row with expected and return list of mismatches.

        Args:
            actual_row: The actual info row values
            expected_row: The expected info row values
            fieldnames: List of column names for error messages

        Returns:
            List of mismatch error messages (empty if no mismatches)
        """

    def _validate_info_row(
        self,
        second_row: list[str] | None,
        fieldnames: list[str],
        templates: list[MetadataTemplate],
    ) -> str | None:
        """
        Validate that the 2nd row (info row) matches the expected OPTIONAL/REQUIRED format.

        Args:
            second_row: The 2nd row of the CSV as a list of values, or None if no 2nd row exists
            fieldnames: List of column names from the CSV header
            templates: List of metadata templates to validate against

        Returns:
            Error message if validation fails, None if valid or no info row present
        """

    def _get_templates(self, source_type: SourceType | None) -> list[MetadataTemplate]:
        """Get relevant templates for validation."""

    def _get_file_from_row(self, filename: str, row_num: int) -> tuple[File | None, str | None]:
        """
        Get the file object from a filename.

        Args:
            filename: The filename from the CSV row
            row_num: Row number for error reporting

        Returns:
            Tuple of (File object or None, error message or None)
        """

    def _process_metadata_columns(
        self,
        row: dict,
        file_obj: File,
        template_map: dict,
        row_num: int,
        source_type: SourceType | None = None,
    ) -> tuple[set, int, list]:
        """
        Process metadata columns for a file.

        Args:
            row: Dictionary of column name to value
            file_obj: The file object to add metadata to
            template_map: Map of key names to templates
            row_num: Row number for error reporting

        Returns:
            Tuple of (added_tag_ids set, tags_created count, errors list)
        """

    def _trigger_metadata_signal(self, file_obj: File, added_tag_ids: set) -> None:
        """
        Trigger m2m_changed signal for file status update.

        Args:
            file_obj: The file object
            added_tag_ids: Set of metadata tag IDs that were added
        """

    def _process_row(self, row: dict, row_num: int, template_map: dict, source_type) -> dict:
        """
        Process a single CSV row.

        Args:
            row: Dictionary of column name to value
            row_num: Row number for error reporting
            template_map: Map of key names to templates

        Returns:
            Dictionary with processing results
        """

    def _create_metadata_tag(
        self,
        template: MetadataTemplate,
        value_str: str,
        file_obj: File,
        row_num: int,
        source_type: SourceType | None = None,
    ) -> list[FileMetadataTag]:
        """
        Create or update FileMetadataTag entries.

        Args:
            template: The metadata template
            value_str: The value string from CSV
            file_obj: The file to tag
            row_num: Row number for error reporting

        Returns:
            List of created FileMetadataTag instances (empty list if none created)
        """
        # Handle multiple values for multi-select or LIST fields (pipe-separated in CSV)
        # Normalize the value based on key's data type (handles date normalization)

        # Validate against key's data type

        # For SELECT type, validate against predefined template options
        # LIST type accepts any free-form text or numeric string — no option check needed

        # Get or create the Value

        # Get or create the MetadataTag

        # here need to determine if i need to pass the source type or not
        # depending on if the metadata tag template has one or not
        # Create or update FileMetadataTag
