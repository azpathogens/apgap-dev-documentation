class OrganizationViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        """
        Use detail serializer for retrieve action, patch serializer for partial_update action,
        list serializer for list action.
        """

    def partial_update(self, request, *args, **kwargs):
        """
        PATCH endpoint that only allows updating default_approve_analytical_dataset_requests.
        """

    def perform_destroy(self, instance):
        """
        Soft delete: Set active=False instead of actually deleting the organization.
        Deletion is prevented if organization has users (checked at model level and here).
        """
