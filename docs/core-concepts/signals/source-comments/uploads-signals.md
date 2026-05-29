

@receiver(post_save, sender=BatchUpload)
def create_gcs_buckets_for_batch_upload(sender, instance, created, **kwargs):
    """
    Create ingest GCS buckets for BatchUploads after they are created.
    For batch:
    - Creates an ingest bucket in the DataOps project
    - Grants IAM permissions to the project's default service account on the ingest bucket
    - Creates a pub/sub topic for bucket notifications
    - Configures bucket notifications to the pub/sub topic
    """
