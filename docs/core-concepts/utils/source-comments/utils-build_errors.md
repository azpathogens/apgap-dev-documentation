"""
Helpers for persisting GCP / Cloud Build provisioning failures on a model.

Models that opt in declare a ``last_build_error`` ``TextField``. The helpers
here capture the latest exception (formatted with type, message, and
traceback), truncate it to a sane size, and write it via
``save(update_fields=["last_build_error"])`` so it can be surfaced on the API
and rendered in the UI.

The helpers are intentionally defensive: nothing in this module is allowed to
raise into the calling exception handler. A failure to persist the error
message must not mask the original failure.
"""


def _has_error_field(instance: Any) -> bool:
    """Return True if the instance's model declares ``last_build_error``."""


def capture_build_error(
    instance: Any,
    exc: BaseException | str,
    *,
    max_len: int = DEFAULT_MAX_LEN,
) -> None:
    """
    Persist a captured failure on ``instance.last_build_error`` (truncated).

    ``exc`` may be either an ``Exception`` (we will format type, message, and
    traceback) or a plain string (used for synthesized non-exception failures
    such as a terminal Cloud Build ``FAILURE`` status).

    Never raises. Logs and returns silently on any error so the caller's
    primary error path is preserved.
    """


def clear_build_error(instance: Any) -> None:
    """
    Clear ``instance.last_build_error`` after a successful run.

    Only writes when the field is currently non-empty, to avoid an unnecessary
    UPDATE on every successful re-run. Never raises.
    """
