@receiver(post_save, sender=Dataset)
def create_gcs_buckets(sender, instance, created, **kwargs):  # noqa: C901, PLR0912, PLR0915
    """
    Create GCS buckets for datasets after they are created.

    For single GUI upload:
    - Creates a target bucket in the project's GCP project

    For batch:
    - Creates an ingest bucket in the DataOps project
    - Creates a target bucket in the project's GCP project
    - Creates a batch service account in the project's GCP project
    - Grants IAM permissions to the project's default service account on the ingest bucket
    - Grants IAM permissions to the batch service account on the target bucket
    - Creates a pub/sub topic for bucket notifications
    - Configures bucket notifications to the pub/sub topic
    """


@receiver(pre_delete, sender=Dataset)
def cleanup_gcs_buckets(sender, instance, **kwargs):  # noqa: C901, PLR0912, PLR0915
    """
    Clean up GCS buckets, IAM bindings, and pub/sub resources when a dataset is deleted.

    For single GUI upload:
    - Preserves the target bucket for archival purposes

    For batch:
    - Removes IAM bindings from the ingest bucket
    - Deletes the ingest bucket
    - Preserves the target bucket for archival purposes
    - Deletes the pub/sub topic and subscription
    - Deletes the batch service account key secret
    - Deletes the batch service account
    """


@receiver(m2m_changed, sender=Dataset.assigned_projects.through)
def handle_dataset_project_assignment(sender, instance, action, reverse, model, pk_set, **kwargs):  # noqa: PLR0913, C901, PLR0912, PLR0915
    """
    Handle IAM permissions and Seqera data links when projects are assigned/unassigned to datasets.

    When a project is assigned:
    1. Grant IAM permissions to the project's default service account on the dataset's buckets
    2. Create a Seqera data link in the project's workspace for the dataset's bucket

    When a project is unassigned:
    1. Delete the Seqera data link from the project's workspace
    2. Remove IAM permissions from the project's default service account on the dataset's buckets
    """
