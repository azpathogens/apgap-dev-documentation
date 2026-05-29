"""
Predicates that decide what a user is allowed to do with a File, and what
state a File must be in to permit a given action
"""


def can_hard_delete_file(user, file) -> tuple[bool, str]:  # noqa: PLR0911
    """
    Decide whether `user` is allowed to hard-delete `file`.

    Returns (allowed, reason) where `reason` is a short user-facing string when denied,
    empty when allowed.
    """

    # Non-admin users can only delete files they created and only in a
    # deletable status (DRAFT, FAILED, or PII_DETECTED).

    # Check if user is a lab admin

    # If not a platform admin and not a lab admin, apply restriction
    # Default: allow admins to delete


def check_bulk_deletable(user, file) -> str | None:
    """
    Decide whether a single file can be hard-deleted as part of a bulk batch.

    Refuses the file if any of these hold:
      - status is PRIMARY (must go through the single-delete endpoint)
      - file is a copy living inside an analytical dataset
      - file has copies inside one or more analytical datasets
      - `user` lacks permission to hard-delete it (per `can_hard_delete_file`)

    Returns the user-facing reason for the first failing rule, or None if the
    file passes everything.
    """
