"""
Data model for the configurable metadata-validation rule engine.

Four tables:

- `ValidatorRule`  : field-local rules attached to a `MetadataTemplate`
- `CrossFieldRule` : rules that span two templates within a source-type scope
- `ValidationRun`  : audit trail row per validation attempt (preview or promote)
- `ValidationIssue`: one row per error/warning produced during a `ValidationRun`

Cross-app FKs use string references (`"metadata_requirements.MetadataTemplate"`,
`"files.File"`, `"users.User"`) to avoid import cycles at app-loading time.
"""


class FieldRuleType(models.TextChoices):
    """
    Field-local rule kinds. A rule points to one `MetadataTemplate`.

    Parameters live in `ValidatorRule.params` (JSONField). Shape per kind
    is documented in `validators/registry.py::RULE_PARAM_SCHEMA`.
    """


class CrossFieldRuleType(models.TextChoices):
    """
    Cross-field rule kinds. A rule points to a `left_template` and `right_template`
    (may be the same template for intra-field rules like "none cannot co-occur with
    other multi-select values").
    """


class ValidatorRule(models.Model):
    """A single field-level validation rule attached to a `MetadataTemplate`."""


class CrossFieldRule(models.Model):
    """A validation rule that relates two templates within a source-type scope."""


class ValidationRun(models.Model):
    """
    Record of a single validation attempt against a `File`.

    Written for both `PREVIEW` (no state change) and `PROMOTE` (state change
    attempt). Cheap and high-cardinality; prune with a periodic task if needed.
    """


class ValidationIssue(models.Model):
    """A single error or warning emitted by a `ValidationRun`."""
