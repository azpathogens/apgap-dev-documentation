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

## Notification Audiences

| Audience | Description | Applicable Notification Types |
|----------|-------------|------------------------------|
| `ALL_USERS` | All users can receive these | USER_UPDATED, LAB_USER_ADDED, PROJECT_USER_ADDED, ACCESS_REQUEST_APPROVED, ACCESS_REQUEST_DENIED |
| `PLATFORM_ADMIN` | Only Platform Admins | USER_CREATED, USER_DELETED, LAB_CREATED |
| `LAB_MEMBER` | Lab Directors and Readers | PROJECT_CREATED, PROJECT_ARCHIVED, PROJECT_DELETED, FILE_UPLOADED, FILE_PII_DETECTED, FILE_FAILED, FILE_DELETED, DATASET_CREATED, DATASET_FILE_STATUS, ACCESS_REQUEST |
| `LAB_DIRECTOR` | Lab Directors Only | ARCHIVE_REQUEST |

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
