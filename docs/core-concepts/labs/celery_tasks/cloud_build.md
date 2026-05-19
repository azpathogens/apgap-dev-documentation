# Max retries set to 24 (up to 2 hours with default 5 min retry delay)
@shared_task(bind=True, max_retries=24)
def poll_lab_cloud_build_status(self, build_id, project_id, location, lab_id_db):
    """
    Poll the status of a Cloud Build build and perform actions based on the result.

    Args:
        build_id (str): The ID of the build
        project_id (str): The GCP project ID
        location (str): The location of the build (e.g., 'us-central1')
        lab_id_db (int): The database ID of the lab

    Returns:
        str: The final status of the build
    """

    # Get the request ID or use a default value for tests
    # self.request might be None or missing the id attribute in tests

    except Retry:
        # ``self.retry(...)`` raises ``celery.exceptions.Retry`` from inside the
        # ``try`` above to schedule the next poll. It's a normal control-flow
        # signal, NOT a real error — never persist it as ``last_build_error``
        # and never re-call ``self.retry()`` from here. Just let Celery handle it.
        raise
    except Exception as e:
        # Persist the failure on the lab so it surfaces in the UI. Best-effort:
        # capture_build_error never raises, but Lab.objects.get may, so guard it.
        # Release the lock before retrying
