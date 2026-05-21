"""
Shared metadata-filter evaluator.

This module contains the pure logic that turns a ``metadata_filters`` JSON
payload (the same shape that ``FileFilter`` accepts via the API) into a
filtered Django queryset over ``files.File`` rows.

It is consumed by:

1. :class:`asu_apgap.files.api.filters.FileFilter` for the data-catalog HTTP
   endpoint.
2. :func:`asu_apgap.analytical_datasets.celery_tasks.dynamic_subscriptions
   .evaluate_dynamic_subscriptions` so dynamic-dataset matches use the exact
   same semantics that users see when previewing filters in the UI.

Keeping the implementation here (rather than in a method on ``FileFilter``)
ensures the two callers cannot drift apart.
"""


# Parsing / validation -----------------------------------------------------


def parse_metadata_filters_json(filters_json: str | None) -> tuple[list | None, str | None]:
    """Parse a JSON-encoded metadata_filters string.

    Returns ``(filters_list, error_message)``. ``filters_list`` is ``None``
    when ``filters_json`` is empty/None.
    """


def _check_key_identification(condition: dict) -> str | None:
    """Validate the key/key_id half of a filter condition.

    Accepts either ``{"key": "<name>", ...}`` (legacy), ``{"key_id": <int>, ...}``
    (forward), or both. Returns the error message on failure, ``None`` on success.
    Extracted so `validate_filter_condition` stays under the early-return budget.
    """


def validate_filter_condition(condition: Any) -> tuple[bool, str | None]:
    """Validate the shape of a single condition dict.

    Accepts either of two key-identification shapes:
    - Legacy: ``{"key": "<name>", ...}``
    - Forward: ``{"key": "<name>", "key_id": <int>, ...}``
    The forward shape is what the dual-write serializer produces; the legacy
    shape continues to be accepted so unmigrated rows / older clients keep
    working. ``key_id`` alone (no ``key`` string) is also accepted for
    completeness.
    """


def _get_key(name: str) -> Key | None:
    """Look up a `Key` by its current canonical name.

    Renames break this lookup, which is exactly the brittleness Change 3's
    `KeyAlias` model exists to backstop. The fallback wiring lives there;
    this helper stays narrow.
    """


def _resolve_key(condition: dict) -> Key | None:
    """Resolve a filter condition to its `Key` row.

    Preference order:
    1. `condition["key_id"]` — the FK-stable identifier dual-written into the
       JSON by the saved-search / dynamic-subscription serializers. Renames
       cannot break this path.
    2. `condition["key"]` — the legacy display-name string. Looked up against
       the current `Key.name`; if the key has since been renamed, the
       `KeyAlias` table (Change 3) provides a fallback through the historical
       name. Returns ``None`` if neither path resolves so the existing
       "unknown key matches nothing" semantics in `build_q_for_condition`
       continue to apply.
    """


def build_q_for_condition(condition: dict, queryset, *, use_exists: bool):
    """Build a (Q, queryset) pair for a single condition.

    Mirrors ``FileFilter._build_q_for_condition`` but is callable from
    anywhere. Returns ``(Q(pk__in=[]), None)`` when the key is unknown so the
    caller can compose it with other conditions without raising.

    Resolution prefers ``condition["key_id"]`` (FK, rename-safe) over
    ``condition["key"]`` (display name, legacy). See `_resolve_key`.
    """


# Public entry point -------------------------------------------------------


def apply_metadata_filters(
    queryset: QuerySet,
    metadata_filters: list[dict] | None,
    logic: str = "AND",
) -> QuerySet:
    """Apply a metadata-filter payload to a ``files.File`` queryset.

    Mirrors the semantics of ``FileFilter.filter_by_metadata_tags`` exactly,
    so the data-catalog UI preview and a dynamic-dataset subscription will
    always agree about what matches.

    Args:
        queryset: A queryset over ``files.File``.
        metadata_filters: A list of ``{"key", "operator", "value"}`` dicts.
            ``None`` or empty list returns the queryset unchanged.
        logic: ``"AND"`` (default) or ``"OR"``. Anything else returns the
            empty queryset, matching the strictness of the HTTP filter.

    Returns:
        A new queryset; the input is not mutated.
    """


def inject_key_ids(metadata_filters: list[dict]) -> list[dict]:
    """Return a copy of ``metadata_filters`` with ``key_id`` filled in.

    Resolves each condition's display name to a current `Key.id` (taking
    the `KeyAlias` fallback into account via `_resolve_key`) and writes
    the result onto a shallow-copied condition dict. Conditions that
    cannot be resolved are passed through unchanged so the persisted JSON
    keeps the original ``key`` string for human auditability and the
    runtime evaluator's "unknown key matches nothing" semantics still
    apply.

    Idempotent: a condition that already carries a valid ``key_id`` is
    not overwritten unless that id no longer resolves (in which case we
    fall back to a fresh resolution by name and only update if successful).

    Used by `SavedSearchCreateUpdateSerializer.validate_metadata_filters`
    and `DatasetSubscriptionSerializer.validate_metadata_filters` so the
    dual-write happens transparently at save time.
    """


def validate_metadata_filters_payload(metadata_filters: list[dict]) -> tuple[bool, str | None]:
    """Pre-flight validation used by the subscription serializer.

    Catches structural problems (bad shape, unknown operator for key's data
    type) without executing a query. Unknown keys are tolerated here for the
    same reason the runtime evaluator tolerates them: a renamed/missing key
    should not block saving the rule, it should just not match anything.
    """
