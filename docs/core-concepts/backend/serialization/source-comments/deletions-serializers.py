
class ArchiveRequestFileSerializer(serializers.ModelSerializer):
    """
    Lightweight nested serializer for File in archive request list view.
    """


class ArchiveRequestListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing archive requests.
    """

    def get_file(self, obj):
        """
        Get nested file serializer if the content object is a File.
        """

    def get_description(self, obj):
        """
        Get the description from the file being archived.
        """

    def get_lab_name(self, obj):
        """
        Get the lab name from the file being archived.
        """


class ArchiveRequestDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for archive request information.
    """

    def get_object_details(self, obj):
        """
        Get details about the object being archived.
        For Files, includes filename, lab, created_at, etc.
        """

    def get_description(self, obj):
        """
        Get the description from the file being archived.
        """

    def get_lab_directors(self, obj):
        """
        Get list of lab directors for the file's lab.
        """


class ArchiveRequestCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating archive requests.

    Validates:
    - The requester is the original uploader of the file
    - External storage location is provided if retention requirement is not met
    """

    def validate_file_id(self, value):
        """
        Validate that the file exists and the requester has permission to request archiving.

        Permission is granted if the requester is:
        - The original uploader of the file (any file status), OR
        - A lab director of the lab that owns the file (for PRIMARY files only), OR
        - A platform admin (for PRIMARY files only)
        """

    def validate(self, data):
        """
        Validate that external storage is provided if retention requirement is not met.
        """

    def create(self, validated_data):
        """
        Create the archive request with the file as the content object.
        """


class ArchiveRequestApproveSerializer(serializers.Serializer):
    """
    Serializer for approving an archive request.
    No additional fields required - approval is just an action.
    """


class ArchiveRequestDenySerializer(serializers.Serializer):
    """
    Serializer for denying an archive request.
    """


class DeletionSerializer(serializers.ModelSerializer):
    """
    Serializer for Deletion model.
    Provides read-only access to deletion records.
    """


class DeletionSummarySerializer(serializers.ModelSerializer):
    """
    Simplified serializer for Deletion model list views.
    """
