"""Helpers for building metadata CSV exports of File records"""


def collect_metadata_rows(
    files: Iterable["File"],
    *,
    include_status: bool = False,
) -> tuple[list[str], list[list[str]]]:
    """
    Build (header, rows) for a metadata CSV export for a file or files containing:
    - filename
    - all metadata tags
    - file upload status (if include_status is True)

    Returns:
        (header, rows) where each row is aligned to the header columns.
    """
    files_list = list(files)

    # for copies in analytical datasets the metadata lives on the original
    # so resolve to the original file id


def build_metadata_csv_string(
    files: Iterable["File"],
    *,
    include_status: bool = False,
) -> str:
    """
    Build a metadata CSV export for a file or files containing:
    - filename
    - all metadata tags
    - file upload status (if include_status is True)

    Returns:
        CSV content as string with header row and data rows
    """


def write_metadata_csv(
    response,
    files: Iterable["File"],
    *,
    include_status: bool = False,
) -> None:
    """
    Build a metadata CSV export for a file or files containing:
    - filename
    - all metadata tags
    - file upload status (if include_status is True)

    The CSV is streamed directly to the file-like response object. Caller is responsible
    for setting Content-Type and Content-Disposition

    Returns:
        None
    """
