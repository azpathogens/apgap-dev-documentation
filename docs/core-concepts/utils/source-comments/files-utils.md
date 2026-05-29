"""Utility functions for file operations."""


def split_filename(filename: str) -> tuple[str, str]:
    """
    Split a filename into name and extension at the first dot.

    This ensures that compound extensions (e.g., '.fastq.gz', '.tar.gz')
    are preserved as a single unit when generating unique filenames.

    Args:
        filename: The filename to split.

    Returns:
        A tuple of (name, extension) where extension includes all dots.
        If no extension, returns (filename, '').

    Examples:
        >>> split_filename('sample.fastq')
        ('sample', '.fastq')
        >>> split_filename('sample.fastq.gz')
        ('sample', '.fastq.gz')
        >>> split_filename('sample.data.fastq')
        ('sample', '.data.fastq')
        >>> split_filename('README')
        ('README', '')
    """


def generate_unique_filename(lab, filename: str) -> str:
    """
    Generate a unique filename for a lab by appending -1, -2, etc.

    If a file with the given filename already exists for the lab,
    a numeric suffix is appended before the extension to create
    a unique filename.

    Args:
        lab: The Lab instance to check for existing files.
        filename: The original filename to make unique.

    Returns:
        The original filename if unique, otherwise a modified filename
        with a numeric suffix (e.g., 'sample-1.fastq').

    Examples:
        - If 'sample.fastq' doesn't exist: returns 'sample.fastq'
        - If 'sample.fastq' exists: returns 'sample-1.fastq'
        - If 'sample.fastq' and 'sample-1.fastq' exist: returns 'sample-2.fastq'
    """
