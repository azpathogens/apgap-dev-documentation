"""Keep analytical-dataset metadata CSVs in sync with FileMetadataTag edits.

The CSV builder resolves tags through ``original_file_id``, so a metadata
change on a source file silently invalidates the CSV for every dataset that
contains a copy of it. These receivers fan out a refresh to each such
dataset; the debounced enqueue helper collapses bulk edits per dataset.
"""


def _enqueue_refresh_for_dependents(file_id: int) -> None:
    """Enqueue a CSV refresh for every dataset that points at ``file_id``.

    Covers both the common case (datasets containing copies of this file) and
    the edge case where the file itself is a direct dataset member.
    """
