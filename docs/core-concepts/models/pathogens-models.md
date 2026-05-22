class Pathogen(models.Model):
    """Registry of pathogens we track reportability (and metadata) for.
    Every Pathogen object has an associated metadata Value, but not every
    metadata Value that is an option for the pathogen key needs to have
    a Pathogen object

    The metadata Value name is used as the single source of truth for the
    pathogen name
    """

    @name.setter
    def name(self, val):

        # re-link to the (possibly existing) Value with that name rather than renaming in place.
        # renaming would collide if the target name already exists as a separate Value
        # (e.g. user fixing a typo where the correctly-spelled Value is already in use as a metadata tag)

    def is_reportable_for(self, file) -> bool:
        """Whether this pathogen makes `file` reportable.

        reportable=True overrides rules (always reportable). Otherwise,
        any active ReportabilityRule whose metadata_filters match the file is
        sufficient. No rules + override off = never reportable
        """


class PathogenReportabilityRule(models.Model):
    """Conditional reportability rule attached to a Pathogen

    A file tagged with the pathogen is reportable when this rule matches if
    Pathogen.reportable is False

    The metadata_filters JSON shape mirrors
    DatasetSubscription so the evaluator can be shared (files.api.metadata_filter_eval)
    """

    def matches(self, file) -> bool:
        """Whether `file` satisfies this rule's metadata conditions"""

        # apply_metadata_filters treats an empty list as a pass-through (matches everything),
        # we don't want that here
