"""
Utility functions for metadata handling.
"""


def normalize_date_value(value_name: str) -> str:
    """
    Normalize a date value to a canonical format (YYYY-MM-DD).

    Parses various date formats and returns a consistent format to prevent
    duplicates like "12/1/26" and "12/01/26" being stored as different values.

    Args:
        value_name: The date string to normalize

    Returns:
        str: Normalized date string in YYYY-MM-DD format, or uppercase original if parsing fails
    """


def normalize_metadata_value(value_name: str, data_type: str) -> str:
    """
    Normalize a metadata value based on the key's data type.

    Args:
        value_name: The value string to normalize
        data_type: The key's data type (from Key.DataType)

    Returns:
        str: Normalized value string
    """
