"""
Lightweight dataclasses exchanged between the engine and individual validators.

Kept pydantic-free on purpose: this layer is called in hot paths and we want
zero allocation overhead beyond `dataclass` and basic dicts.
"""


@dataclass(frozen=True)
class Issue:
    """
    One error or warning produced by a single validator invocation.

    `issue_hash` is the stable identifier the frontend echoes back in
    `acknowledged_warning_ids`; it is derived from the content of the issue
    so that if anything material changes (rule params, offending value, the
    rule itself), the hash changes and any prior acknowledgement becomes
    invalid. See `compute_issue_hash`.

    Identity carriers:
        `template_ids` is the FK-stable identity of the template(s) involved
        and is what `issue_hash` actually folds in. `template_keys` is a
        denormalized display-name snapshot that the engine emits for the
        in-flight UI; it is intentionally NOT part of the hash so a rename
        does not invalidate outstanding acknowledgements.
    """


@dataclass
class ValidationResult:
    @property
    def is_passing(self) -> bool:
        """True when promotion should proceed."""

    @property
    def eligible_for_primary(self) -> bool:
        """
        True when *all* currently-outstanding issues could be resolved by
        acknowledging every warning. Used by the preview endpoint so the UI
        can decide whether to show the "Set Primary" button at all.
        """


def compute_issue_hash(  # noqa: PLR0913 — each kw is an independent identity component of the issue
    *,
    rule_kind: str,
    rule_id: int | None,
    code: str,
    template_ids: tuple[int, ...],
    offending_values: tuple[str, ...],
    rule_params_fingerprint: str,
) -> str:
    """
    Deterministic sha256 over the content-identifying fields of an issue.

    The fingerprint includes the rule's params — this is a *security*
    property: a user who acknowledges a warning then tampers with the rule
    would otherwise sneak past the gate. By folding params into the hash,
    any edit invalidates the acknowledgement.

    Identity is keyed on `template_ids` (stable FKs), NOT `template_keys`
    (display name snapshot). A rename of `MetadataTemplate.name` or
    `Key.name` therefore preserves the hash and any outstanding
    acknowledgements; only changes that materially affect the rule or
    the offending data invalidate the hash.
    """


def params_fingerprint(params: dict[str, Any]) -> str:
    """Stable, short fingerprint for a rule's params dict."""
