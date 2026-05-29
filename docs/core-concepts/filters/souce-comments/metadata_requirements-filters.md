

class SourceTypeFilter(django_filters.FilterSet):
    """
    Filter class for SourceType model.
    Allows filtering by name with various lookup expressions.
    """


class MetadataRequirementFilter(django_filters.FilterSet):
    """
    Filter class for MetadataRequirement model.
    Provides comprehensive filtering options for metadata requirements.
    """

    def filter_applies_to_all(self, queryset, name, value):
        """Filter for requirements that apply to all source types."""

    def filter_specific_type_only(self, queryset, name, value):
        """Filter for requirements that apply to specific source types only."""


class MetadataRequirementAdvancedFilter(MetadataRequirementFilter):
    """
    Extended filter with additional complex filtering options.
    """

    def filter_search(self, queryset, name, value):
        """Search across multiple fields."""


class MetadataTemplateFilter(django_filters.FilterSet):
    """
    Filter class for MetadataTemplate model.
    Allows filtering by source_type and is_core.
    """
