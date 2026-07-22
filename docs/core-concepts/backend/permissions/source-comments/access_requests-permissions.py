

class AccessRequestPermission(permissions.BasePermission):

    Custom permission for access requests.

    - Users can create their own access requests(Platform Admin, Lab Director, Bioinformatics User)
    - Users can view their own access requests
    - Lab Directors can view access requests for their lab data
    - Approvers can view access requests assigned to them
    - Users can update/delete their own pending access requests
    - Lab Directors can approve/reject access requests for their lab data
    - Platform Admins can do everything
