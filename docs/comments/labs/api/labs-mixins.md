from asu_apgap.labs.api.serializers import LabListSerializer from asu_apgap.labs.api.serializers import LabPostPatchSerializer
from asu_apgap.labs.api.serializers import LabSerializer


class DetermineLabSerializerMixin:
    def get_serializer_class(self, *arg, **kwargs):
        if self.request.method in ["POST", "PATCH"]:
            return LabPostPatchSerializer
        if getattr(self, "action", None) == "list":
            return LabListSerializer
        return LabSerializer
