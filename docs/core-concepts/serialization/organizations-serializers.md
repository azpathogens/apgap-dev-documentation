
class OrganizationDetailSerializer(serializers.ModelSerializer):

    def get_has_users(self, obj):
        """
        Return True if organization has any users in labs or projects.
        """


class OrganizationPatchSerializer(serializers.ModelSerializer):
    """
    Serializer for PATCH endpoint that allows updating default_approve_analytical_dataset_requests and display_name.
    Extra fields are silently ignored.
    """

    def to_internal_value(self, data):
        """
        Filter out any fields that aren't in the allowed list before validation.
        This allows extra fields to be silently ignored.
        """
