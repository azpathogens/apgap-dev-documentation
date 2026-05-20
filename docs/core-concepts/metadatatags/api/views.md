class MetadataTagViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing metadata tags.
    Only accessible by platform administrators.
    """

    def get_queryset(self):
        """
        Optionally filter by key or value.
        Returns results ordered alphabetically by value name.
        """

    @action(detail=False, methods=["get"], url_path="keys")
    def keys(self, request):
        """List all predefined metadata Keys (for bulk-upload dropdown)."""

    @action(
        detail=False,
        methods=["post"],
        url_path="upload-values-csv",
        parser_classes=[MultiPartParser, FormParser],
    )
    def upload_values_csv(self, request):
        """
        Bulk-create Value rows + MetadataTag rows for a single Key from a CSV.

        Request (multipart):
        - csv_file: CSV with a single 'value' column
        - key: ID of the Key all values will be tagged under

        Returns success/error counts; status 201 on full success,
        207 on partial success, 400 if every row failed.
        """
