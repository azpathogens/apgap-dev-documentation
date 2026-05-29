

class FileRenameNotAllowedError(ValueError):
    """Raised when a file rename operation is not allowed."""


def _validate_file_rename_allowed(old_instance: File) -> None:
    """
    Validate that a file is allowed to be renamed.

    Raises FileRenameNotAllowedError if the file cannot be renamed.
    """


def _perform_gcs_rename(bucket_name: str, old_path: str, new_path: str, file_pk: int) -> None:
    """
    Perform the actual GCS blob rename operation (copy + delete).
    """


@receiver(pre_save, sender=File)
def rename_gcs_blob_on_path_change(sender, instance, **kwargs):
    """
    Rename the GCS blob when a file's gcs_file_path changes.

    This signal detects when the gcs_file_path has changed and renames
    the underlying GCS blob by copying it to the new location and deleting
    the old one.

    Only files in DRAFT status can have their path changed.
    Files that are copies (in analytical datasets) cannot be renamed.
    """


# NOTE: This signal is disabled. File status promotion to PRIMARY is now handled
# via the manual set-primary endpoint and File.promote_to_primary() method.
# See: File.check_primary_eligibility() and File.promote_to_primary() in models.py
#
# @receiver(models.signals.m2m_changed, sender=File.file_metadata_tags.through)
# def update_file_status_on_metadata_change(sender, instance, action, pk_set, **kwargs):
#     """
#     Update file status based on metadata requirements when metadata tags are added or removed.
#
#     Checks if all required metadata templates are fulfilled:
#     - Core templates (source_type=None) apply to all files
#     - Source-specific templates apply only to files with matching source_type
#     - Metadata tags with source_type=None or matching file's source_type are considered
#     - File is promoted to PRIMARY when all required metadata is present
#     - File is demoted to DRAFT when required metadata is missing
#     """
#     logger.info("\n\n\nrunning update file status signal")
#     # Only process post_add and post_remove actions
#     if action not in ["post_add", "post_remove", "post_clear"]:
#         return
#
#     # instance is the File object when using m2m_changed
#     file = instance
#
#     # Skip if file is not in DRAFT or PRIMARY status
#     if file.status not in [FileStatus.DRAFT, FileStatus.PRIMARY]:
#         logger.debug(f"File {file.id} is not in DRAFT or PRIMARY status, skipping metadata check")
#         return
#
#     # Get all required metadata templates for this file's source type
#     # Include both core templates (source_type=None) and source-specific templates
#     required_templates = (
#         MetadataTemplate.objects.filter(is_required=True)
#         .filter(models.Q(source_type=None) | models.Q(source_type=file.source_type))
#         .select_related("key")
#     )
#
#     # If no required templates exist, nothing to check
#     if not required_templates.exists():
#         logger.debug(f"No required metadata templates found for file {file.id}")
#         return
#
#     # Get all metadata keys currently associated with the file (matching source_type)
#     # Consider metadata tags that either:
#     # - Have no source_type (None) - for backward compatibility
#     # - Have the same source_type as the file
#     file_metadata_keys = set(
#         file.file_metadata_tags.through.objects.filter(
#             models.Q(file=file) & (models.Q(source_type=None) | models.Q(source_type=file.source_type)),
#         )
#         .select_related("metadata_tag__key")
#         .values_list("metadata_tag__key__id", flat=True),
#     )
#
#     # Get all required key IDs from templates
#     required_key_ids = set(required_templates.filter(key__isnull=False).values_list("key__id", flat=True))
#
#     # Check if all required keys are present
#     metadata_complete = required_key_ids.issubset(file_metadata_keys)
#
#     # Update file status based on metadata completeness
#     if metadata_complete and file.status == FileStatus.DRAFT:
#         # All required metadata is present, promote to PRIMARY
#         file.status = FileStatus.PRIMARY
#         file.save(update_fields=["status", "updated_at"])
#         logger.info(
#             f"File {file.id} has all required metadata "
#             f"(source_type: {file.source_type.name if file.source_type else 'None'}). "
#             f"Status updated from DRAFT to PRIMARY",
#         )
#
#     elif not metadata_complete and file.status == FileStatus.PRIMARY:
#         # Required metadata is missing, demote to DRAFT
#         file.status = FileStatus.DRAFT
#         file.save(update_fields=["status", "updated_at"])
#         missing_keys = required_key_ids - file_metadata_keys
#         logger.info(
#             f"File {file.id} is missing {len(missing_keys)} required metadata keys "
#             f"(source_type: {file.source_type.name if file.source_type else 'None'}). "
#             f"Status reverted from PRIMARY to DRAFT",
#         )
#     elif file.status == FileStatus.DRAFT:
#         missing_keys = required_key_ids - file_metadata_keys
#         logger.debug(f"File {file.id} remains in DRAFT. Missing {len(missing_keys)} required keys: {missing_keys}")
#     else:
#         logger.debug(f"File {file.id} remains in PRIMARY. All required metadata present.")


def update_file_status_on_metadata_change(sender, instance, action, pk_set, **kwargs):
    """
    Placeholder function kept for import compatibility.
    The actual signal is disabled - status changes are now manual via set-primary endpoint.
    """


# @receiver(post_save, sender=File)
# def trigger_dlp_scan_signal(sender, instance, created, **kwargs):
#     """
#     Trigger DLP scan when a new file is created with PROCESSING status.
#     """
#     if created and instance.status == FileStatus.PROCESSING and settings.ENABLE_GCP_INTERACTIONS:
#         logger.info(f"Triggering DLP scan for new file {instance.id}")
#         # Queue the DLP scan task
#         trigger_dlp_scan.delay(instance.id)


@receiver(post_save, sender=File)
def notify_file_status_change(sender, instance, created, **kwargs):
    """
    Send notifications when file status changes to important states.
    """


@receiver(post_save, sender=File)
def notify_file_created(sender, instance, created, **kwargs):
    """
    Send notifications when a new file is uploaded to a lab.
    """


@receiver(pre_delete, sender=File)
def cleanup_gcs_file(sender, instance, **kwargs):
    """
    Clean up GCS file when a File record is deleted.
    This is optional and can be disabled if you want to keep files in GCS after deletion.
    """
