"""
Registry + decorator + dispatch for validators.

This file intentionally has no Django-model imports at module scope so it
can be imported cheaply and so tests can monkeypatch handlers.
"""


# Signatures:
#   field validator     : (rule, template, values, context) -> list[Issue]
#   cross-field validator: (rule, context) -> list[Issue]

# Declarative param schema per rule_type. The rule-types-catalog API exposes
# this; the API serializer validates payloads against it on create/update.
# Each entry:
#   { "required": [...], "optional": [...], "description": "..." }


def register_field(
    rule_type: str,
    *,
    required: list[str] | None = None,
    optional: list[str] | None = None,
    description: str = "",
) -> Callable[[FieldValidator], FieldValidator]:
    """
    Decorator: register a field-level validator for `rule_type`.

    Also records the declarative param schema so the admin API can surface
    the accepted params and reject unknown ones at create time.
    """
