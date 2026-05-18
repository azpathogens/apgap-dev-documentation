class File(models.Model):
    """
    Model representing individual files associated with a Lab.
    Files are uploaded to GCS and tracked in the database.
    """

    @property
    def filename(self):
        """
        Extract the filename from the GCS path.
        """

    @property
    def lab_gcs_bucket(self):
        """
        Get the GCS bucket name for lab files.
        """

    @property
    def full_gcs_path(self):
        """
        Get the full GCS path including bucket.
        """

    @property
    def full_ingest_path(self):
        """
        Get the full GCS ingest path (same as full_gcs_path for lab files).
        This property is provided for consistency with DatasetFile.
        """

    @property
    def is_processing(self):
        """
        Check if the file is still being processed.
        """

    @property
    def is_uploaded(self):
        """
        Check if the file has been successfully uploaded.
        """

    @property
    def has_pii(self):
        """
        Check if the file has been flagged for containing PII.
        """

    @property
    def has_failed(self):
        """
        Check if the file processing has failed.
        """

    @property
    def is_archived(self):
        """
        Check if the file has been archived.
        """

    @property
    def is_deleted(self):
        """
        Check if the file has been marked as deleted (for copies when original is hard-deleted).
        """

    @property
    def meets_retention_requirement(self):
        """
        Check if the file meets the minimum retention requirement for archiving.
        Returns True if the file has been stored for at least SEQUENCE_RETENTION_YEARS.
        """

    @property
    def file_size_display(self):
        """
        Return a human-readable file size.
        """

    def can_be_downloaded(self):
        """
        Check if the file can be downloaded.
        Files can only be downloaded if they are uploaded and don't contain PII.
        """

    def mark_as_uploaded(self):
        """
        Mark the file as successfully uploaded.
        """

    def mark_as_failed(self, reason=None):
        """
        Mark the file as failed.
        """

    def mark_as_pii_detected(self):
        """
        Mark the file as containing PII.
        """

    def check_filename_globally_unique(self):
        """
        Check if this file's filename is globally unique across all PRIMARY files.

        Only checks against files that are currently in PRIMARY status, since
        the constraint is that only one file with a given filename can be PRIMARY
        at any time.

        Returns:
            dict: {
                "is_unique": bool,
                "conflicting_file_ids": list,  # List of file IDs with the same filename
            }
        """

        # Find any other PRIMARY files with the same filename (excluding this file)
        # Need to check both:
        # 1. Paths that end with "/{filename}" (files in subdirectories)
        # 2. Paths that exactly match the filename (files at root/without directory)

    def _check_primary_eligibility_via_engine(self, result: dict, *, acknowledged_warning_ids, user, persist) -> dict:
        """Engine-backed eligibility check; mutates and returns `result`."""
        # Legacy `missing_metadata_keys` contract: surface key names of every
        # REQUIRED error so downstream callers that haven't migrated to
        # `errors[]` still see what's missing.

    def _check_primary_eligibility_legacy(self, result: dict) -> dict:
        """Legacy presence-only check used when ENFORCE_METADATA_VALIDATION=False."""

    def check_primary_eligibility(self, *, acknowledged_warning_ids=None, user=None, persist=False):
        """
        Check if this file is eligible to be promoted to PRIMARY status.

        Validates that:
        1. The file is currently in DRAFT status
        2. The filename is globally unique
        3. When ENFORCE_METADATA_VALIDATION is True, the full metadata
           validation engine passes. When False, falls back to the legacy
           "required keys present" check for backwards compatibility.
        """

    def promote_to_primary(self, *, force=False, acknowledged_warning_ids=None, user=None):
        """
        Promote this file to PRIMARY status.

        Args:
            force: If True, skip eligibility check and force promotion.
                   Use with caution - primarily for admin overrides.
            acknowledged_warning_ids: List of issue hashes the caller has acknowledged.
                                      Errors still block; only warnings can be acknowledged.
            user: The user initiating promotion (audit trail).

        Returns:
            dict: {
                "success": bool,
                "message": str,
                "eligible": bool,
                "missing_metadata_keys": list,
                "errors": list[dict],
                "warnings": list[dict],
                "unacknowledged_warning_hashes": list[str],
            }
        """

        # Dynamic-dataset subscription hook: every active rule is evaluated
        # against this file and matching files are copied (same-lab) or
        # access-requested (cross-lab) into the matching analytical datasets.
        # transaction.on_commit ensures we don't enqueue if the surrounding
        # transaction rolls back.

    def _enqueue_dynamic_subscription_evaluation(self) -> None:
        """Schedule evaluate_dynamic_subscriptions for this file after commit.

        Imported lazily to avoid a circular import (the celery task module
        imports File for type lookups). Errors here must never block a
        successful promotion: a missed enqueue is recoverable, a broken
        promotion is not.
        """

    def mark_as_archived(self, external_storage_location="", external_storage_type=""):
        """
        Mark the file as archived.
        Optionally stores the external storage location where the file can be accessed.
        """

    def get_metadata_tags_as_csv(self) -> str:
        """
        Generate CSV string of file metadata tags.
        Shares the build logic with the metadata_csv API endpoints.

        Returns:
            CSV content as string with header row and data row.
        """

    def _mark_copies_as_deleted(self, reason: str) -> int:
        """
        Mark all copies of this file in analytical datasets as DELETED.

        This only marks the copies as DELETED in the database - it does NOT delete their GCS blobs.
        The blobs remain in the analytical dataset buckets because the dataset owner might still
        be using them. When the analytical dataset itself is deleted, the blobs will be cleaned up
        by AnalyticalDataset.delete().

        Args:
            reason: The deletion reason to store on copies.

        Returns:
            Number of copies marked as deleted.
        """

    def _mark_copies_as_archived(
        self,
        external_storage_location: str = "",
        external_storage_type: str = "",
        archived_at=None,
    ) -> int:
        """
        Mark all copies of this file in analytical datasets as ARCHIVED.

        Args:
            external_storage_location: External storage location to propagate to copies.
            external_storage_type: External storage type to propagate to copies.
            archived_at: Timestamp when the file was archived (defaults to now if not provided).

        Returns:
            Number of copies marked as archived.
        """

    def _delete_gcs_blob(self) -> bool:
        """
        Delete the GCS blob for this file.

        Returns:
            True if blob was deleted, False otherwise.
        """

    def _collect_deletion_notification_recipients(self) -> tuple[set, list[dict]]:
        """
        Collect all users who should receive deletion notifications.

        Returns:
            Tuple of (notification_users set, impacted_datasets list)
        """

    def _send_uploader_csv_email(self, details: str, metadata_csv: str) -> None:
        """Send direct email with CSV attachment to the uploader if they haven't opted out."""

    def _send_deletion_notification(self, justification: str, metadata_csv: str, deleted_by=None) -> None:
        """
        Create notification for file deletion with CSV attachment.

        Email recipients are filtered by user notification preferences.
        """

    def hard_delete(
        self,
        justification: str,
        deleted_by,
        *,
        bulk_batch_id: str | None = None,
    ) -> dict:
        """
        Permanently delete this file with full audit trail and cleanup.

        For original files (files in lab buckets):
        - Exports metadata to CSV
        - Marks all copies of this file as DELETED (status only, blobs preserved)
        - Deletes the original file's GCS blob
        - Sends email notification to uploader of this file and analytical
          dataset creators that are using a copy of this file (single-delete
          only; see bulk_batch_id below)
        - Creates audit trail (Deletion record)
        - Either marks the original as DELETED (if copies exist) or deletes it from DB

        For copied files (files in analytical datasets):
        - NOTE: Individual copied files can ONLY be deleted via Django admin panel, NOT via API
        - Deletes the copy's GCS blob
        - Marks the copy as DELETED in database
        - Checks if this was the last active copy of a deleted original file
        - If so, deletes the orphaned original file record

        Args:
            justification: Reason for deletion.
            deleted_by: User performing the deletion.
            bulk_batch_id: When set, marks this call as part of a bulk-delete
                batch. This suppresses per-file notification dispatch, since the bulk task
                sends one aggregated notification for the whole batch.
                The id is written to the Deletion row's additional_data.
                None for single-delete.

        Returns:
            Dict containing metadata_csv and file_info for audit logging.
        """
        # if no justification was supplied, fall back to the status label
        # validation upstream ensures justification is provided or the status itself
        # gives enough justification

    def _hard_delete_copy(self, justification: str, deleted_by) -> dict:
        """
        Delete a copied file (file in an analytical dataset bucket) with audit trail.

        NOTE: This method is ONLY called via Django admin panel for individual copied file deletion.
        It is NOT exposed via API. The primary way copied files are deleted is through cascade
        deletion when their parent AnalyticalDataset is deleted.

        This includes:
        - Deleting the copy's GCS blob
        - Marking the copy as DELETED in database
        - Checking if the original file is deleted and has no remaining active copies
        - If so, deleting the orphaned original file record

        Args:
            justification: Reason for deletion.
            deleted_by: User performing the deletion.

        Returns:
            Dict containing file_info for audit logging.
        """

        # 1. Delete the copy's GCS blob

        # 2. Delete Copy from database

        # 3. Check if we need to cleanup the orphaned original file AFTER deleting this copy
        # Since the copy is now deleted from DB, the count will automatically exclude it

    def _hard_delete_original(
        self,
        justification: str,
        deleted_by,
        *,
        bulk_batch_id: str | None = None,
    ) -> dict:
        """
        Delete an original file (file in a lab bucket) with full audit trail.

        This includes:
        - Exporting metadata
        - Marking all copies as DELETED and deleting their GCS blobs
        - Deleting the original's GCS blob
        - Sending per-file email/in-app notifications (single delete only)
        - Creating audit trail
        - Either marking as DELETED or deleting from DB

        Args:
            justification: Reason for deletion.
            deleted_by: User performing the deletion.
            bulk_batch_id: See hard_delete. presence suppresses per-file notifications.

        Returns:
            Dict containing metadata_csv and file_info for audit logging.
        """

        # 1. Export metadata to CSV

        # 2. Mark all copies as DELETED and delete their GCS blobs

        # 3. Delete the original file's GCS blob

        # 4. Send notification to uploader and analytical dataset creators (single-delete only)

        # 5. Create Deletion record for audit trail
        # 6. Either mark as DELETED or delete from database
