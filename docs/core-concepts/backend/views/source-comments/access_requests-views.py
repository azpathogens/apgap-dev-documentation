
class OptionalPageNumberPagination(PageNumberPagination):
    
    Only paginate if ?pagination=true is present.
    Otherwise return full list.
    


class AccessRequestViewSet(viewsets.ModelViewSet):
    
    ViewSet for managing access requests.

    Provides CRUD operations for access requests with appropriate permissions:
    - Users can create access requests for themselves
    - Users can view their own access requests
    - Approvers can view access requests they need to approve
    - Global admins can view and manage all access requests

    Features:
    - Filtering by user, status, analytical dataset, file
    - Searching by user email, analytical dataset name, file name
    - Optional pagination
    - Custom actions for approving and rejecting requests
    


    def get_serializer_class(self):
        
        Return the appropriate serializer based on the action.
        

    def _get_optimized_queryset(self, queryset):
        
        Apply select_related and prefetch_related optimizations to reduce N+1 queries.
        

    def get_queryset(self):
        
        Filter access requests to only those the user has access to view.
        Uses the User model's get_access_requests() method for consistent permission filtering.
        

    def perform_create(self, serializer):
        
        Log access request creation.
        

    def perform_update(self, serializer):
        
        Log access request updates.
        

    def destroy(self, request, *args, **kwargs):
        
        Delete an access request.
        

    @action(detail=True, methods=["post"], url_path="approve")
    def approve(self, request, pk=None):
        
        Approve an access request.

        Only approvers assigned to this request can approve it.
        

    @action(detail=True, methods=["post"], url_path="reject")
    def reject(self, request, pk=None):
        
        Reject an access request.

        Only approvers assigned to this request can reject it.
        

    @action(detail=False, methods=["get"], url_path="my-requests")
    def my_requests(self, request):
        
        Get all access requests created by the current user.
        Only returns access requests for files in active labs.
        

    @action(detail=False, methods=["get"], url_path="pending-approvals")
    def pending_approvals(self, request):
        
        Get all pending access requests that the current user needs to approve.
        Only returns access requests for files in active labs.
        
