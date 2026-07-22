@receiver(post_save, sender=Project)
def handle_project_archived(sender, instance, created, **kwargs):
    """
    Handle archiving behavior when a project is archived.

    This signal ensures that archiving behavior happens regardless of how
    the project is archived (via API, Django admin, etc.).

    The behavior is delegated to ProjectArchiveService.process_archiving_behavior()
    to keep all business logic in the service layer.

    The method is idempotent, so it's safe to call multiple times.
    """


@receiver(post_save, sender=Project)
def trigger_gcp_project_creation(sender, instance, created, **kwargs):
    """Trigger GCP project creation when a new project is created."""

    # ``trigger_cloud_build`` itself can raise (network/IAM/etc.) before
    # any build is submitted. If it does, we must surface it on the
    # project so the UI's "Build logs" affordance can show it — otherwise
    # the project just looks stuck forever with no feedback.


@receiver(pre_delete, sender=Project)
def delete_notification(sender, instance, **kwargs):
    """
    Create notification for project deletion.

    This signal handler creates notifications for all project deletions,
    whether via API, Django admin, or other means. It includes platform
    admins and justification (if available) in the notification.

    Using pre_delete ensures we have access to all related objects before
    CASCADE deletions occur.
    """


@receiver(post_save, sender=ProjectUser)
def notify_project_user_updated(sender, instance, created, **kwargs):


@receiver([post_save, post_delete], sender=ProjectUser)
def handle_project_user_changes(sender, instance, **kwargs):
    """
    Handle Seqera workspace access when project users are added or removed.
    This will trigger a full sync of workspace access to ensure all users
    with appropriate permissions have access.
    """


@receiver([post_save, post_delete], sender=LabUser)
def handle_lab_user_changes(sender, instance, **kwargs):
    """
    Handle Seqera workspace access when lab users are added or removed.
    This will trigger a full sync of workspace access for all projects in the lab
    to ensure all users with appropriate permissions have access.
    """


@receiver([post_save, post_delete], sender=ProjectUser)
def handle_notebook_viewer_for_project_user(sender, instance, **kwargs):
    """Sync notebook viewer IAM at project level when project users are added or removed."""


@receiver([post_save, post_delete], sender=LabUser)
def handle_notebook_viewer_for_lab_user(sender, instance, **kwargs):
    """Sync notebook viewer IAM at project level when lab directors are added or removed."""
