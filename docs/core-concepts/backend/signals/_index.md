# Signal Layer

## `pre_delete` for Notifications and Cleanup, `post_save` for Everything Else

Across the signal layer, `pre_delete` is used deliberately when the handler needs access to related objects that CASCADE deletions would otherwise destroy. `post_save` is used for everything else.

`projects-signals.md` makes this explicit: `delete_notification` is connected to `pre_delete` rather than `post_delete` specifically because the notification must reference related objects (project users, lab directors) before they are cascade-deleted. `files-signals.md` follows the same convention: `cleanup_gcs_file` uses `pre_delete` so the GCS path is still available on the instance.

Any signal handler that needs to read or notify from related data before a delete must use `pre_delete`. Using `post_delete` for this purpose will silently produce incomplete notifications or miss data.


---

## GCP Infrastructure Provisioned via `post_save` Signals, Not in the API Layer

GCP resource creation: Cloud Build triggers, GCS bucket provisioning, pub/sub topics, IAM bindings, service accounts: is handled in `post_save` signal handlers, not in serializers or views. This means it fires regardless of how a resource is created (API, Django admin, management commands, fixtures, etc.).

This pattern appears across `labs-signals`, `projects-signals`, `uploads-signals`, and `datasets-signals`. The trade-off is that GCP errors surface on the model (written back as a build status or error field) rather than as API validation errors, so the UI's "Build logs" affordance is the primary feedback mechanism for infrastructure failures.

Critically, `trigger_cloud_build` can raise before any build is submitted (network/IAM errors). Both `trigger_gcp_lab_project_creation` and `trigger_gcp_project_creation` explicitly capture this failure case and write it back to the model so the UI can surface it: otherwise the resource would appear stuck indefinitely with no feedback.


---

## GCP Cleanup on Delete Deliberately Preserves Target Buckets

`datasets-signals.cleanup_gcs_buckets` does not delete everything on dataset deletion. Target buckets (where processed data lands) are explicitly preserved for archival purposes. Only ingest buckets, pub/sub topics and subscriptions, service account key secrets, and service accounts are cleaned up.

This is a deliberate data-preservation decision, not an oversight. Developers modifying deletion logic should not add target bucket deletion without explicit sign-off.


---

## Business Logic Delegated to Service Layer from Signals (`ProjectArchiveService`)

Signal handlers are kept thin: they detect that something happened and delegate to a service layer method rather than containing the business logic themselves. `handle_project_archived` delegates entirely to `ProjectArchiveService.process_archiving_behavior()`.

The signal is also noted as idempotent by design: it is safe to call multiple times, which is important because `post_save` fires on every save, not only when the archived state first changes. Any signal handler that drives a state transition should either be idempotent or guard explicitly against re-triggering.


---

## Email Recipients Pre-Filtered at Write Time, Not at Send Time

`notifications-signals.handle_email_recipients_changed` fires when `email_recipients` are added to a `Notification` and triggers the actual email send. The handler performs no preference filtering itself: that filtering is expected to have already happened when `email_recipients` was populated.

This mirrors the same pattern in the manager layer (`inapp_recipients`): correctness is enforced at write time. Any code that populates `email_recipients` must filter by user notification preferences before adding users: the signal handler will send to everyone it finds in that field without further checks.


---

## `m2m_changed` Used When Related Objects Must Exist Before the Signal Fires

Two signal handlers use `m2m_changed` specifically because they need the M2M relationship to be fully committed before acting: `access_requests-signals.notify_approvers_of_new_access_request` and `notifications-signals.handle_email_recipients_changed`.

For access requests, using `post_add` on `m2m_changed` ensures approvers are already added before the notification is sent to them. The handler also deduplicates: if approvers are added in batches, it checks whether a notification for the request already exists before creating a new one.

For notifications, using `m2m_changed` on the `email_recipients` through table ensures the recipient list is populated before the email dispatch fires.

Using `post_save` instead would fire before the M2M rows exist, producing empty recipient lists.


---

## Soft Deletion Detected via `pre_save` Flag, Notified via `post_save`

Soft deletion of users is a two-signal operation. `detect_soft_deletion` (connected to `pre_save`) reads the previous state from the database and sets a flag on the instance when it detects that `deleted_by` is changing from `None` to a value, or `is_active` is changing from `True` to `False`. The subsequent `post_save` handler `notify_user_soft_deleted` reads that flag and sends the notification.

This two-step approach is necessary because `post_save` cannot reliably compare old vs. new field values: by the time it fires, the old state is gone. The `pre_save` handler captures the diff and passes it forward via the instance flag.

The `post_delete` handler for hard deletions explicitly notes that `content_object` will return null when the notification is serialized, since the user no longer exists in the database at that point.

---

## Metadata Tag Changes Fan Out CSV Refreshes to All Dependent Datasets

When a `FileMetadataTag` is edited, the change silently invalidates the metadata CSV for every analytical dataset that contains a copy of that file (since the CSV builder resolves tags via `original_file_id`). The `metadatatags-signals` module handles this by fanning out a refresh job to each affected dataset via `_enqueue_refresh_for_dependents`.

A debounce/collapse mechanism is noted: bulk edits are collapsed per dataset so a single file with many tag changes does not enqueue redundant refreshes for the same dataset.

---

## Deferred Imports in Signals to Avoid Circular Dependencies

`labs-signals.add_lab_to_sequencing_lab_metadata` explicitly defers its imports inside the function body to avoid circular dependencies between the `labs` and `metadatatags` apps. This is the same pattern used in the model layer (`File._enqueue_dynamic_subscription_evaluation`) and the manager layer (`ProjectModelManager.active()`).

Any signal handler that needs to import from a sibling app should follow this pattern: top-level imports between apps that mutually reference each other will produce import errors at startup.

---

## Disabled Signals Left in Place with Explicit Comments

Two signals are fully commented out in `files-signals.md` rather than deleted: the automatic metadata-based PRIMARY promotion signal (`update_file_status_on_metadata_change`) and the DLP scan trigger (`trigger_dlp_scan_signal`). Both are preserved with their full implementation intact and a `NOTE:` comment explaining why they were disabled and what replaced them.

A placeholder function `update_file_status_on_metadata_change` is kept at module level explicitly for import compatibility: other modules may import it by name, and removing it would cause an `ImportError`.

Developers should not re-enable these signals without understanding the replacement mechanisms: status promotion is now manual via `File.promote_to_primary()`, and DLP scanning has its own trigger path.

