class ArchiveRequestPermission(permissions.BasePermission):
    """
    Custom permission for archive requests.

    - Create: User must be the original uploader (created_by) of the target File
    - Approve/Deny: User must be Lab Director (is_lab_admin=True) of the File's lab
    - List: Users see their own requests + Lab Directors see requests for their labs
    - Retrieve: User is requester or Lab Director of the file's lab
    - Global admins can do everything
    """

    def has_permission(self, request, view):
        """
        Check if user has permission to perform the action.
        """

    def has_object_permission(self, request, view, obj):  # noqa: PLR0911
        """
        Check if user has permission to access a specific archive request.
        """

    def _get_file_from_archive_request(self, archive_request):
        """
        Get the File object from an archive request.
        Returns None if the archive request is not for a File.
        """

    def _is_lab_director_for_file(self, user, file):
        """
        Check if the user is a lab director for the file's lab.
        """
