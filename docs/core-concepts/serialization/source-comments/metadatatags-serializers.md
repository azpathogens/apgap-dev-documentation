class KeySerializer(serializers.ModelSerializer):
    """
    Serializer for Key model.
    Handles predefined metadata keys.
    """


class MetadataTagSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        """
        Create a new metadata tag, creating Key and Value if they don't exist.
        """

    def validate(self, attrs):
        """
        Convert string key and value names to Key and Value objects before validation.
        """

    def update(self, instance, validated_data):
        """
        Update a metadata tag.
        """

    def to_representation(self, instance):
        """
        Convert the instance to a representation that includes the key and value names.
        """


class BulkValueUploadSerializer(serializers.Serializer):
    """
    Request body for POST /api/metadata-tags/upload-values-csv/.
    """
