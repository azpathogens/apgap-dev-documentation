# Celery Tasks

## Cloud Build Polling Uses Up to 24 Retries Over Two Hours

Both `poll_cloud_build_status` (projects) and `poll_lab_cloud_build_status` (labs) share identical retry configuration: `max_retries=24` with a default 5-minute retry delay, giving a maximum polling window of approximately two hours. This is the standard polling budget for any GCP Cloud Build operation in the codebase.

Both tasks also accept a `bind=True` parameter, meaning they receive `self` and can call `self.retry()` to reschedule. When adding a new Cloud Build polling task, use the same `max_retries=24` ceiling rather than choosing an arbitrary number.

---

## `celery.exceptions.Retry` Must Be Re-Raised, Never Caught as an Error

Both Cloud Build polling tasks contain an explicit `except Retry: raise` block, with a comment explaining why. `self.retry()` raises `celery.exceptions.Retry` as a **normal control-flow mechanism** to schedule the next poll: it is not an error. Catching it and treating it as an exception (e.g. persisting it as `last_build_error`, or calling `self.retry()` again from the `except` block) would produce incorrect error state on the model or cause a double-retry.

Any `bind=True` task that calls `self.retry()` inside a broad `try/except Exception` block must have an explicit `except Retry: raise` guard above the general exception handler, or `Retry` will be silently swallowed.

---

## Errors Are Persisted on the Model, Not Just Logged

When a Cloud Build polling task catches a real (non-`Retry`) exception, it persists the failure on the relevant model (`Lab.last_build_error` or `Project.last_build_error`) so it surfaces in the UI's "Build logs" affordance. This is a best-effort operation: the error-capture helper (`capture_build_error`) is documented as never raising, but the surrounding `objects.get` may, so the whole block is guarded.

The same pattern appears in the signal layer: `trigger_gcp_project_creation` and `trigger_gcp_lab_project_creation` write back to the model if `trigger_cloud_build` raises before submitting a build. The principle is consistent throughout: **GCP failures must always surface on the model, not disappear into logs.**

---

## Notebook Sync Uses Model Properties, Not Raw DB Fields, to Handle Cache Misses

`sync_notebook_viewer_access` calls `_sync_single_project`, which reads the notebook SA email via model properties (which fall back to reading Terraform state from GCS) rather than directly from cached DB fields. This is deliberate: on each Celery retry, the property re-polls for values that may not have been cached yet due to a race condition between Cloud Build completing and the cache being warmed.

If the notebook SA email is still unavailable after the property lookup, the task raises `Retry` rather than failing. Combined with a `max_retries=5` and `default_retry_delay=30` (exponential backoff: 30s, 60s, 120s, 240s, 300s), this allows the task to wait for the cache to be populated without blocking a worker thread.

---

## DLP Scan Tasks Suppress Error Returns to Avoid Overriding the Main Task Result

Both `trigger_dlp_scan` and `trigger_dlp_scan_batch` in `datasets-dlp_scan` contain a comment on the ingest blob cleanup step: *"Don't return error message here as it would override the main task result."* This means cleanup failures are silently swallowed rather than surfaced as task failures, intentionally. The main task result (whether the DLP scan and file move succeeded) takes precedence over cleanup errors.

This is a conscious trade-off: a failed cleanup of the ingest blob is recoverable and should not mask a successful scan result. Developers adding steps at the end of a DLP task should be aware of this pattern and not return error values from cleanup steps.

---

## Bulk Delete Re-Validates Per-File Invariants Inside the Task

`bulk_hard_delete_files` does not trust the pre-validation performed synchronously in the view. It re-fetches all files in a single query (keyed by ID into a dict to preserve request order) and re-checks every per-file rule the view enforced. Any file that fails the re-check is treated as drift between enqueue and execution: the time between validation and task execution is long enough that file state may have changed.

This is the correct pattern for any Celery task that operates on resources validated at enqueue time: always re-validate inside the task, never assume the pre-validation result is still valid.

---

## Aggregated Notifications for Bulk Operations, with Failure Details Sent Only to the Initiator

`bulk_hard_delete_files` sends a single aggregated notification to all recipients (lab directors, platform admins, file uploaders, and the initiating actor) summarising the successful deletions. Failure details are sent in a **separate notification to the initiator only**: not to the shared recipient list. This prevents internal error messages (e.g. raw GCS exceptions) from being visible to all recipients.

The recipient list is resolved via `_collect_batch_recipients`, which always includes the initiating actor so they always receive their own batch result.

---

## Batch Upload Cleanup Clears the Secret Name Even on Partial Failure

`cleanup_expired_batch_uploads` sets `batch_service_account_secret_name` to an empty string after attempting cleanup, even if some cleanup steps failed. This is explicitly to avoid retrying indefinitely: once the secret name is cleared, the record will not be picked up by the next run of the periodic task.

The task also explicitly does **not** delete service accounts, only the secret. Service accounts are preserved because they may be reused or managed separately outside this cleanup path.

---

## Stuck File Cleanup as a Safety Net for Indefinitely Processing Files

`cleanup_stuck_files` in `files-dlp_scan` exists as a scheduled safety net: files that remain in `PROCESSING` status beyond a configurable threshold (`older_than_hours`, defaulting to 8) are transitioned to `FAILED`. This guards against scenarios where a DLP scan task silently fails or a Pub/Sub notification is dropped, which would otherwise leave a file stuck in `PROCESSING` indefinitely with no feedback.

