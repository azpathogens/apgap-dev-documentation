def _sync_single_project(task, project, client):
    """
    Sync notebook viewer IAM for a single project.

    Uses the model properties (which fall back to reading the Terraform state
    from GCS) instead of raw DB fields, so each Celery retry re-polls for
    values that may not have been cached yet.

    Returns True if sync succeeded or was skipped, False if it failed.

    Raises:
        Retry: If the notebook SA email is not yet available and the task should retry.
    """


class _NotebookSyncTask(Task):
    """Celery base task that records terminal failures on each affected project."""


@shared_task(bind=True, base=_NotebookSyncTask, max_retries=5, default_retry_delay=30)
def sync_notebook_viewer_access(self, project_ids: list[int] | int) -> bool:
    """
    Celery task to sync notebook viewer IAM at the GCP project level for one or more projects.

    Reconciles the configured role (e.g. roles/notebooks.viewer) on each project's
    GCP project so that current project members and lab directors have access.

    If a project's notebook SA email is not yet available (e.g. due to a race condition
    where the cache has not yet been populated), the task will automatically retry with
    exponential backoff (30s, 60s, 120s, 240s, 300s) up to 5 times.

    Args:
        project_ids: A single project ID or list of project IDs.

    Returns:
        True if all syncs succeeded, False if any failed.
    """
