"""
Serializers for the validation-rule admin API.

Key property: params are validated against the declarative schema in
`validators/registry.py::RULE_PARAM_SCHEMA` so admins cannot POST an
unknown-rule_type rule or a rule missing required params.
"""


def _validate_params_against_schema(rule_type: str, params: dict) -> None:
    """Reject unknown keys and missing required keys for the given rule_type."""


class ValidationIssueReadSerializer(serializers.ModelSerializer):
    """Read-only serializer for `ValidationIssue`.

    `template_keys` is derived at read time from the FK-stable `template_ids`
    (preferred) or, for legacy rows lacking IDs, from the persisted name
    snapshot. Resolution uses one bulk fetch of every distinct template ID
    referenced in the queryset (see `to_representation`) so the per-row work
    is O(1) regardless of issue count.

    A template that has been deleted since the issue was written is rendered
    as the empty list rather than raising; older legacy rows continue to
    show their stored name snapshot until the next backfill or rewrite.
    """

    @staticmethod
    def _label_for(template) -> str:
        """Display label that matches the engine's `_label` precedence.

        Centralized here (and in `field_validators._label`) so all surfaces
        agree on the rule: `template.name` if set, else `key.name`, else "".
        """

    def _name_lookup(self) -> dict[int, str]:
        """Return a {template_id: display_name} map for this serializer call.

        Cached on `self.context` so a list view that serializes N issues
        triggers exactly one bulk fetch over `MetadataTemplate`.
        """

    def get_template_keys(self, obj) -> list[str]:
        """Render the display-name snapshot.

        Order of preference:
        1. Resolve `obj.template_ids` to current `MetadataTemplate.name`
           (or `key.name` fallback). Reflects renames immediately.
        2. If `template_ids` is empty (legacy row), fall back to the
           persisted `template_keys` snapshot so old rows still serialize.
        3. If a template has been deleted, its slot is omitted.
        """
