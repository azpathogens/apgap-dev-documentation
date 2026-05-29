class LabDeletionService:
    """Service for deleting labs whose GCP builds have failed."""

    def delete_failed_lab(lab: Lab, deleted_by) -> tuple[bool, str]:
        """
        Delete a lab whose build has failed.

        Only labs with a build_status of FAILURE, TIMEOUT, or CANCELLED can be deleted.
        This triggers GCP resource cleanup (terraform destroy) and removes the
        database record along with associated LabUser records (via CASCADE).

        Args:
            lab: The Lab instance to delete
            deleted_by: The User performing the deletion

        Returns:
            tuple: (success: bool, message: str)
        """


class LabResourceCleanupService:
    """Service for cleaning up GCP resources associated with labs."""

    @staticmethod
    def cleanup_gcp_resources(lab: Lab) -> None:
        """
        Trigger cleanup of GCP resources for a lab.

        Triggers a Cloud Build destroy trigger to tear down the lab's
        GCP project and associated resources via Terraform.

        Args:
            lab: The Lab instance
        """
