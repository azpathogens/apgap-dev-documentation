"""
Admin API for the validation-rule engine.
"""


class ValidatorRuleViewSet(viewsets.ModelViewSet):
    """CRUD for field-level validator rules."""


class CrossFieldRuleViewSet(viewsets.ModelViewSet):
    """CRUD for cross-field validator rules."""


class RuleTypeCatalogView(APIView):
    """
    Enumerate every supported rule type + its declarative param schema.

    Drives the admin UI (dropdowns, per-rule form fields) and acts as a
    drift-detection surface: if a rule_type exists in the Django enum but
    lacks a handler, `catalog` returns `registered=False` and tests fail.
    """
