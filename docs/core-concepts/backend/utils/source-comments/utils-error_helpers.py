"""Helper functions for extracting clean error messages from DRF ValidationError objects."""


def extract_error_message(error):  # noqa: PLR0911
    """
    Extract clean string messages from DRF ValidationError or ErrorDetail objects.

    Args:
        error: Can be a ValidationError, ErrorDetail, list, dict, or string

    Returns:
        str: Clean error message string
    """
