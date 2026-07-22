"""
DLP scan and SRA scrubber workflow processing for uploads.

Like the descent into the underworld, files must pass through trials
before they emerge, transformed and purified, into their final resting place.
"""


# Redis client for distributed locking

# Polling configuration constants
WORKFLOW_POLL_RETRY_COUNTDOWN = 60  # seconds between polling attempts
# Max retries (120 * 60s = 2 hour polling window)
WORKFLOW_POLL_MAX_RETRIES = 120
# Poll-phase lock expiration (slightly longer than retry countdown)
WORKFLOW_POLL_LOCK_EXPIRE = 65
# Promotion-phase lock expiration. Held while we run the cross-bucket rewrite
# of the scrubbed FASTQ from the workflow output bucket to the lab bucket.
# Sized to comfortably cover a multi-GB cross-region rewrite plus cleanup.
PROMOTE_LOCK_EXPIRE = 1800

# Lua script for compare-and-delete: only release the lock if we still own it.
# Prevents a worker that re-acquired an expired lock from accidentally
# deleting the predecessor's still-valid lock. Keys/Args are 1-indexed in Lua.


def _release_lock_if_owner(lock_key: str, request_id: str) -> None:
    """
    Atomically release a Redis lock, but only if the current owner matches.

    Uses a Lua script (EVAL) so the get-and-delete pair is atomic on the
    Redis server side. Failures (e.g. transient network errors) are logged
    and swallowed -- the lock will self-heal via TTL expiration.
    """


def _get_file_type_info(filename: str) -> tuple[bool, bool, bool]:
    """
    Determine file type info from filename.

    Args:
        filename: The filename to analyze

    Returns:
        Tuple of (is_fastq, is_gz, is_bz)
    """
    # Check if file is fastq - match .fastq or .fq anywhere in extensions
    # Supports: file.fastq, file.fq, file.fastq.gz, file.fq.gz,
    #           file.fastq_1.gz, file.fq_1.gz, etc.


def _get_blob_size_bytes(source_blob, upload_id) -> int | None:
    """
    Fetch the size of a GCS blob in bytes, returning None if it cannot be read.

    Used as a fallback when an Upload's stored file_size is missing so the
    SRA scrubber resource calculator can still size the Batch job correctly
    instead of silently falling back to its minimum disk allocation.
    """


def _resolve_upload_file_size_bytes(upload: Upload, source_blob, upload_id) -> int | None:
    """
    Resolve the input file size for SRA scrubber resource calculation.

    Tries, in order:
      1. ``Upload.file_size`` (set when the row was created from Pub/Sub).
      2. ``Upload.file.file_size`` (mirrored on the linked File row).
      3. The GCS blob's metadata (defensive fallback for when the Pub/Sub
         OBJECT_FINALIZE message arrived without a ``size`` field, leaving
         both DB columns null).

    Returns ``None`` only when all three sources fail, in which case
    ``calculate_scrubber_resources`` will fall back to its small-tier defaults.
    """


@shared_task
def trigger_dlp_scan_for_upload(upload_id):  # noqa: PLR0915
    """
    Trigger DLP scan for the given upload.

    Upon successful DLP scan, triggers the SRA scrubber workflow
    for further processing.

    Args:
        upload_id: The ID of the Upload object to scan

    Returns:
        str: Status message or None if failed
    """

        # Assuming DLP scan passed, below.
        # Move file to dataset STAGING bucket
        # For batch uploads, Upload.filename contains the original filename (for source blob lookup)
        # but the destination should use the unique filename from File.gcs_file_path
        # (which may have been incremented if there was a duplicate).


@shared_task(bind=True, max_retries=WORKFLOW_POLL_MAX_RETRIES)
def poll_sra_scrubber_workflow(  # noqa: PLR0911
    self,
    upload_id: int,
    execution_name: str,
    ingest_bucket: str,
    blob_name: str,
):
    """
    Poll the status of the SRA scrubber workflow execution.

    Once the workflow completes, promotes the processed file from the
    workflow output bucket to the final destination bucket and cleans up
    intermediate storage.

    Args:
        upload_id: The ID of the Upload object being processed
        execution_name: The full resource name of the workflow execution
        ingest_bucket: The ingest bucket where the original file was uploaded
        blob_name: The name of the blob in the ingest bucket

    Returns:
        str: Final status message or None if still polling
    """
    # Acquire distributed lock to prevent duplicate processing.
    # The lock is keyed on execution_name so concurrent polls of the SAME
    # workflow execution serialize, while polls of different executions
    # remain independent.

    # Single release point: every code path below (retry, terminal failure,
    # terminal success, Upload.DoesNotExist, generic exception) flows through
    # this finally so the lock cannot leak. The release is a compare-and-delete
    # so we only ever drop our own lock, never one a successor has acquired
    # after a TTL expiration.

                    # Extend the lock TTL before the long-running promotion.
                    # A multi-GB cross-region rewrite can far outlast the
                    # poll-phase TTL; without this, a sibling worker could
                    # acquire the lock mid-promotion and start a duplicate copy.

                # Workflow failed/cancelled/unavailable
                # Note: The Error proto uses 'payload' (JSON string) and 'context' (stack trace),
                error_msg = execution.error.payload if execution.error else "Unknown error"
                logger.error(
                    f"SRA scrubber workflow failed for upload {upload_id}: {error_msg}",
                )
                upload.file.status = FileStatus.FAILED
                upload.file.save()

                # Clean up ingest bucket
                _cleanup_ingest_blob(ingest_bucket, blob_name)

                return f"Workflow failed: {error_msg}"

            # Workflow still in progress - retry
            logger.info(
                f"SRA scrubber workflow for upload {upload_id} is still {state_name}. "
                f"Retrying in {WORKFLOW_POLL_RETRY_COUNTDOWN} seconds.",
            )
            self.retry(countdown=WORKFLOW_POLL_RETRY_COUNTDOWN)
            return None

        except Upload.DoesNotExist:
            logger.error(f"Upload {upload_id} does not exist")
            return "Upload not found"

        except Retry:
            # self.retry() raises celery.exceptions.Retry to schedule the next
            # attempt. Re-raise so Celery's task machinery handles it; the
            # outer finally still runs to release the lock.
            raise

        except Exception as e:
            logger.exception(f"Error polling workflow for upload {upload_id}: {e}")
            self.retry(countdown=WORKFLOW_POLL_RETRY_COUNTDOWN)
            return None
    finally:
        _release_lock_if_owner(lock_key, request_id)


def _trigger_sra_scrubber_workflow(  # noqa: PLR0913
    upload: Upload,
    ingest_bucket: str,
    blob_name: str,
    original_filename: str,
    *,
    is_fastq: bool,
    is_gz: bool,
    is_bz: bool,
    is_gui_upload: bool,
    workflow_id: str,
    workflow_project_id: str,
    workflow_location: str,
    output_bucket: str,
    resources: "BatchJobResources | None" = None,
) -> dict | None:
    """
    Trigger the SRA scrubber workflow with the appropriate payload.

    Args:
        upload: The Upload object being processed
        ingest_bucket: The bucket containing the input file
        blob_name: The name of the blob in the ingest bucket
                   (ingest_uuid for GUI uploads, filename for batch uploads)
        original_filename: The original filename as provided by the user
        is_fastq: Whether the file is a fastq file
        is_gz: Whether the file is gzip compressed
        is_bz: Whether the file is bzip2 compressed
        is_gui_upload: Whether this is a GUI upload (vs batch/CLI upload)
        workflow_id: The ID of the SRA scrubber workflow
        workflow_project_id: The GCP project ID where the workflow is deployed
        workflow_location: The location where the workflow is deployed
        output_bucket: The bucket where the workflow will write output
        resources: Optional dict of dynamic resource parameters
                   (disk_size_gb, cpu_milli, memory_mib, num_threads)
                   from calculate_scrubber_resources(). If None, the workflow
                   will use its built-in defaults.

    Returns:
        dict: The workflow execution object, or None if trigger failed
    """
    workflows_client = WorkflowsClient()

    # Build the workflow payload
    # - filename: the blob name in the input bucket, also used as the output filename
    # - original_filename: the actual filename provided by the user
    arguments = {
        "filename": blob_name,
        "original_filename": original_filename,
        "is_fastq": str(is_fastq).lower(),
        "is_gz": str(is_gz).lower(),
        "is_bz": str(is_bz).lower(),
        "is_gui_upload": str(is_gui_upload).lower(),
        "input_gcs": ingest_bucket,
        "output_gcs": output_bucket,
    }

    # Include dynamic resource parameters if available.
    # The workflow uses default() fallbacks, so omitting these is safe.
    if resources:
        arguments.update(resources.to_workflow_args())

    return workflows_client.execute_workflow(
        workflow_id=workflow_id,
        project_id=workflow_project_id,
        location=workflow_location,
        arguments=arguments,
    )


def _find_workflow_output_blob(output_bucket, blob_name: str):
    """
    Search for the workflow output blob, which may have a compression extension appended.

    The SRA scrubber workflow may append .gz or .bz2 to the output filename.

    Args:
        output_bucket: The GCS bucket object to search in
        blob_name: The base blob name (typically UUID) to search for

    Returns:
        tuple: (blob object, actual blob name) if found, (None, None) if not found
    """
    # The possible extensions the workflow may append, in order of likelihood
    # First we try the raw name, then the compressed variants
    candidate_names = [
        blob_name,
        f"{blob_name}.gz",
        f"{blob_name}.bz2",
    ]

    for candidate in candidate_names:
        blob = output_bucket.blob(candidate)
        if blob.exists():
            logger.info(f"Found workflow output blob: {candidate}")
            return blob, candidate

    return None, None


def _copy_blob_cross_bucket_with_rewrite(
    source_blob,
    destination_bucket,
    destination_blob_name: str,
    *,
    storage_client=None,
    if_generation_match: int | None = None,
) -> None:
    """
    Copy a blob to another bucket using the JSON rewrite API.

    Cross-location or large-object server-side copies exceed the ~30s limit of
    objects.copy; rewrite is resumable via tokens until complete.

    When ``if_generation_match`` is provided, it is forwarded to every rewrite
    RPC. Pass ``0`` to require that the destination object does not yet exist
    (GCS's create-only precondition). On a race the loser gets HTTP 412
    PreconditionFailed and the rewrite raises -- callers should catch it.
    """
    destination_blob = destination_bucket.blob(destination_blob_name)
    # Only include the kwarg when explicitly requested. Keeps the rewrite()
    # call signature unchanged for the common case and preserves backward
    # compatibility with existing tests that assert exact kwargs.
    extra = {} if if_generation_match is None else {"if_generation_match": if_generation_match}
    rewrite_token = None
    while True:
        rewrite_token, bytes_rewritten, total_bytes = destination_blob.rewrite(
            source_blob,
            token=rewrite_token,
            client=storage_client,
            retry=DEFAULT_RETRY,
            **extra,
        )
        if rewrite_token is None:
            logger.info(
                "Cross-bucket rewrite finished: %s -> gs://%s/%s (%s bytes)",
                source_blob.name,
                destination_bucket.name,
                destination_blob_name,
                total_bytes,
            )
            return
        logger.debug(
            "Cross-bucket rewrite progress: %s -> gs://%s/%s (%s/%s bytes)",
            source_blob.name,
            destination_bucket.name,
            destination_blob_name,
            bytes_rewritten,
            total_bytes,
        )


def _finalize_already_promoted(
    upload: Upload,
    output_blob,
    ingest_bucket: str,
    blob_name: str,
) -> str:
    """
    Idempotent finalize for "another worker already promoted this file".

    Performs best-effort cleanup of the workflow output and ingest blobs and
    sets the File status to DRAFT only if it is still PROCESSING. Used in the
    duplicate-worker race paths so the loser exits cleanly without flipping
    the file to FAILED or interfering with terminal status set by the winner.
    """
    if output_blob is not None:
        _cleanup_blob(output_blob)
    _cleanup_ingest_blob(ingest_bucket, blob_name)
    if upload.file and upload.file.status == FileStatus.PROCESSING:
        upload.file.status = FileStatus.DRAFT
        upload.file.save()
    logger.info(
        "Promotion no-op for upload %s: another worker already promoted the file.",
        upload.id,
    )
    return "File already promoted by concurrent worker"


def _promote_file_from_workflow_output(  # noqa: PLR0911
    upload: Upload,
    ingest_bucket: str,
    blob_name: str,
) -> str:
    """
    Promote the processed file from workflow output bucket to final destination.

    This function:
    1. Copies the file from SRA_SCRUBBER_WORKFLOW_OUTPUT_BUCKET to the lab's bucket
    2. Cleans up the file from the workflow output bucket (staging)
    3. Cleans up the original file from the ingest bucket
    4. Updates the file status to DRAFT

    Idempotency: if a sibling worker has already promoted the file (the
    destination already exists, or the source vanishes mid-copy because the
    sibling cleaned it up, or the rewrite hits a 412 Precondition Failed),
    this function returns success without flipping the file to FAILED.

    Args:
        upload: The Upload object being processed
        ingest_bucket: The original ingest bucket
        blob_name: The name of the blob in the ingest bucket

    Returns:
        str: Status message
    """
    storage_client = storage.Client(project=settings.DATAOPS_PROJECT_ID)

    try:
        # Source: workflow output bucket (staging)
        # The workflow may output the file with a compression extension appended
        output_bucket_name = settings.SRA_SCRUBBER_WORKFLOW_OUTPUT_BUCKET
        output_bucket = storage_client.bucket(output_bucket_name)

        logger.info(f"Searching for processed file in gs://{output_bucket_name}/ with base name {blob_name}")

        # Search for the blob - it may have .gz or .bz2 appended by the workflow
        output_blob, actual_blob_name = _find_workflow_output_blob(output_bucket, blob_name)

        # Destination: lab's bucket (use unique filename from File to handle duplicates)
        destination_bucket = storage_client.bucket(upload.lab.gcs_bucket)
        destination_blob_name = upload.file.filename if upload.file else upload.filename

        if output_blob is None:
            # Source missing. Two reasons this can happen:
            #   1. A sibling worker already promoted and cleaned up the staging blob.
            #   2. The workflow really failed to produce output.
            # Distinguish by checking whether the destination exists.
            if destination_bucket.blob(destination_blob_name).exists():
                logger.info(
                    "Workflow output missing but destination present for upload %s; treating as already promoted.",
                    upload.id,
                )
                return _finalize_already_promoted(upload, None, ingest_bucket, blob_name)
            logger.error(
                f"Processed file not found in workflow output bucket: gs://{output_bucket_name}/{blob_name} "
                f"(also tried .gz and .bz2 extensions)",
            )
            upload.file.status = FileStatus.FAILED
            upload.file.save()
            return "Processed file not found in workflow output"

        # Pre-check: if the destination already exists we have nothing to do.
        # Cheaper than letting the rewrite RPC fail with 412 and avoids racing
        # against a sibling worker that is still in the middle of promoting.
        if destination_bucket.blob(destination_blob_name).exists():
            logger.info(
                "Destination gs://%s/%s already exists for upload %s; skipping rewrite.",
                upload.lab.gcs_bucket,
                destination_blob_name,
                upload.id,
            )
            return _finalize_already_promoted(upload, output_blob, ingest_bucket, blob_name)

        logger.info(
            f"Promoting file from gs://{output_bucket_name}/{actual_blob_name} "
            f"to gs://{upload.lab.gcs_bucket}/{destination_blob_name}",
        )

        # if_generation_match=0 = "destination must not yet exist". This is
        # GCS's atomic create-only precondition; on a race exactly one rewrite
        # succeeds, the loser gets PreconditionFailed.
        try:
            _copy_blob_cross_bucket_with_rewrite(
                output_blob,
                destination_bucket,
                destination_blob_name,
                storage_client=storage_client,
                if_generation_match=0,
            )
        except PreconditionFailed:
            logger.info(
                "Destination gs://%s/%s already promoted (precondition failed) for upload %s; treating as success.",
                upload.lab.gcs_bucket,
                destination_blob_name,
                upload.id,
            )
            return _finalize_already_promoted(upload, output_blob, ingest_bucket, blob_name)
        except NotFound:
            # Source disappeared mid-copy. Either the sibling worker cleaned
            # up after promoting, or the workflow output was deleted out of
            # band. Re-check the destination to disambiguate.
            if destination_bucket.blob(destination_blob_name).exists():
                logger.info(
                    "Source vanished but destination present for upload %s; another worker promoted first.",
                    upload.id,
                )
                return _finalize_already_promoted(upload, output_blob, ingest_bucket, blob_name)
            logger.error(
                "Both source and destination missing for upload %s; workflow output disappeared.",
                upload.id,
            )
            upload.file.status = FileStatus.FAILED
            upload.file.save()
            return "Workflow output disappeared before promotion"

        logger.info(f"File successfully promoted for upload {upload.id}")

        # Update file status
        upload.file.status = FileStatus.DRAFT
        upload.file.save()

        # Clean up: delete from workflow output bucket (staging)
        _cleanup_blob(output_blob)
        logger.info(f"Cleaned up staging bucket for upload {upload.id}")

        # Clean up: delete from ingest bucket
        _cleanup_ingest_blob(ingest_bucket, blob_name)
        logger.info(f"Cleaned up ingest bucket for upload {upload.id}")

        return "File processed and promoted successfully"

    except Exception as e:
        logger.exception(f"Error promoting file from workflow output: {e}")
        upload.file.status = FileStatus.FAILED
        upload.file.save()
        return f"Error promoting file: {e}"


def _promote_file_directly(
    upload: Upload,
    storage_client,
    bucket,
    source_blob,
) -> str:
    """
    Promote file directly from ingest bucket to destination (legacy behavior).

    This is used when no SRA scrubber workflow is configured.

    Args:
        upload: The Upload object being processed
        storage_client: The GCS storage client
        bucket: The source bucket object
        source_blob: The source blob object

    Returns:
        str: Status message
    """
    try:
        # Move file to lab's bucket
        destination_bucket = storage_client.bucket(upload.lab.gcs_bucket)
        # Use the unique filename from File.gcs_file_path (handles duplicates)
        # Fall back to Upload.filename if no File is associated
        destination_blob_name = upload.file.filename if upload.file else upload.filename

        logger.info(f"lab bucket name: {upload.lab.gcs_bucket}")
        logger.info(f"destination bucket: {destination_bucket}")
        logger.info(f"destination blob name: {destination_blob_name}")

        # Log credentials info for debugging
        credentials = storage_client._credentials  # NOQA: SLF001
        if hasattr(credentials, "service_account_email"):
            logger.info(f"Service Account Email: {credentials.service_account_email}")
        elif hasattr(credentials, "client_email"):
            logger.info(f"Client Email: {credentials.client_email}")
        else:
            logger.info(f"Credentials type: {type(credentials)}")
            logger.info("Could not detect service account email")

        _copy_blob_cross_bucket_with_rewrite(
            source_blob,
            destination_bucket,
            destination_blob_name,
            storage_client=storage_client,
        )

        upload.file.status = FileStatus.DRAFT
        upload.file.save()

        # Clean up the ingest blob
        _cleanup_blob(source_blob)

        return "File processed and moved successfully"

    except Exception:
        logger.exception("Error processing file")
        upload.file.status = FileStatus.FAILED
        upload.file.save()
        return "Error processing file"


def _cleanup_blob(blob) -> None:
    """
    Delete a blob if it exists.

    Args:
        blob: The blob object to delete
    """
    try:
        if blob.exists():
            logger.info(f"Deleting blob {blob.name}")
            blob.delete()
        else:
            logger.info(f"Blob {blob.name} does not exist, skipping deletion")
    except Exception as e:
        logger.exception(f"Error deleting blob {blob.name}: {e}")


def _cleanup_ingest_blob(ingest_bucket: str, blob_name: str) -> None:
    """
    Clean up a blob from the ingest bucket.

    Args:
        ingest_bucket: The name of the ingest bucket
        blob_name: The name of the blob to delete
    """
    try:
        storage_client = storage.Client(project=settings.DATAOPS_PROJECT_ID)
        bucket = storage_client.bucket(ingest_bucket)
        blob = bucket.blob(blob_name)
        _cleanup_blob(blob)
    except Exception as e:
        logger.exception(f"Error cleaning up ingest blob {blob_name}: {e}")
