"""
Validation engine: loads the relevant data for a File and dispatches rules.

Design notes:

- One `ValidationEngine(file).run(trigger=...)` call is side-effect-safe for
  `PREVIEW`; `PROMOTE` and `FORCE_PROMOTE` persist a `ValidationRun` + issues
  in a single transaction.
- Per-rule exception isolation: if any single handler raises, we swallow and
  emit a `CONFIG_ERROR` issue so the rest of the run continues. One bad rule
  can't block every upload.
- Queries are prefetched once so the loop is O(rules) in CPU and O(1) in DB
  round-trips.
"""


@dataclass
class ValidationContext:
    """Small read-only view of the File+tags state handed to validators."""


class ValidationEngine:
    """
    Main entry point.

    Usage:
        result = ValidationEngine(file).run(trigger=Trigger.PREVIEW, user=user)
    """

    def _load_values(self, templates):
        """Return dict template_id -> list[str]. Matches on key because
        FileMetadataTag points to Key, not Template."""

    # ---- execution -------------------------------------------------------

    def _partition_rules(self, rules):
        """Split a template's rules into (ungrouped, grouped-by-rule_group, has_required)."""

    def _run_rule_group(self, group_rules, template, values, context) -> list[Issue]:
        """Run a rule_group OR-set: passes iff at least one member passes."""

    def _run_field_rules(self, templates, context: ValidationContext) -> list[Issue]:
        # Implicit REQUIRED from MetadataTemplate.is_required — preserves the
        # legacy behavior where any `is_required=True` template blocked
        # promotion without the caller seeding an explicit rule row. Skipped
        # when an explicit REQUIRED ValidatorRule is present to avoid double
        # reporting.

    def _run_implicit_required(self, template, values) -> list[Issue]:
        # Display label prefers `template.name` so a per-template rename is
        # reflected immediately; falls back to `key.name`. Identity is carried
        # by `template_ids` (FK), not the display string.

        # ---- public API ------------------------------------------------------

    def run(
        self,
        *,
        trigger: str = Trigger.PREVIEW,
        user=None,
        acknowledged_warning_ids: list[str] | None = None,
        persist: bool | None = None,
    ) -> ValidationResult:
        """
        Execute all rules and return a `ValidationResult`.

        `persist` defaults to True for non-PREVIEW triggers (so we have an
        audit trail of every promote attempt), and False for PREVIEW.
        """
