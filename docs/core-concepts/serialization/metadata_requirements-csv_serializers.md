"""
CSV-specific serializers for metadata template export and import.
"""


class CSVTemplateDownloadSerializer(serializers.Serializer):
    """
    Serializer for CSV template download request.
    """


class CSVMetadataUploadSerializer(serializers.Serializer):
    """
    Serializer for CSV metadata upload request.
    """

    def validate_csv_file(self, value):
        """Validate the uploaded file is a CSV."""


class CSVUploadResultSerializer(serializers.Serializer):
    """
    Serializer for CSV upload result response.
    """


class CSVValidationResultSerializer(serializers.Serializer):
    """
    Serializer for CSV validation result response.
    """
