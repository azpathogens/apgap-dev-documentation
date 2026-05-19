"""
Field-level validator implementations.

Each handler takes:
    rule       : the ValidatorRule instance
    template   : the MetadataTemplate being validated
    values     : list of string values attached to this file for this template
                 (a list even for single-select — multi-select templates just
                  carry more than one)
    context    : ValidationContext (db accessors, file, etc.)

and returns a list of Issue.
"""

# ---------------------------------------------------------------------------
# Helpers


def _template_keys(template) -> tuple[str, ...]:
    """Display-name snapshot for the in-flight UI.

    Prefers `template.name` so a per-template rename is reflected immediately;
    falls back to `template.key.name` when no override is set. Not part of
    `issue_hash` — see `Issue.template_ids` for the identity-bearing field.
    """


def _template_ids(template) -> tuple[int, ...]:
    """Stable FK snapshot used by `Issue.issue_hash`."""


def _issue(
    rule,
    template,
    *,
    code: str,
    message: str,
    offending_values: tuple[str, ...] = (),
) -> Issue:

    # ---------------------------------------------------------------------------
    # REQUIRED — pure "field must have at least one value"


@register_field(
    "REQUIRED",
    description="Field must have at least one value.",
)
def validate_required(rule, template, values, context) -> list[Issue]:
    # Empty strings and whitespace-only count as missing.

    # ---------------------------------------------------------------------------
    # TYPE_FORMAT


_FORMAT_CHECKS = {
    "alphanumeric": coercion.is_alphanumeric,
    "alpha": coercion.is_alpha,
    "integer": lambda v: coercion.coerce_integer(v)[0],
    "positive_integer": lambda v: (coercion.coerce_integer(v)[0] and coercion.coerce_integer(v)[1] > 0),
    "float": lambda v: coercion.coerce_number(v)[0],
    "positive_float": lambda v: coercion.coerce_positive_number(v)[0],
    "date": lambda v: coercion.coerce_date(v)[0],
    "url": coercion.is_valid_url,
    "zipcode": coercion.is_zipcode_us,
    "gps": coercion.is_gps,
    "npdes": coercion.is_npdes,
    "nwss_site_id": coercion.is_nwss_site_id,
    "nwss_sample_id": coercion.is_nwss_sample_id,
}


# ---------------------------------------------------------------------------
# NUMERIC_RANGE


def _numeric_range_config_issue(rule, template, mn, mx) -> list[Issue] | None:
    """Validate rule config; return a list with a single CONFIG_ERROR if invalid, else None."""


# ---------------------------------------------------------------------------
# NUMERIC_SINGLE_OR_RANGE (e.g. soil depth "5" or "[0, 10]")


def _in_bounds(x: Decimal, *, mn, mx, require_positive: bool) -> bool:
    # "require_positive" in the Phase 2 CSV means "non-negative" — e.g. soil
    # depth `[0, 2]` and `[0, 10]` are explicitly listed as valid.


def _validate_range_literal(  # noqa: PLR0913 — internal helper, explicit params aid readability
    rule,
    template,
    v: str,
    *,
    mn,
    mx,
    require_positive: bool,
) -> Issue | None:
    # Returning None is ambiguous (could mean "not a range literal"); caller uses
    # `_RANGE_LITERAL.match(v)` to disambiguate before calling.

    # ---------------------------------------------------------------------------
    # UNIQUE


@register_field(
    "UNIQUE",
    optional=["scope", "active_statuses"],
    description=(
        "Value must be unique within the given scope. "
        "`scope` ∈ {'PLATFORM', 'LAB', 'ORG'} (default PLATFORM). "
        "`active_statuses` overrides the default active-status allowlist."
    ),
)
def validate_unique(rule, template, values, context) -> list[Issue]:
    """
    Uniqueness is evaluated against other Files' FileMetadataTags attached to
    the same template.key — case-insensitive, whitespace-trimmed, NFC.
    Archived/Deleted files are excluded by default.
    """
# ---------------------------------------------------------------------------
# REFERENCES_MODEL — restricted allowlist


_REFERENCES_ALLOWLIST = {
    # model_label_lower : {match_field : column}
    "users.user": {"email": "email", "username": "username"},
    "labs.lab": {"name": "name", "display_name": "display_name"},
}


@register_field(
    "REFERENCES_MODEL",
    required=["target_model"],
    optional=["match_field", "allow_missing", "case_sensitive"],
    description=(
        "Value must identify an existing row in the target model. `target_model` must be one of the allowlisted labels."
    ),
)
