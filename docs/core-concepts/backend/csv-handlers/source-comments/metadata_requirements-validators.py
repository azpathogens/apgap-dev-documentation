"""
CSV validation utilities for metadata templates.
"""


def validate_csv_structure(csv_content: str) -> tuple[bool, list[str]]:
    """
    Validate the basic structure of a CSV file.

    Args:
        csv_content: The CSV content as string

    Returns:
        Tuple of (is_valid, list of error messages)
    """
