def add_lab_to_sequencing_lab_metadata(lab):
    """Add a newly created lab's display name as an option in the sequencing lab metadata template.

    Imports are deferred to avoid circular dependencies between the labs and metadatatags apps.
    """


@receiver(post_save, sender=Lab)
def trigger_gcp_lab_project_creation(sender, instance, created, **kwargs):
    """Trigger GCP project creation when a new lab is created."""
    # Generate and save project prefix if not already set
    # Trigger the Cloud Build

    # ``trigger_cloud_build`` itself can raise (network/IAM/etc.) before
    # any build is submitted. Capture the failure on the lab so the UI's
    # "Build logs" affordance can show it; preserve the existing
    # raise-on-falsy behavior below so callers that depend on it (the
    # API layer) still see the failure.
