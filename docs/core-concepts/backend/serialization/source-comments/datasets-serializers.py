class DatasetListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing datasets with summary information.
    Includes file count and total size instead of the complete file list.
    """

    def get_metadata_tags(self, obj):
        """
        Custom method to serialize dataset metadata tags.
        """


class DatasetDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed dataset information.
    Includes complete file list using the model's all_files property.
    """

    def get_files(self, obj):
        """
        Get all files for the dataset using the all_files property.
        """
        return obj.all_files

    def get_metadata_tags(self, obj):
        """
        Custom method to serialize dataset metadata tags.
        """


class DatasetCreateSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        """
        Create a new dataset and set the created_by user.
        Also handle metadata tag assignments.
        """


class DatasetPatchSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a dataset.
    """


class DatasetBladeViewSerializer(serializers.ModelSerializer):
    """
    Serializer for the blade view endpoint which provides a detailed view
    of a dataset including metadata tags, file preview, and project information.
    """

    def get_metadata_tags(self, obj):
        """Get metadata tags as key-value pairs."""

    def get_owning_project(self, obj):
        """Format the owning project with lab name."""

    def get_projects_with_access(self, obj):
        """Get all projects with access to this dataset."""
