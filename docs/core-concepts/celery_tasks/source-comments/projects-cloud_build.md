def _set_seqera_error(project, message: str) -> None:
    """Persist a Seqera provisioning error message on the project (truncated)."""


def create_seqera_workspace(project, seqera_client):
    """
    Create a Seqera workspace for the given project.

    Args:
        project (Project): The project to create the workspace for
        seqera_client (SeqeraClient): The Seqera client to use

    Returns:
        dict: The workspace data if successful, None otherwise
    """


def create_seqera_credentials(project, workspace_id, seqera_client):
    """
    Create Seqera credentials for the project using the service account key.

    Args:
        project (Project): The project to create credentials for
        workspace_id (str): The ID of the workspace to create credentials in
        seqera_client (SeqeraClient): The Seqera client to use

    Returns:
        dict: The credentials data if successful, None otherwise
    """


def create_seqera_compute_environment(project, workspace_id, seqera_client, credentials_id=None):  # noqa: C901
    """
    Create a Seqera compute environment for the given project in the given workspace.

    Args:
        project (Project): The project to create the compute environment for
        workspace_id (str): The ID of the workspace to create the compute environment in
        seqera_client (SeqeraClient): The Seqera client to use
        credentials_id (str, optional): The ID of the credentials to use with the compute environment

    Returns:
        dict: The compute environment data if successful, None otherwise
    """


def create_seqera_data_link(project, workspace_id, seqera_client, credentials_id=None):
    """
    Create a Seqera data link for the given project's output bucket.

    Args:
        project (Project): The project to create the data link for
        workspace_id (str): The ID of the workspace to create the data link in
        seqera_client (SeqeraClient): The Seqera client to use
        credentials_id (str, optional): The ID of the credentials to use with the data link

    Returns:
        dict: The data link data if successful, None otherwise
    """


# Max retries set to 24 (up to 2 hours with default 5 min retry delay)
@shared_task(bind=True, max_retries=24)
def poll_cloud_build_status(self, build_id, project_id, location, project_id_db):  # noqa: C901, PLR0911, PLR0912, PLR0915
    """
    Poll the status of a Cloud Build build and perform actions based on the result.

    Args:
        build_id (str): The ID of the build
        project_id (str): The GCP project ID
        location (str): The location of the build (e.g., 'us-central1')
        project_id_db (int): The database ID of the project

    Returns:
        str: The final status of the build
    """

    except Retry:
        # ``self.retry(...)`` raises ``celery.exceptions.Retry`` from inside the
        # ``try`` above to schedule the next poll. It's a normal control-flow
        # signal, NOT a real error — never persist it as ``last_build_error``
        # and never re-call ``self.retry()`` from here. Just let Celery handle it.
    except Exception as e:
        # Persist the failure on the project so it surfaces in the UI. Best-effort:
        # capture_build_error never raises, but Project.objects.get may, so guard it.


@shared_task
def sync_seqera_workspace_access(project_ids: list[int] | int) -> bool:
    """
    Celery task to synchronize Seqera workspace access for one or more projects.
    This ensures all users with appropriate permissions have access to the workspace.

    Args:
        project_ids: Either a single project ID or a list of project IDs to sync workspace access for

    Returns:
        bool: True if all syncs were successful, False if any failed
    """


@shared_task
def handle_adhs_user_access(user_id: int, action: str) -> bool:
    """
    Handle ADHS user access to all projects.
    This task is responsible for:
    1. Adding/removing ProjectUser entries for all projects
    2. Triggering workspace sync for affected projects

    Args:
        user_id: The ID of the user being added/removed from ADHS
        action: Either 'add' or 'remove'

    Returns:
        bool: True if all operations were successful, False otherwise
    """


@shared_task
def handle_new_project_adhs_access(project_id: int) -> bool:
    """
    Handle ADHS user access for a new project.
    This task is responsible for:
    1. Adding all ADHS users to the new project
    2. Triggering workspace sync

    Args:
        project_id: The ID of the new project

    Returns:
        bool: True if all operations were successful, False otherwise
    """
