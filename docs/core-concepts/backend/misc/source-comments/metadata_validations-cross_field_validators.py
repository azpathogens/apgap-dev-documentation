"""
Cross-field validator implementations.

Cross-field rules operate on two templates within a single validation run.
The engine supplies a `ValidationContext` that exposes a lookup
`context.values_for(template_id) -> list[str]`.
"""


def _label(template) -> str:
    """Display label for a template; prefers per-template name override.

    Mirrors the helper in ``field_validators`` so cross-field issues use the
    same precedence (template.name → key.name → "").
    """


def _key_names(template) -> tuple[str, ...]:
    """Display-name snapshot for the in-flight UI.

    Prefers `template.name` so a per-template rename is reflected immediately;
    falls back to `template.key.name` when no override is set. Not part of
    `issue_hash` — see `Issue.template_ids` for the identity-bearing field.
    """


def _template_ids(template) -> tuple[int, ...]:
    """Stable FK snapshot used by `Issue.issue_hash`."""


def _issue(
    rule,
    *,
    code: str,
    message: str,
    templates: tuple,
    offending_values: tuple[str, ...] = (),
) -> Issue:
    """Build an Issue for a cross-field rule.

    Accepts a ``templates`` tuple (left, right) and derives both the display
    snapshot (``template_keys``) and the FK-stable identity (``template_ids``)
    from it, so callers don't have to duplicate the two-line boilerplate at
    every site. Order is preserved (left first, right second).
    """


def validate_conditional_required(rule, context) -> list[Issue]:
    # Value-comparison ops have no meaning when the condition field is empty —
    # short-circuit so configurations like `not_in: ["none"]` don't fire just
    # because nothing was selected. `is_empty`/`is_not_empty` are the explicit
    # ops for absence/presence and intentionally do NOT short-circuit here.
