"""Shared validators for GCP identifiers (billing accounts, project IDs, etc.)."""


# GCP billing account ID format (e.g. ``ABCDEF-123456-FEDCBA``).
# The Cloud Console / Cloud Billing API uses an 18-character ID composed of three
# 6-character segments joined with dashes; for ASU's accounts those characters
# are uppercase hex, but we accept lowercase here to be forgiving on input.
BILLING_ACCOUNT_ID_RE = re.compile(
    r"^[0-9A-Fa-f]{6}-[0-9A-Fa-f]{6}-[0-9A-Fa-f]{6}$")


def validate_billing_account_id(value: str | None) -> str:
    """
    Normalize and validate a GCP billing account ID string.

    Returns the cleaned (stripped) value when ``value`` is empty/whitespace or
    matches the expected ``XXXXXX-XXXXXX-XXXXXX`` shape. Raises
    :class:`rest_framework.serializers.ValidationError` otherwise so callers
    can plug this directly into a DRF serializer field's ``validate_*`` hook.
    """
