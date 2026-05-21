"""
Service layer for project archiving and deletion operations.

This module contains business logic for archiving and hard deleting projects,
separated from the API views for better testability and reusability.
"""


class ProjectArchiveService:
    """Service for archiving projects."""

    @staticmethod
    def process_archiving_behavior(project: Project) -> tuple[int, str]:
        """
        Process archiving behavior for a project.

        This method handles all the side effects of archiving:
        - Sets archived_at timestamp if not already set
        - Deleting analytical datasets
        - Triggering async cleanup of GCP resources
        - Triggering async cleanup of Seqera workspace

        This method is idempotent - it only processes datasets if they exist,
        and cleanup methods are safe to call multiple times.

        Args:
            project: The Project instance that was archived

        Returns:
            tuple: (dataset_count: int, message: str)
        """
    @staticmethod
    @transaction.atomic
    def archive_project(project: Project, archived_by) -> tuple[bool, str]:
        """
        Archive a project.

        This method updates the project status and metadata.
        The archiving behavior (deleting datasets, cleanup) handled by the post_save signal

        Args:
            project: The Project instance to archive
            archived_by: The User who is archiving the project

        Returns:
            tuple: (success: bool, message: str)
        """


class ProjectDeletionService:
    """Service for hard deleting projects."""

    @staticmethod
    @transaction.atomic
    def hard_delete_project(project: Project, deleted_by, justification: str) -> tuple[bool, str]:
        """
        Hard delete a project.

        This method:
        1. Validates that justification is provided
        2. Deletes all analytical datasets associated with the project
        3. Triggers async cleanup of GCP resources
        4. Triggers async cleanup of Seqera workspace
        5. Logs the deletion with justification
        6. Actually deletes the project record from the database

        Args:
            project: The Project instance to delete
            deleted_by: The User who is deleting the project
            justification: Required justification for the deletion

        Returns:
            tuple: (success: bool, message: str)
        """


class ProjectResourceCleanupService:
    """Service for cleaning up external resources (GCP, Seqera) associated with projects."""

    @staticmethod
    def cleanup_gcp_resources(project: Project) -> None:
        """
        Trigger cleanup of GCP resources for a project.

        Triggers Cloud Build destroy trigger to delete GCP project and associated resources.

        Args:
            project: The Project instance
        """

    @staticmethod
    def cleanup_seqera_workspace(project: Project) -> None:
        """
        Cleanup Seqera workspace for a project.

        Deletes the Seqera workspace associated with the project.

        Args:
            project: The Project instance
        """
