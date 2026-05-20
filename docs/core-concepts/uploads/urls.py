from asu_apgap.uploads.api.views import local_upload_handler
from asu_apgap.uploads.api.views import UploadViewSet
from asu_apgap.uploads.api.views import IngestNotificationViewSet
from asu_apgap.uploads.api.views import BatchUploadViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path
rom django.urls import include


app_name = "uploads"

router = DefaultRouter()
router.register(r"batch-uploads", BatchUploadViewSet, basename="batchupload")
router.register(r"ingest-notifications",
                IngestNotificationViewSet, basename="ingestnotification")
router.register("", UploadViewSet, basename="upload")

urlpatterns = [
    path("", include(router.urls)),
    path("local-upload/<uuid:ingest_uuid>/",
         local_upload_handler, name="local-upload"),
]
