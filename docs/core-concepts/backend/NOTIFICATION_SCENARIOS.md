# Notification Scenarios Documentation

This document describes all notification types in the APGAP system, when they are triggered, who receives them, and where the notification logic is implemented.

## Overview

The notification system uses Django signals and API endpoints to create notifications when events occur. Notifications are sent via:
- **In-app notifications**: Displayed in the user's notification panel
- **Email notifications**: Sent via SendGrid

Users can configure their notification preferences to enable/disable either channel for each notification type they are eligible to receive.

## Notification Flow

```
┌─────────────────────┐     ┌───────────────────────┐     ┌─────────────────────┐
│   Event Occurs      │────▶│  Signal Handler or    │────▶│  Create Notification│
│  (create/update/    │     │  API Endpoint         │     │  with Recipients    │
│   delete model)     │     │                       │     │                     │
└─────────────────────┘     └───────────────────────┘     └──────────┬──────────┘
                                                                     │
                            ┌───────────────────────┐                │
                            │  filter_recipients_   │◀───────────────┘
                            │  by_preferences()     │
                            └───────────┬───────────┘
                                        │
                    ┌───────────────────┴───────────────────┐
                    ▼                                       ▼
        ┌───────────────────────┐           ┌───────────────────────┐
        │  email_recipients     │           │  inapp_recipients     │
        │  (ManyToMany)         │           │  (ManyToMany)         │
        └───────────┬───────────┘           └───────────────────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │  m2m_changed signal   │
        │  triggers email task  │
        └───────────────────────┘
```

---

## General Notifications

### User Profile Updated (`USER_UPDATED`)

| Property | Value |
|----------|-------|
| **Trigger** | When a user's tracked fields are modified (name, email, organization, is_platform_admin) |
| **Signal Handler** | `asu_apgap/users/signals.py::notify_user_updated()` |
| **Signal Type** | `pre_save` on `User` model |
| **Recipients** | Platform Admins in same organization + the updated user |
| **Audience** | `ALL_USERS` |

### New User Created (`USER_CREATED`)

| Property | Value |
|----------|-------|
| **Trigger** | When a new user account is created |
| **Signal Handler** | `asu_apgap/users/signals.py::notify_platform_admins_of_user_creation()` |
| **Signal Type** | `post_save` on `User` model (created=True) |
| **Recipients** | All Platform Admins |
| **Audience** | `PLATFORM_ADMIN` |

### User Deleted (`USER_DELETED`)

| Property | Value |
|----------|-------|
| **Trigger** | When a user is deleted (hard delete) or soft deleted (is_active=False) |
| **Signal Handlers** | `asu_apgap/users/signals.py::notify_platform_admins_of_user_deletion()` (hard delete), `notify_user_soft_deleted()` (soft delete) |
| **Signal Type** | `post_delete` on `User` model (hard delete), `post_save` (soft delete) |
| **Recipients** | All Platform Admins |
| **Audience** | `PLATFORM_ADMIN` |

### Welcome Message (`WELCOME`)

| Property | Value |
|----------|-------|
| **Trigger** | When a new user account is created |
| **Signal Handler** | `asu_apgap/users/signals.py::notify_user_created()` |
| **Signal Type** | `post_save` on `User` model (created=True) |
| **Recipients** | The new user (in-app and email) |
| **Audience** | None. `WELCOME` is not in `NOTIFICATION_TYPE_AUDIENCE`, so it never appears in the preferences list |
| **Note** | Not filtered by preferences, since the user has had no chance to set any yet |

---

## Lab Notifications

### Lab Created (`LAB_CREATED`)

| Property | Value |
|----------|-------|
| **Trigger** | When a new lab is created |
| **Signal Handler** | `asu_apgap/labs/signals.py::notify_lab_created()` |
| **Signal Type** | `post_save` on `Lab` model (created=True) |
| **Recipients** | Platform Admins in the same organization |
| **Audience** | `PLATFORM_ADMIN` |

### Added to Lab (`LAB_USER_ADDED`)

| Property | Value |
|----------|-------|
| **Trigger** | When a user is added to a lab as Lab Director or Lab Reader |
| **Signal Handler** | `asu_apgap/labs/signals.py::notify_lab_user_created()` |
| **Signal Type** | `post_save` on `LabUser` model (created=True) |
| **Recipients** | The added user + Platform Admins in same organization + existing Lab Directors |
| **Audience** | `ALL_USERS` |

### Lab Archived (`LAB_ARCHIVED`)

| Property | Value |
|----------|-------|
| **Trigger** | When a lab's teardown finishes (destroy build succeeds, or no build was needed) and the lab moves from `ARCHIVING` to `ARCHIVED` |
| **Method** | `asu_apgap/labs/lifecycle.py::_notify_archived()`, queued on commit by `finalize_teardown()` |
| **Called From** | `asu_apgap/labs/celery_tasks/teardown.py::poll_lab_teardown_build()` (or directly from `start_teardown()` when Cloud Build is disabled or the lab has no `project_prefix`) |
| **Recipients** | All Platform Admins + the lab's directors (`is_lab_admin=True` or the Lab Director group) |
| **Audience** | `LAB_DIRECTOR` |
| **Note** | If the teardown fails, `record_teardown_failure()` sends a `LAB_ARCHIVED` notification with status `error` to all Platform Admins only |

### Lab Deleted (`LAB_DELETED`)

| Property | Value |
|----------|-------|
| **Trigger** | When a lab's teardown finishes (destroy build succeeds, or no build was needed) and the lab row is permanently deleted |
| **Method** | `asu_apgap/labs/lifecycle.py::_notify_deleted()`, queued on commit by `finalize_teardown()` |
| **Called From** | `asu_apgap/labs/celery_tasks/teardown.py::poll_lab_teardown_build()` (or directly from `start_teardown()` when Cloud Build is disabled or the lab has no `project_prefix`) |
| **Recipients** | All Platform Admins + the lab's directors. Recipient IDs are captured before the lab row is deleted |
| **Audience** | `LAB_DIRECTOR` |
| **Note** | If the teardown fails, `record_teardown_failure()` sends a `LAB_DELETED` notification with status `error` to all Platform Admins only |

### Lab Billing Account Changed (`LAB_BILLING_ACCOUNT_CHANGED`)

| Property | Value |
|----------|-------|
| **Trigger** | When the billing account of a lab or project GCP project is changed directly in GCP (Console or `gcloud`) |
| **Methods** | `asu_apgap/labs/services.py::LabBillingSyncService._notify_billing_changed()` (lab project changed, new account adopted and cascaded to the lab's projects), `_notify_project_snap_back()` (project changed, reverted to the lab's account) |
| **API Endpoint** | `asu_apgap/notifications/api/views.py::LabBillingChangeNotificationViewSet.create()` at `POST /api/notifications/lab-billing-change-notifications/` (Pub/Sub push of Cloud Audit Log entries) |
| **Recipients** | Lab Directors of the lab (Lab Director group) + all Platform Admins |
| **Audience** | `LAB_DIRECTOR` |

---

## Project Notifications

### Project Created (`PROJECT_CREATED`)

| Property | Value |
|----------|-------|
| **Trigger** | When a new project is created in a lab |
| **Signal Handler** | `asu_apgap/projects/signals.py::create_notification()` |
| **Signal Type** | `post_save` on `Project` model (created=True) |
| **Recipients** | Lab Directors and Lab Readers of the lab |
| **Audience** | `LAB_MEMBER` |

### Added to Project (`PROJECT_USER_ADDED`)

| Property | Value |
|----------|-------|
| **Trigger** | When a user is added to a project or their permissions are updated |
| **Signal Handler** | `asu_apgap/projects/signals.py::notify_project_user_updated()` |
| **Signal Type** | `post_save` on `ProjectUser` model |
| **Recipients** | The added/updated user + Lab Directors and Lab Readers |
| **Audience** | `ALL_USERS` |

### Project Archived (`PROJECT_ARCHIVED`)

| Property | Value |
|----------|-------|
| **Trigger** | When a project status is changed to ARCHIVED |
| **Signal Handler** | `asu_apgap/projects/signals.py::handle_project_archived()` |
| **Signal Type** | `post_save` on `Project` model (status=ARCHIVED) |
| **Recipients** | Lab users and project users via `project.get_notification_users()` |
| **Audience** | `LAB_MEMBER` |

### Project Deleted (`PROJECT_DELETED`)

| Property | Value |
|----------|-------|
| **Trigger** | When a project is permanently deleted |
| **Signal Handler** | `asu_apgap/projects/signals.py::delete_notification()` |
| **Signal Type** | `pre_delete` on `Project` model |
| **Recipients** | Lab users and project users via `project.get_notification_users()` + Platform Admins (if justification provided) |
| **Audience** | `LAB_MEMBER` |

### Project Creation Failed (`PROJECT_CREATION_FAILED`)

| Property | Value |
|----------|-------|
| **Trigger** | When a project's Cloud Build ends in a failed status, or when the build could not be started at all |
| **Method** | `asu_apgap/projects/signals.py::notify_project_creation_failed()` |
| **Called From** | `notify_project_build_finished()` (`post_save` on `Project` when `build_status` transitions to a failed terminal status) and `trigger_gcp_project_creation()` (`post_save` on `Project`, created=True, when `trigger_cloud_build` raises or returns no build or no build id) |
| **Recipients** | The project creator + all Platform Admins |
| **Audience** | `LAB_DIRECTOR` |

### Notebook Running Reminder (`NOTEBOOK_ACTIVE_REMINDER`)

| Property | Value |
|----------|-------|
| **Trigger** | When a project's Vertex Workbench notebook has been `ACTIVE` for 4 hours, then again every 4 hours while it stays active |
| **Celery Task** | `asu_apgap/projects/celery_tasks/notebook_active_reminders.py::send_notebook_active_reminders()` |
| **Schedule** | `send-notebook-active-reminders` in `CELERY_BEAT_SCHEDULE`, hourly at minute 15. No-op unless `ENABLE_GCP_INTERACTIONS` is true |
| **Recipients** | Lab Directors of the project's lab (Lab Director group) + all Platform Admins |
| **Audience** | `LAB_DIRECTOR` |
| **Note** | Only `ACTIVE` projects with a cached GCP project ID are polled. Tracking lives on `Project.notebook_became_active_at` and `notebook_active_reminder_sent_at` |

### Notebook Idle Shutdown (`NOTEBOOK_IDLE_SHUTDOWN`)

| Property | Value |
|----------|-------|
| **Trigger** | When the hourly poll finds a notebook that was previously tracked as `ACTIVE` is no longer active, and APGAP did not stop it (a manual stop clears the tracking first) |
| **Celery Task** | `asu_apgap/projects/celery_tasks/notebook_active_reminders.py::send_notebook_active_reminders()` (same task as above) |
| **Recipients** | Project users + Lab Directors of the project's lab |
| **Audience** | `LAB_MEMBER` |
| **Note** | Skipped when `Project.notebook_idle_timeout_seconds` is null (projects provisioned before the idle timeout existed) |

---

## File Notifications

### File Uploaded (`FILE_UPLOADED`)

| Property | Value |
|----------|-------|
| **Trigger** | When a new file is uploaded to a lab |
| **Signal Handler** | `asu_apgap/files/signals.py::notify_file_created()` |
| **Signal Type** | `post_save` on `File` model (created=True) |
| **Recipients** | Uploader + Lab Directors/Readers + Project users in the lab + Platform Admins in same organization |
| **Audience** | `LAB_MEMBER` |

### File PII Detected (`FILE_PII_DETECTED`)

| Property | Value |
|----------|-------|
| **Trigger** | When a file's status changes to `PII_DETECTED` after DLP scanning |
| **Signal Handler** | `asu_apgap/files/signals.py::notify_file_status_change()` |
| **Signal Type** | `post_save` on `File` model (status=PII_DETECTED) |
| **Recipients** | File uploader + Lab Directors + Platform Admins in same organization |
| **Audience** | `LAB_MEMBER` |

### File Processing Failed (`FILE_FAILED`)

| Property | Value |
|----------|-------|
| **Trigger** | When a file's status changes to `FAILED` during processing |
| **Signal Handler** | `asu_apgap/files/signals.py::notify_file_status_change()` |
| **Signal Type** | `post_save` on `File` model (status=FAILED) |
| **Recipients** | File uploader + Lab Directors + Platform Admins in same organization |
| **Audience** | `LAB_MEMBER` |

### File Deleted (`FILE_DELETED`)

| Property | Value |
|----------|-------|
| **Trigger** | When a file is permanently deleted via `hard_delete()` method |
| **Method** | `asu_apgap/files/models.py::File._send_deletion_notification()` |
| **API Endpoint** | `asu_apgap/files/api/views.py::FileViewSet.destroy()` |
| **Recipients** | File uploader + Lab Directors/Readers + Project users + Platform Admins |
| **Audience** | `LAB_MEMBER` |
| **Special** | Includes CSV attachment with file metadata sent directly to uploader |

### File Metadata Corrected (`METADATA_CORRECTED`)

| Property | Value |
|----------|-------|
| **Trigger** | When baseline metadata on one or more PRIMARY files is corrected through the correction CSV/XLSX workflow |
| **Method** | `asu_apgap/metadatatags/services.py::_notify_correction()`, called by `correct_files_metadata()` |
| **Called From** | `asu_apgap/metadata_requirements/api/csv_handlers/import_handler.py::CSVImportHandler.commit_correction()`, run by the `asu_apgap/metadata_requirements/celery_tasks/process_csv_upload.py::process_csv_upload` Celery task |
| **Recipients** | For each corrected file, via `File.collect_downstream_notification_recipients()`: the uploader + Lab Directors of the file's lab + all Platform Admins + the creator of every analytical dataset holding a copy of the file |
| **Audience** | `LAB_MEMBER` |
| **Note** | One notification per correction batch, listing every corrected file with its before and after values. Each correction is also recorded as a `Correction` row |

---

## Batch Upload Notifications

### Batch Upload Endpoint Revoked (`BATCH_UPLOAD_REVOKED`)

| Property | Value |
|----------|-------|
| **Trigger** | When someone other than the owner revokes a batch upload endpoint |
| **Method** | `asu_apgap/uploads/notifications.py::notify_batch_upload_revoked()`, called by `asu_apgap/uploads/services.py::BatchUploadRevokeService.revoke()` |
| **API Endpoint** | `asu_apgap/uploads/api/views.py::BatchUploadViewSet.revoke()` at `POST /api/uploads/batch-uploads/{id}/revoke/` |
| **Recipients** | The batch upload's owner (`BatchUpload.user`) only |
| **Audience** | `ALL_USERS` |
| **Note** | Nothing is sent when the owner revokes their own endpoint |

---

## Dataset Notifications (Batch/GUI Upload Datasets)

These notifications are for **batch upload datasets** (`Dataset` model) used for uploading files to projects.

### Dataset Created (`DATASET_CREATED`)

| Property | Value |
|----------|-------|
| **Trigger** | When a new batch/GUI upload dataset is created for a project |
| **Signal Handler** | `asu_apgap/datasets/signals.py::notify_dataset_created()` |
| **Signal Type** | `post_save` on `Dataset` model (created=True) |
| **Recipients** | Dataset creator + Project users + Lab Directors/Readers |
| **Audience** | `LAB_MEMBER` |

### Dataset File Status Changed (`DATASET_FILE_STATUS`)

| Property | Value |
|----------|-------|
| **Trigger** | When a dataset file's status changes (uploaded, PII detected, failed) |
| **Signal Handler** | `asu_apgap/datasets/signals.py::notify_dataset_file_status_change()` |
| **Signal Type** | `post_save` on `DatasetFile` model |
| **Recipients** | File uploader + Project users + Lab Directors/Readers |
| **Audience** | `LAB_MEMBER` |

---

## Access & Archive Notifications (Analytical Datasets)

These notifications are for **analytical datasets** (`AnalyticalDataset` model) which are collections of files copied from lab files for analysis purposes.

### Access Request (`ACCESS_REQUEST`)

| Property | Value |
|----------|-------|
| **Trigger** | When approvers (lab directors) are assigned to an access request for a file |
| **Signal Handler** | `asu_apgap/access_requests/signals.py::notify_approvers_of_new_access_request()` |
| **Signal Type** | `m2m_changed` on `AccessRequest.approvers.through` (action=post_add, status=PENDING) |
| **Recipients** | Lab Directors (approvers) assigned to the access request |
| **Audience** | `LAB_MEMBER` |
| **Note** | Each file in an analytical dataset requires a separate access request. Notification is only sent for PENDING requests (not auto-approved). |

### Access Request Approved (`ACCESS_REQUEST_APPROVED`)

| Property | Value |
|----------|-------|
| **Trigger** | When **all** file access requests for an analytical dataset are approved |
| **Signal Handler** | `asu_apgap/access_requests/signals.py::check_dataset_approval_status()` |
| **Signal Type** | `post_save` on `AccessRequest` model (status=APPROVED and all files approved) |
| **Recipients** | The requesting user (who created the analytical dataset) |
| **Audience** | `ALL_USERS` |
| **Note** | The analytical dataset's `approval_status` is set to `APPROVED` |

### Access Request Denied (`ACCESS_REQUEST_DENIED`)

| Property | Value |
|----------|-------|
| **Trigger** | When **any** file access request for an analytical dataset is rejected |
| **Signal Handler** | `asu_apgap/access_requests/signals.py::check_dataset_approval_status()` |
| **Signal Type** | `post_save` on `AccessRequest` model (status=REJECTED) |
| **Recipients** | The requesting user (who created the analytical dataset) |
| **Audience** | `ALL_USERS` |
| **Note** | The analytical dataset's `approval_status` is set to `DENIED` |

### Archive Request (`ARCHIVE_REQUEST`)

| Property | Value |
|----------|-------|
| **Trigger** | When a user submits an archive request for a file |
| **Signal Handler** | `asu_apgap/deletions/signals.py::notify_archive_request_status_change()` |
| **Signal Type** | `post_save` on `ArchiveRequest` model (created=True) |
| **Recipients** | Lab Directors of the file's lab + Platform Admins in same organization |
| **Audience** | `LAB_DIRECTOR` |

| Property | Value |
|----------|-------|
| **Trigger** | When an archive request is approved |
| **Signal Handler** | `asu_apgap/deletions/signals.py::_notify_requester_of_approval()` |
| **Signal Type** | `post_save` on `ArchiveRequest` model (status=APPROVED) |
| **Recipients** | The requesting user |
| **Uses** | `ACCESS_REQUEST_APPROVED` notification type for filtering |

| Property | Value |
|----------|-------|
| **Trigger** | When an archive request is denied |
| **Signal Handler** | `asu_apgap/deletions/signals.py::_notify_requester_of_denial()` |
| **Signal Type** | `post_save` on `ArchiveRequest` model (status=DENIED) |
| **Recipients** | The requesting user |
| **Uses** | `ACCESS_REQUEST_DENIED` notification type for filtering |

---

## Analytical Dataset Notifications

### Analytical Dataset File Deleted (`ANALYTICAL_DATASET_FILE_DELETED`)

| Property | Value |
|----------|-------|
| **Trigger** | When a file is deleted from an analytical dataset bucket outside of APGAP (Cloud Console, `gsutil rm`, or anything that bypasses Django) |
| **API Endpoint** | `asu_apgap/notifications/api/views.py::AnalyticalDatasetDeleteNotificationViewSet.create()` at `POST /api/notifications/analytical-dataset-delete-notifications/` (Pub/Sub push of GCS `OBJECT_DELETE` events) |
| **Recipients** | Lab Directors of the dataset's lab (Lab Director group) + all Platform Admins |
| **Audience** | `LAB_DIRECTOR` |
| **Note** | Only sent when a `File` row still points at the deleted object. App driven deletes remove the row first, and events for a dataset whose `deletion_status` is not `NONE` are ignored |

### Analytical Dataset Deleted (`ANALYTICAL_DATASET_DELETED`)

| Property | Value |
|----------|-------|
| **Trigger** | When the asynchronous deletion of an analytical dataset finishes (success) or its GCS teardown fails (failure) |
| **Celery Task** | `asu_apgap/analytical_datasets/celery_tasks/delete.py::delete_analytical_dataset()` |
| **Recipients (success)** | Lab Directors of the dataset's lab + all Platform Admins + the dataset creator + the user who started the deletion |
| **Recipients (failure)** | The user who started the deletion only, in-app and email, not filtered by preferences |
| **Audience** | `LAB_DIRECTOR` |
| **Note** | On failure the dataset is left in place with `deletion_status=DELETE_FAILED` so the delete can be retried |

---

## Metadata Option Request Notifications

These notifications cover requests to add a new option to a SELECT metadata template (`MetadataOptionRequest` model).

### Metadata Option Request (`METADATA_OPTION_REQUEST`)

| Property | Value |
|----------|-------|
| **Trigger** | When a new pending option request is created. Attaching another file to an existing pending request for the same template and value does not notify again |
| **Method** | `asu_apgap/metadatatags/models.py::MetadataOptionRequest.notify_admins_of_new_request()` |
| **Called From** | `asu_apgap/metadatatags/api/serializers.py::MetadataOptionRequestSerializer.create()` (`POST /api/metadata-tags/option-requests/`) |
| **Recipients** | All Platform Admins |
| **Audience** | `PLATFORM_ADMIN` |
| **Note** | Also used for pending action reminders (see below) |

### Metadata Option Request Approved (`METADATA_OPTION_REQUEST_APPROVED`)

| Property | Value |
|----------|-------|
| **Trigger** | When a Platform Admin approves an option request |
| **Method** | `asu_apgap/metadatatags/models.py::MetadataOptionRequest._notify_attachers_of_approval()`, called by `approve()` |
| **API Endpoint** | `asu_apgap/metadatatags/api/views.py::MetadataOptionRequestViewSet.approve()` at `POST /api/metadata-tags/option-requests/{id}/approve/` |
| **Recipients** | Every distinct user who attached a file to the request (`MetadataOptionRequestFile.requested_by`) |
| **Audience** | `LAB_MEMBER` |

### Metadata Option Request Rejected (`METADATA_OPTION_REQUEST_REJECTED`)

| Property | Value |
|----------|-------|
| **Trigger** | When a Platform Admin rejects an option request |
| **Method** | `asu_apgap/metadatatags/models.py::MetadataOptionRequest._notify_attachers_of_rejection()`, called by `reject()` |
| **API Endpoint** | `asu_apgap/metadatatags/api/views.py::MetadataOptionRequestViewSet.reject()` at `POST /api/metadata-tags/option-requests/{id}/reject/` |
| **Recipients** | Every distinct user who attached a file to the request (`MetadataOptionRequestFile.requested_by`) |
| **Audience** | `LAB_MEMBER` |

---

## Batched File Notifications

`FILE_UPLOADED` and `FILE_FAILED` are not sent once per file. The `File` signal handlers buffer each event and a debounced Celery task sends one notification per uploader, lab, and kind.

| Property | Value |
|----------|-------|
| **Buffering** | `asu_apgap/files/signals.py::notify_file_created()` calls `record_uploaded_file()`. `notify_file_status_change()` calls `record_failed_file()` on a transition into `FAILED`. Both write a `BatchedFileEventBuffer` row |
| **Module** | `asu_apgap/files/celery_tasks/batched_notifications.py` |
| **Celery Task** | `flush_file_event_notifications(user_id, lab_id, kind)`, scheduled on commit with a countdown equal to the debounce window |
| **Debounce Window** | `FILE_UPLOAD_NOTIFICATION_DEBOUNCE_SECONDS` (default 60) for uploads, `FILE_FAILED_NOTIFICATION_DEBOUNCE_SECONDS` (default 300) for failures |
| **Scheduling Guard** | A cache key per (kind, user, lab) stops a large batch from queueing one flush per file. If the cache is unavailable the guard fails open and schedules anyway |
| **Recipients (uploaded)** | Uploader + Lab Directors and Lab Readers + project users in the lab + all Platform Admins |
| **Recipients (failed)** | Uploader + Lab Directors + all Platform Admins |
| **Note** | The flush drains the buffer with `select_for_update` inside one transaction, so a redelivered task cannot send twice. The notification lists every file and names the original name of any file renamed around a name collision. `FILE_PII_DETECTED` is still sent once per file. Files copied into an analytical dataset are not buffered |

---

## Pending Action Reminders

Reminders repeat the original notification for items that are still waiting on someone. They reuse the item's existing notification type, so each user's email preference for that type applies.

| Property | Value |
|----------|-------|
| **Celery Task** | `asu_apgap/notifications/celery_tasks/reminders.py::send_pending_action_reminders()` |
| **Schedule** | `send-pending-action-reminders` in `CELERY_BEAT_SCHEDULE` (`config/settings/base.py`), daily at 9:00 Arizona time. The task does nothing until `cadence_days` have passed since `ReminderSettings.last_run_at` |
| **Settings** | `ReminderSettings` singleton (pk=1): `cadence_days` (default 7), `max_age_days` (default 0, no cutoff), `enabled_notification_types` (empty by default, so every reminder starts off) |
| **Settings API** | `GET`/`PATCH /api/notifications/reminder-settings/` (`ReminderSettingsView`, Platform Admin only). Also editable in Django admin |
| **Delivery** | In-app to all recipients and email to recipients who have not opted out of the type. Notifications have `is_reminder=True` |
| **Superseding** | Each new reminder clears the in-app recipients of earlier reminders for the same target, so the panel shows only the latest one. The earlier rows are kept |

Reminder-capable types (the `REMINDERS` registry):

| Notification Type | What Is Pending | Recipients | Grouping |
|-------------------|-----------------|------------|----------|
| `ACCESS_REQUEST` | `AccessRequest` rows with status `PENDING` | Assigned approvers | One reminder per analytical dataset |
| `ARCHIVE_REQUEST` | `ArchiveRequest` rows with status `PENDING` | Lab admins (`is_lab_admin=True`) of the file's lab + all Platform Admins | One reminder per request |
| `METADATA_OPTION_REQUEST` | `MetadataOptionRequest` rows with status `PENDING` | All Platform Admins | One reminder per request |

---

## System Alerts

System alerts are platform-wide banners, not `Notification` rows. They do not use notification types, recipients, or preferences.

| Property | Value |
|----------|-------|
| **Created In** | Django admin (`SystemAlertAdmin` in `asu_apgap/notifications/admin.py`) |
| **Models** | `SystemAlert` (title, details, status `info`/`warning`/`error`, `is_active`, `expires_at`) and `SystemAlertAcknowledgement` (one row per user and alert) |
| **Shown To** | All authenticated users, for alerts that are active, not expired, and not acknowledged by that user (`SystemAlert.objects.active_for(user)`) |
| **API Endpoints** | `GET /api/notifications/system-alerts/` (pending alerts for the user), `GET /api/notifications/system-alerts/all/` (every alert, for the System Alerts page), `POST /api/notifications/system-alerts/{id}/acknowledge/` |
| **Acknowledge vs Dismiss** | Acknowledging writes a `SystemAlertAcknowledgement` row, so the alert stays hidden on every device. Closing the popup is session only and is not stored |

---

## Notification Audiences

| Audience | Description | Applicable Notification Types |
|----------|-------------|------------------------------|
| `ALL_USERS` | All users can receive these | USER_UPDATED, LAB_USER_ADDED, PROJECT_USER_ADDED, ACCESS_REQUEST_APPROVED, ACCESS_REQUEST_DENIED, BATCH_UPLOAD_REVOKED |
| `PLATFORM_ADMIN` | Only Platform Admins | USER_CREATED, USER_DELETED, LAB_CREATED, METADATA_OPTION_REQUEST |
| `LAB_MEMBER` | Lab Directors and Readers | PROJECT_CREATED, PROJECT_ARCHIVED, PROJECT_DELETED, FILE_UPLOADED, FILE_PII_DETECTED, FILE_FAILED, FILE_DELETED, DATASET_CREATED, DATASET_FILE_STATUS, ACCESS_REQUEST, METADATA_CORRECTED, NOTEBOOK_IDLE_SHUTDOWN, METADATA_OPTION_REQUEST_APPROVED, METADATA_OPTION_REQUEST_REJECTED |
| `LAB_DIRECTOR` | Lab Directors Only | ARCHIVE_REQUEST, LAB_DELETED, LAB_ARCHIVED, LAB_BILLING_ACCOUNT_CHANGED, PROJECT_CREATION_FAILED, NOTEBOOK_ACTIVE_REMINDER, ANALYTICAL_DATASET_FILE_DELETED, ANALYTICAL_DATASET_DELETED |

---

## Test Coverage

Tests for each notification scenario are located in:

| Notification Type | Test File |
|------------------|-----------|
| USER_CREATED, USER_UPDATED, USER_DELETED | `asu_apgap/users/tests/test_signals.py` |
| LAB_CREATED, LAB_USER_ADDED | `asu_apgap/notifications/tests/test_notification_signals.py` |
| PROJECT_CREATED, PROJECT_DELETED | `asu_apgap/projects/tests/test_signals.py` |
| PROJECT_ARCHIVED, PROJECT_USER_ADDED | `asu_apgap/notifications/tests/test_notification_signals.py` |
| FILE_UPLOADED, FILE_PII_DETECTED, FILE_FAILED | `asu_apgap/notifications/tests/test_notification_signals.py` |
| FILE_DELETED | `asu_apgap/files/tests/test_hard_delete.py` |
| DATASET_CREATED, DATASET_FILE_STATUS | `asu_apgap/notifications/tests/test_notification_signals.py` |
| ACCESS_REQUEST, ACCESS_REQUEST_APPROVED, ACCESS_REQUEST_DENIED | `asu_apgap/notifications/tests/test_notification_signals.py` |
| ARCHIVE_REQUEST | `asu_apgap/deletions/tests/test_signals.py` |
| LAB_ARCHIVED, LAB_DELETED | `asu_apgap/labs/tests/test_lab_lifecycle.py` |
| LAB_BILLING_ACCOUNT_CHANGED | `asu_apgap/labs/tests/test_lab_billing_sync.py` |
| PROJECT_CREATION_FAILED | `asu_apgap/projects/tests/test_signals.py`, `asu_apgap/projects/tests/test_celery_tasks.py` |
| NOTEBOOK_ACTIVE_REMINDER, NOTEBOOK_IDLE_SHUTDOWN | `asu_apgap/projects/tests/test_notebook_active_reminders.py` |
| METADATA_CORRECTED | `asu_apgap/metadatatags/tests/test_corrections.py` |
| BATCH_UPLOAD_REVOKED | `asu_apgap/uploads/tests/test_batch_upload_revoke.py` |
| ANALYTICAL_DATASET_FILE_DELETED | `asu_apgap/notifications/tests/test_analytical_dataset_delete_notifications.py` |
| ANALYTICAL_DATASET_DELETED | `asu_apgap/analytical_datasets/tests/test_async_delete.py` |
| METADATA_OPTION_REQUEST, METADATA_OPTION_REQUEST_APPROVED, METADATA_OPTION_REQUEST_REJECTED | `asu_apgap/metadatatags/tests/test_option_requests.py` |
| Batched FILE_UPLOADED / FILE_FAILED | `asu_apgap/files/tests/test_batched_notifications.py` |
| Pending action reminders | `asu_apgap/notifications/tests/test_reminders.py` |
| System alerts | `asu_apgap/notifications/tests/test_system_alerts.py`, `asu_apgap/notifications/tests/test_system_alert_admin.py` |

---

## Email Sending

Email notifications are sent via the SendGrid API. The flow is:

1. Notification is created with `email_recipients` ManyToMany field
2. `m2m_changed` signal on `Notification.email_recipients` triggers `handle_email_recipients_changed()` in `asu_apgap/notifications/signals.py`
3. A Celery task `send_notification_email_task()` is queued
4. The task calls `send_notification_email()` in `asu_apgap/utils/sendgrid_client.py`

---

## Adding New Notification Types

To add a new notification type:

1. Add the type to `NotificationType` enum in `asu_apgap/notifications/models.py`
2. Add the audience mapping in `NOTIFICATION_TYPE_AUDIENCE`
3. Create the signal handler or API endpoint that creates the notification
4. Use `filter_recipients_by_preferences()` to filter recipients
5. Add tests in the appropriate test file
6. Update this documentation
