
class SourceTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for SourceType model.
    Handles the various sample source types in the system.
    """


class MetadataRequirementSerializer(serializers.ModelSerializer):
    """
    Serializer for MetadataRequirement model.
    Provides both write (using IDs) and read (nested) representations.
    """

    class Meta:

    def get_display_name(self, obj):
        """Generate a human-readable display name for the requirement."""

    def validate(self, attrs):
        """Validate unique constraint for key and source_type combination."""


class MetadataRequirementListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for list views.
    Provides essential information without heavy nested objects.
    """


class MetadataTemplateOptionSerializer(serializers.ModelSerializer):
    """
    Nested serializer for options in metadata templates.

    Gets both name and value from the Value model's name field.
    MetadataTemplateOption has a ForeignKey to Value, and Value has a 'name' field.
    """


class MetadataTemplateSerializer(serializers.ModelSerializer):
    """
    Serializer for MetadataTemplate model.
    Returns the template with all required fields including options from the through table.

    Performance optimizations:
    - Uses direct CharField with source for source_type_name instead of SerializerMethodField
    - Relies on select_related("key", "source_type") in the view's get_queryset()
    """

    def get_name(self, obj):
        """Return the template name, falling back to key name if not set.

        Note: This uses SerializerMethodField because it requires fallback logic
        (template.name -> key.name -> ""). The key is already loaded via select_related.
        """


class MetadataTemplateWriteSerializer(serializers.ModelSerializer):
    """
    Base serializer for writing MetadataTemplate (POST and PATCH).
    Handles common fields and get-or-create logic for Values.
    """

    def _validate_and_process_values(self, values, key):
        """Validate values against key's data_type and return normalized list.

        The list index determines the sort_order, regardless of any sort_order
        value provided in the API request.
        """

    def _update_template_options(self, template, values):
        """Update or create MetadataTemplateOption entries for the given values.

        The list order determines the sort_order. Options not in the list are deleted.
        """

    def to_representation(self, instance):
        """Return full template representation using the read serializer."""


class MetadataTemplatePOSTSerializer(MetadataTemplateWriteSerializer):
    """
    Serializer for creating MetadataTemplate via POST.
    Extends base serializer with key_name and data_type fields.
    """

    def validate_key_name(self, value):
        """Normalize the key name."""

    def validate(self, attrs):
        """Validate key existence and data type consistency."""

    def create(self, validated_data):
        """Create MetadataTemplate with get-or-create logic for Key and Values."""


class MetadataTemplatePATCHSerializer(MetadataTemplateWriteSerializer):
    """
    Serializer for updating MetadataTemplate via PATCH.
    Allows updating the template name and other fields.
    """

    def validate(self, attrs):
        """Validate values against the existing key's data_type."""

        # the frontend pre-fills name from the get response and re-sends it on
        # every patch, so an unchanged value would otherwise re-run the uniqueness
        # check and 400 whenever two rows already share a name+source_type. only
        # run the check when the admin is actually renaming to a new value
        # (if they're just editing the values list name dosent matter)
        # when the check does run, it still filters by (name, source_type)

    def update(self, instance, validated_data):
        """Update MetadataTemplate with get-or-create logic for Values."""
