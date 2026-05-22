def _normalize_pubsub_generation(message: dict) -> str:
    """Return GCS object generation from Pub/Sub OBJECT_FINALIZE payload as a string."""


def _safe_file_size_from_message(message: dict):
    """Parse OBJECT_FINALIZE size (bytes). Returns None when absent."""


class OptionalPageNumberPagination(PageNumberPagination):
    """
    Only paginate if ?pagination=true is present.
    Otherwise return full list.
    """


class UploadViewSet(viewsets.ModelViewSet):
    """ViewSet for GUI uploads with basic CRUD operations."""

    def get_queryset(self):
        """Filter uploads based on user's lab access."""

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""

    def perform_create(self, serializer):
        """Set the user when creating an upload."""

    @action(detail=True, methods=["get"])
    def upload_url(self, request, pk=None):
        """Get the signed upload URL for a GUI upload.

        Note: This endpoint is kept for backward compatibility.
        The upload_url is now automatically included in POST response.
        """


class BatchUploadViewSet(viewsets.ModelViewSet):
    """ViewSet for batch uploads with basic CRUD operations."""

    def get_queryset(self):
        """Filter batch uploads based on user's access level."""

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""

    def perform_create(self, serializer):
        """Set the user when creating an upload."""

    @action(detail=True, methods=["get"])
    def download_service_account_key(self, request, pk=None):
        """Download the actual service account key for batch upload.

        Query parameters:
        - as_file: If 'true', returns the key as a downloadable JSON file.
                   Otherwise, returns as JSON response.
        """


class IngestNotificationViewSet(viewsets.ViewSet):
    """
    A ViewSet for handling pub/sub push notifications for batch ingest buckets.
    Triggers DLP scans for uploaded files.
    """

    def create(self, request):
        """
        Handle pub/sub push notifications for batch ingest bucket.
        Triggers DLP scan for the uploaded file.
        """


@csrf_exempt
@require_http_methods(["PUT"])
@api_view(["PUT"])
# Allow any for local dev - mimics GCS signed URL
@permission_classes([AllowAny])
def local_upload_handler(request, ingest_uuid):
    """
    Local development endpoint to emulate GCP bucket PUT uploads.

    This function mimics the behavior of uploading to a GCS signed URL,
    allowing frontend applications to test file uploads in local development
    without requiring actual GCP infrastructure.

    Args:
        request: The HTTP request containing the file data
        ingest_uuid: The UUID of the upload (matches ingest_uuid in the model)

    Returns:
        HTTP response indicating success or failure
    """
