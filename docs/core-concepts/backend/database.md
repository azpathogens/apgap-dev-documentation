---
title: Database Structure
---

# Database Entity Relationship Diagram

This document provides a comprehensive view of the ASU APGAP database schema.

## Visual Diagram

![Entity Relationship Diagram](/images/apgap_erd.png)

## Quick Reference

| Domain             | Models                                                                                                                                                                                                                                                                                                                              |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Organization       | `Organization`, `Lab`, `Project`, `Program`, `LabAutoApproval`, `SeqeraMembershipFailure`                                                                                                                                                                                                                                           |
| Users              | `User`, `LabUser`, `ProjectUser`                                                                                                                                                                                                                                                                                                    |
| Files              | `File`, `Upload`, `BatchUpload`, `BatchedFileEventBuffer`                                                                                                                                                                                                                                                                           |
| Datasets           | `Dataset`, `DatasetFile`, `DatasetProjectAssignment`, `AnalyticalDataset`, `DatasetSubscription`                                                                                                                                                                                                                                    |
| Metadata           | `Key`, `Value`, `MetadataTag`, `FileMetadataTag`, `DatasetMetadataTag`, `SourceType`, `MetadataTemplate`, `MetadataTemplateOption`, `MetadataRequirement`, `KeyAlias`, `MetadataOptionRequest`, `MetadataOptionRequestFile`, `PostAnalysisPublication`, `FileMetadataRedaction`, `LabCustomTag`, `LabCustomTagOption`, `Correction` |
| Access Control     | `AccessRequest`, `AccessRequestApprover`                                                                                                                                                                                                                                                                                            |
| Audit              | `Deletion`, `ArchiveRequest`                                                                                                                                                                                                                                                                                                        |
| Notifications      | `Notification`, `UserNotificationPreference`, `NotificationRead`, `SystemAlert`, `SystemAlertAcknowledgement`, `ReminderSettings`, `ActionItemSettings`                                                                                                                                                                             |
| Validation         | `ValidatorRule`, `CrossFieldRule`, `ValidationRun`, `ValidationIssue`, `RuleOperation`, `RuleTypeDefinition`, `RuleParamDefinition`                                                                                                                                                                                                 |
| Pathogens          | `Pathogen`, `PathogenReportabilityRule`                                                                                                                                                                                                                                                                                             |
| Search & Reporting | `SavedSearch`, `ReportingUpload`, `SavedReport`, `ReportPreset`, `ReportPresetSeed`                                                                                                                                                                                                                                                 |
| Policy & Site      | `AcceptableUsePolicy`, `AcceptableUsePolicyAcknowledgement`, `SitePublicLinks`                                                                                                                                                                                                                                                      |
| Other              | `DomainWhitelist`, `SeqeraWorkspace`                                                                                                                                                                                                                                                                                                |

---

## Model Details

### Organization

| Field                                       | Type    | Constraints | Description                   |
| ------------------------------------------- | ------- | ----------- | ----------------------------- |
| id                                          | int     | PK          | Primary key                   |
| display_name                                | string  | UNIQUE      | Organization name             |
| default_approve_analytical_dataset_requests | boolean |             | Auto-approve dataset requests |
| active                                      | boolean |             | Soft delete flag              |

### Lab

| Field           | Type     | Constraints       | Description                     |
| --------------- | -------- | ----------------- | ------------------------------- |
| id              | int      | PK                | Primary key                     |
| organization_id | int      | FK → Organization | Parent organization             |
| display_name    | string   |                   | Lab name                        |
| description     | text     |                   | Lab description                 |
| active          | boolean  |                   | Active status                   |
| gcs_bucket      | string   |                   | GCS bucket for lab files        |
| project_prefix  | string   | UNIQUE            | Unique prefix for GCP resources |
| build_status    | string   |                   | Cloud Build deployment status   |
| created_by_id   | int      | FK → User         | User who created the lab        |
| created_at      | datetime |                   | Creation timestamp              |
| gcp_project_id  | string   |                   | Cached GCP project ID           |

### LabUser

| Field               | Type    | Constraints | Description             |
| ------------------- | ------- | ----------- | ----------------------- |
| id                  | int     | PK          | Primary key             |
| lab_id              | int     | FK → Lab    | Lab reference           |
| user_id             | int     | FK → User   | User reference          |
| permission_group_id | int     | FK → Group  | Django permission group |
| is_lab_admin        | boolean |             | Lab director flag       |

**Unique Constraint**: (lab_id, user_id)

### LabAutoApproval

A lab director's standing grant that lets a user's analytical dataset access requests for this lab's sequences be auto-approved. No row means no grant.

| Field         | Type     | Constraints | Description                                  |
| ------------- | -------- | ----------- | -------------------------------------------- |
| id            | int      | PK          | Primary key                                  |
| lab_id        | int      | FK → Lab    | Lab granting the auto-approval               |
| user_id       | int      | FK → User   | User whose access requests are auto-approved |
| level         | string   |             | OWN_UPLOADS, ALL_LAB                         |
| granted_by_id | int      | FK → User   | Lab director who set the grant               |
| created_at    | datetime |             | Creation time                                |
| updated_at    | datetime |             | Last update                                  |

**Unique Constraint**: (lab_id, user_id)

### Program

| Field        | Type   | Constraints | Description  |
| ------------ | ------ | ----------- | ------------ |
| id           | int    | PK          | Primary key  |
| display_name | string | UNIQUE      | Program name |

### Project

| Field                  | Type     | Constraints  | Description                 |
| ---------------------- | -------- | ------------ | --------------------------- |
| id                     | int      | PK           | Primary key                 |
| lab_id                 | int      | FK → Lab     | Parent lab                  |
| program_id             | int      | FK → Program | Optional program            |
| display_name           | string   |              | Project name                |
| active                 | boolean  |              | Active status               |
| status                 | string   |              | ACTIVE, ARCHIVED            |
| gcs_bucket             | string   |              | GCS bucket for project      |
| project_prefix         | string   | UNIQUE       | Unique prefix               |
| created_by_id          | int      | FK → User    | Creator                     |
| deleted_by_id          | int      | FK → User    | Who deleted                 |
| archived_by_id         | int      | FK → User    | Who archived                |
| archived_at            | datetime |              | Archive timestamp           |
| deleted_at             | datetime |              | Deletion timestamp          |
| deletion_justification | text     |              | Deletion reason             |
| description            | text     |              | Project description         |
| build_status           | string   |              | Cloud Build status          |
| opt_out_of_seqera      | boolean  |              | Skip Seqera workspace       |
| seqera_workspace_id    | string   |              | Seqera workspace ID         |
| seqera_compute_env_id  | string   |              | Seqera compute env ID       |
| seqera_credentials_id  | string   |              | Seqera credentials ID       |
| gcp_project_id         | string   |              | Cached GCP project ID       |
| seqera_output_bucket   | string   |              | Cached Seqera output bucket |
| vertex_notebook_uri    | string   |              | Cached Vertex notebook URI  |

### ProjectUser

| Field               | Type | Constraints  | Description       |
| ------------------- | ---- | ------------ | ----------------- |
| id                  | int  | PK           | Primary key       |
| project_id          | int  | FK → Project | Project reference |
| user_id             | int  | FK → User    | User reference    |
| permission_group_id | int  | FK → Group   | Permission group  |

**Unique Constraint**: (project_id, user_id)

### SeqeraMembershipFailure

A row exists only while the user is failing to be added to the workspace. It is deleted once the add succeeds.

| Field             | Type     | Constraints  | Description                                                     |
| ----------------- | -------- | ------------ | --------------------------------------------------------------- |
| id                | int      | PK           | Primary key                                                     |
| project_id        | int      | FK → Project | Project whose Seqera workspace the add failed for               |
| user_id           | int      | FK → User    | User who could not be added                                     |
| role              | string   |              | Seqera workspace role the user should have (e.g. admin, launch) |
| error             | text     |              | Last error returned by Seqera                                   |
| last_attempted_at | datetime |              | Last attempt time                                               |

**Unique Constraint**: (project_id, user_id)

### User

| Field             | Type    | Constraints       | Description         |
| ----------------- | ------- | ----------------- | ------------------- |
| id                | int     | PK                | Primary key         |
| name              | string  |                   | Full name           |
| email             | string  | UNIQUE            | Email address       |
| organization_id   | int     | FK → Organization | User's organization |
| is_platform_admin | boolean |                   | Platform admin flag |
| is_data_analyst   | boolean |                   | Data analyst flag   |
| is_active         | boolean |                   | Active status       |
| created_by_id     | int     | FK → User         | Who created         |
| deleted_by_id     | int     | FK → User         | Who deleted         |
| reactivated_by_id | int     | FK → User         | Who reactivated     |

### File

| Field                     | Type     | Constraints            | Description                                                                            |
| ------------------------- | -------- | ---------------------- | -------------------------------------------------------------------------------------- |
| id                        | int      | PK                     | Primary key                                                                            |
| lab_id                    | int      | FK → Lab               | Lab that owns the file                                                                 |
| gcs_file_path             | string   |                        | GCS path                                                                               |
| file_type                 | string   |                        | File extension/type                                                                    |
| file_size                 | bigint   |                        | Size in bytes                                                                          |
| status                    | string   |                        | DRAFT, PRIMARY, WAITING, PROCESSING, PII_DETECTED, UPLOADED, FAILED, ARCHIVED, DELETED |
| created_by_id             | int      | FK → User              | Uploader                                                                               |
| created_at                | datetime |                        | Upload timestamp                                                                       |
| updated_at                | datetime |                        | Last update                                                                            |
| source_type_id            | int      | FK → SourceType        | Sample source type                                                                     |
| original_file_id          | int      | FK → File              | Original if this is a copy                                                             |
| analytical_dataset_id     | int      | FK → AnalyticalDataset | If copied to dataset                                                                   |
| description               | text     |                        | File description                                                                       |
| external_storage_location | string   |                        | Archive location (e.g., NCBI SRA)                                                      |
| external_storage_type     | string   |                        | NCBI_SRA, OTHER                                                                        |
| archived_at               | datetime |                        | Archive timestamp                                                                      |
| deletion_reason           | text     |                        | Reason for deletion                                                                    |

### BatchedFileEventBuffer

Transient buffer for batched `FILE_UPLOADED` and `FILE_FAILED` notifications. Rows are deleted by `flush_file_event_notifications` once the notification is sent.

| Field             | Type     | Constraints | Description                            |
| ----------------- | -------- | ----------- | -------------------------------------- |
| id                | int      | PK          | Primary key                            |
| user_id           | int      | FK → User   | Uploader (nullable)                    |
| lab_id            | int      | FK → Lab    | Lab of the file                        |
| file_id           | int      | FK → File   | File the event is about (nullable)     |
| filename          | string   |             | Filename snapshot at buffer time       |
| original_filename | string   |             | Name before a collision rename, if any |
| kind              | string   |             | UPLOADED, FAILED                       |
| created_at        | datetime |             | Creation time                          |

**Index**: (user_id, lab_id, kind)

### Upload

| Field           | Type     | Constraints      | Description                    |
| --------------- | -------- | ---------------- | ------------------------------ |
| id              | int      | PK               | Primary key                    |
| user_id         | int      | FK → User        | Uploader                       |
| lab_id          | int      | FK → Lab         | Target lab                     |
| file_id         | int      | FK → File        | Associated file                |
| filename        | string   |                  | Original filename              |
| content_type    | string   |                  | MIME type                      |
| gcs_filepath    | string   |                  | GCS path                       |
| ingest_uuid     | uuid     |                  | Unique ingest identifier       |
| time_to_live    | int      |                  | TTL in hours                   |
| created_at      | datetime |                  | Upload start time              |
| status          | string   |                  | CREATED, SUCCEEDED, FAILED     |
| file_size       | bigint   |                  | Size in bytes                  |
| batch_upload_id | int      | FK → BatchUpload | Parent batch (if batch upload) |

### BatchUpload

| Field                             | Type     | Constraints | Description             |
| --------------------------------- | -------- | ----------- | ----------------------- |
| id                                | int      | PK          | Primary key             |
| user_id                           | int      | FK → User   | Creator                 |
| lab_id                            | int      | FK → Lab    | Target lab              |
| batch_service_account_secret_name | string   |             | Secret Manager path     |
| batch_service_account_email       | string   |             | Service account email   |
| ingest_bucket                     | string   |             | Temporary ingest bucket |
| kind                              | string   |             | CLI, BASESPACE          |
| time_to_live                      | int      |             | TTL in hours            |
| description                       | text     |             | Batch description       |
| created_at                        | datetime |             | Creation time           |

### Dataset

| Field                             | Type    | Constraints  | Description              |
| --------------------------------- | ------- | ------------ | ------------------------ |
| id                                | int     | PK           | Primary key              |
| owning_project_id                 | int     | FK → Project | Owner project            |
| searchable                        | boolean |              | Visible in catalog       |
| type                              | string  |              | batch, single_gui_upload |
| created_by_id                     | int     | FK → User    | Creator                  |
| batch_ingest_bucket               | string  |              | Batch ingest bucket      |
| target_gcs_bucket                 | string  |              | Target GCS bucket        |
| display_name                      | string  |              | Dataset name             |
| description                       | text    |              | Dataset description      |
| batch_service_account_email       | string  |              | Batch SA email           |
| batch_service_account_secret_name | string  |              | Batch SA secret          |
| seqera_data_link_id               | string  |              | Seqera data link ID      |

### DatasetFile

| Field         | Type   | Constraints  | Description                                |
| ------------- | ------ | ------------ | ------------------------------------------ |
| id            | int    | PK           | Primary key                                |
| dataset_id    | int    | FK → Dataset | Parent dataset                             |
| gcs_file_path | string |              | GCS path                                   |
| file_type     | string |              | File type                                  |
| file_size     | bigint |              | Size in bytes                              |
| status        | string |              | PROCESSING, PII_DETECTED, UPLOADED, FAILED |
| created_by_id | int    | FK → User    | Uploader                                   |

### DatasetProjectAssignment

| Field               | Type     | Constraints  | Description                          |
| ------------------- | -------- | ------------ | ------------------------------------ |
| id                  | int      | PK           | Primary key                          |
| dataset_id          | int      | FK → Dataset | Dataset                              |
| project_id          | int      | FK → Project | Assigned project                     |
| seqera_data_link_id | string   |              | Seqera data link for this assignment |
| created_at          | datetime |              | Assignment time                      |
| updated_at          | datetime |              | Last update                          |

**Unique Constraint**: (dataset_id, project_id)

### AnalyticalDataset

| Field               | Type     | Constraints  | Description               |
| ------------------- | -------- | ------------ | ------------------------- |
| id                  | int      | PK           | Primary key               |
| name                | string   |              | Dataset name              |
| gcs_bucket          | string   |              | GCS bucket (auto-created) |
| project_id          | int      | FK → Project | Parent project            |
| created_by_id       | int      | FK → User    | Creator                   |
| created_at          | datetime |              | Creation time             |
| updated_at          | datetime |              | Last update               |
| approval_status     | string   |              | PENDING, APPROVED, DENIED |
| description         | text     |              | Description               |
| seqera_data_link_id | string   |              | Seqera data link ID       |

### DatasetSubscription

A metadata-based rule that automatically adds newly promoted PRIMARY files to an analytical dataset when they match.

| Field                 | Type     | Constraints            | Description                               |
| --------------------- | -------- | ---------------------- | ----------------------------------------- |
| id                    | int      | PK                     | Primary key                               |
| analytical_dataset_id | int      | FK → AnalyticalDataset | Dataset the rule is attached to           |
| name                  | string   |                        | Rule name                                 |
| description           | string   |                        | Optional description                      |
| metadata_filters      | json     |                        | List of {key, operator, value} conditions |
| metadata_filter_logic | string   |                        | AND, OR                                   |
| allow_cross_lab       | boolean  |                        | Match files from other labs               |
| is_active             | boolean  |                        | Inactive rules are not evaluated          |
| created_by_id         | int      | FK → User              | Rule owner, used as requester             |
| created_at            | datetime |                        | Creation time                             |
| updated_at            | datetime |                        | Last update                               |

**M2M Relations**: source_types → SourceType

**Unique Constraint**: (lower(name), analytical_dataset_id)

### SourceType

| Field      | Type   | Constraints | Description      |
| ---------- | ------ | ----------- | ---------------- |
| id         | int    | PK          | Primary key      |
| name       | string |             | Source type name |
| sort_order | int    |             | Display order    |

### Key

| Field     | Type   | Constraints | Description                |
| --------- | ------ | ----------- | -------------------------- |
| id        | int    | PK          | Primary key                |
| name      | string | UNIQUE      | Key name (uppercase)       |
| data_type | string |             | TEXT, NUMBER, DATE, SELECT |

### KeyAlias

Records every prior `Key.name` so name-based lookups survive renames. Populated by `Key.save` on rename.

| Field      | Type     | Constraints | Description                   |
| ---------- | -------- | ----------- | ----------------------------- |
| id         | int      | PK          | Primary key                   |
| name       | string   | UNIQUE      | Former key name               |
| key_id     | int      | FK → Key    | Key that now carries the name |
| created_at | datetime |             | Creation time                 |

### Value

| Field | Type   | Constraints | Description            |
| ----- | ------ | ----------- | ---------------------- |
| id    | int    | PK          | Primary key            |
| name  | string | UNIQUE      | Value name (uppercase) |

### MetadataTag

| Field    | Type | Constraints | Description    |
| -------- | ---- | ----------- | -------------- |
| id       | int  | PK          | Primary key    |
| key_id   | int  | FK → Key    | Metadata key   |
| value_id | int  | FK → Value  | Metadata value |

**Unique Constraint**: (key_id, value_id)

### FileMetadataTag

| Field           | Type | Constraints      | Description         |
| --------------- | ---- | ---------------- | ------------------- |
| id              | int  | PK               | Primary key         |
| file_id         | int  | FK → File        | Tagged file         |
| metadata_tag_id | int  | FK → MetadataTag | Applied tag         |
| source_type_id  | int  | FK → SourceType  | Source type context |

**Unique Constraint**: (file_id, metadata_tag_id, source_type_id)

### DatasetMetadataTag

| Field           | Type | Constraints      | Description    |
| --------------- | ---- | ---------------- | -------------- |
| id              | int  | PK               | Primary key    |
| dataset_id      | int  | FK → Dataset     | Tagged dataset |
| metadata_tag_id | int  | FK → MetadataTag | Applied tag    |

**Unique Constraint**: (dataset_id, metadata_tag_id)

### MetadataRequirement

| Field          | Type | Constraints     | Description                  |
| -------------- | ---- | --------------- | ---------------------------- |
| id             | int  | PK              | Primary key                  |
| key_id         | int  | FK → Key        | Required key                 |
| source_type_id | int  | FK → SourceType | For source type (null = all) |

**Unique Constraint**: (key_id, source_type_id)

### MetadataTemplate

| Field           | Type    | Constraints     | Description           |
| --------------- | ------- | --------------- | --------------------- |
| id              | int     | PK              | Primary key           |
| key_id          | int     | FK → Key        | Template key          |
| name            | string  |                 | Template name         |
| source_type_id  | int     | FK → SourceType | For source type       |
| is_required     | boolean |                 | Required field        |
| multiple_select | boolean |                 | Allow multiple values |
| is_core         | boolean |                 | Applies to all types  |
| sort_order      | int     |                 | Display order         |
| value_type      | string  |                 | Value type hint       |

**Unique Constraint**: (key_id, source_type_id)

### MetadataTemplateOption

| Field                | Type | Constraints           | Description     |
| -------------------- | ---- | --------------------- | --------------- |
| id                   | int  | PK                    | Primary key     |
| metadata_template_id | int  | FK → MetadataTemplate | Parent template |
| value_id             | int  | FK → Value            | Option value    |
| sort_order           | int  |                       | Display order   |

**Unique Constraint**: (metadata_template_id, value_id)

### MetadataOptionRequest

A user request to add a new option to a SELECT metadata template. While pending, attached files cannot be promoted to PRIMARY.

| Field                 | Type     | Constraints           | Description                                 |
| --------------------- | -------- | --------------------- | ------------------------------------------- |
| id                    | int      | PK                    | Primary key                                 |
| template_id           | int      | FK → MetadataTemplate | SELECT template the option is requested for |
| proposed_value        | string   |                       | Requested value (normalized)                |
| request_justification | text     |                       | Requester's reason                          |
| status                | string   |                       | PENDING, APPROVED, REJECTED, CANCELLED      |
| reviewed_by_id        | int      | FK → User             | Reviewer                                    |
| reviewed_at           | datetime |                       | Review time                                 |
| review_justification  | text     |                       | Reviewer's reason                           |
| created_at            | datetime |                       | Creation time                               |
| updated_at            | datetime |                       | Last update                                 |

**M2M Relations**: files → File (through MetadataOptionRequestFile)

**Unique Constraint**: (template_id, proposed_value) where status = PENDING

### MetadataOptionRequestFile

| Field                    | Type     | Constraints                | Description                             |
| ------------------------ | -------- | -------------------------- | --------------------------------------- |
| id                       | int      | PK                         | Primary key                             |
| request_id               | int      | FK → MetadataOptionRequest | Parent request                          |
| file_id                  | int      | FK → File                  | Attached file                           |
| requested_by_id          | int      | FK → User                  | User who attached the file              |
| auto_promote_on_approval | boolean  |                            | Promote the file to PRIMARY on approval |
| created_at               | datetime |                            | Creation time                           |

**Unique Constraint**: (request_id, file_id)

### PostAnalysisPublication

A dated set of post-analysis metadata tags on a PRIMARY file. `FileMetadataTag.publication_id` points here. Null means a baseline tag.

| Field           | Type     | Constraints | Description                      |
| --------------- | -------- | ----------- | -------------------------------- |
| id              | int      | PK          | Primary key                      |
| file_id         | int      | FK → File   | Original (non-copy) PRIMARY file |
| status          | string   |             | DRAFT, PUBLISHED                 |
| sequence        | int      |             | Per-file set number              |
| note            | text     |             | Optional note                    |
| created_by_id   | int      | FK → User   | Creator                          |
| created_at      | datetime |             | Creation time                    |
| published_by_id | int      | FK → User   | Who published                    |
| published_at    | datetime |             | Publish time                     |
| updated_at      | datetime |             | Last update                      |

**Unique Constraint**: (file_id) where status = DRAFT (one open draft per file)

### FileMetadataRedaction

Marks one metadata cell (file, key) as redacted. The value is hidden from cross-lab read paths but stays visible to the file's lab, users with approved access, and platform admins.

| Field         | Type     | Constraints | Description   |
| ------------- | -------- | ----------- | ------------- |
| id            | int      | PK          | Primary key   |
| file_id       | int      | FK → File   | File          |
| key_id        | int      | FK → Key    | Redacted key  |
| created_by_id | int      | FK → User   | Who redacted  |
| created_at    | datetime |             | Creation time |
| updated_at    | datetime |             | Last update   |

**Unique Constraint**: (file_id, key_id)

### LabCustomTag

A lab-scoped custom post-analysis tag definition.

| Field           | Type     | Constraints | Description                          |
| --------------- | -------- | ----------- | ------------------------------------ |
| id              | int      | PK          | Primary key                          |
| lab_id          | int      | FK → Lab    | Owning lab                           |
| key_id          | int      | FK → Key    | Shared metadata key                  |
| is_private      | boolean  |             | Values visible only to lab members   |
| multiple_select | boolean  |             | Allow multiple options (SELECT keys) |
| created_by_id   | int      | FK → User   | Creator                              |
| created_at      | datetime |             | Creation time                        |
| updated_at      | datetime |             | Last update                          |

**Unique Constraint**: (lab_id, key_id)

### LabCustomTagOption

| Field             | Type | Constraints       | Description   |
| ----------------- | ---- | ----------------- | ------------- |
| id                | int  | PK                | Primary key   |
| lab_custom_tag_id | int  | FK → LabCustomTag | Parent tag    |
| value_id          | int  | FK → Value        | Option value  |
| sort_order        | int  |                   | Display order |

**Unique Constraint**: (lab_custom_tag_id, value_id)

### Correction

Audit record for a baseline metadata correction on a PRIMARY file. One row per correction.

| Field           | Type     | Constraints | Description                                         |
| --------------- | -------- | ----------- | --------------------------------------------------- |
| id              | int      | PK          | Primary key                                         |
| file_id         | int      | FK → File   | Corrected file (nullable, kept after file deletion) |
| reason          | text     |             | Reason for the correction                           |
| corrected_by_id | int      | FK → User   | Who corrected                                       |
| corrected_at    | datetime |             | Correction time                                     |
| additional_data | json     |             | Per-key before and after snapshot                   |

### ValidatorRule

A field-level validation rule on a `MetadataTemplate`.

| Field                | Type     | Constraints           | Description                                                                                                                                                         |
| -------------------- | -------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| id                   | int      | PK                    | Primary key                                                                                                                                                         |
| metadata_template_id | int      | FK → MetadataTemplate | Template the rule applies to                                                                                                                                        |
| rule_type            | string   |                       | REQUIRED, TYPE_FORMAT, NUMERIC_RANGE, NUMERIC_SINGLE_OR_RANGE, REGEX, ENUM_MATCH, UNIQUE, REFERENCES_MODEL, MUTUALLY_EXCLUSIVE_VALUE, DATE_NOT_FUTURE, DATE_MAX_AGE |
| params               | json     |                       | Rule parameters                                                                                                                                                     |
| severity             | string   |                       | ERROR, WARNING                                                                                                                                                      |
| message_template     | string   |                       | Optional message override                                                                                                                                           |
| is_active            | boolean  |                       | Active flag                                                                                                                                                         |
| sort_order           | int      |                       | Evaluation order                                                                                                                                                    |
| rule_group           | string   |                       | Rules sharing a group form an OR set                                                                                                                                |
| created_at           | datetime |                       | Creation time                                                                                                                                                       |
| updated_at           | datetime |                       | Last update                                                                                                                                                         |

### CrossFieldRule

A validation rule that spans two templates.

| Field             | Type     | Constraints           | Description                                                                                       |
| ----------------- | -------- | --------------------- | ------------------------------------------------------------------------------------------------- |
| id                | int      | PK                    | Primary key                                                                                       |
| source_type_id    | int      | FK → SourceType       | Scope (null = all source types)                                                                   |
| left_template_id  | int      | FK → MetadataTemplate | Left template                                                                                     |
| right_template_id | int      | FK → MetadataTemplate | Right template                                                                                    |
| rule_type         | string   |                       | CROSS_FIELD_COMPARE, CONDITIONAL_REQUIRED, CROSS_FIELD_VALUE_DEPENDENCY, MUTUALLY_EXCLUSIVE_VALUE |
| params            | json     |                       | Rule parameters                                                                                   |
| severity          | string   |                       | ERROR, WARNING                                                                                    |
| message_template  | string   |                       | Optional message override                                                                         |
| is_active         | boolean  |                       | Active flag                                                                                       |
| sort_order        | int      |                       | Evaluation order                                                                                  |
| created_at        | datetime |                       | Creation time                                                                                     |
| updated_at        | datetime |                       | Last update                                                                                       |

### ValidationRun

Audit row for one validation attempt on a file.

| Field                    | Type     | Constraints | Description                                            |
| ------------------------ | -------- | ----------- | ------------------------------------------------------ |
| id                       | int      | PK          | Primary key                                            |
| file_id                  | int      | FK → File   | Validated file                                         |
| triggered_by_id          | int      | FK → User   | Who triggered it                                       |
| trigger                  | string   |             | PREVIEW, PROMOTE, FORCE_PROMOTE, PUBLISH_POST_ANALYSIS |
| passed                   | boolean  |             | Whether validation passed                              |
| acknowledged_warning_ids | json     |             | Warnings the user acknowledged                         |
| error_count              | int      |             | Number of errors                                       |
| warning_count            | int      |             | Number of warnings                                     |
| created_at               | datetime |             | Creation time                                          |

### ValidationIssue

| Field               | Type   | Constraints         | Description                                     |
| ------------------- | ------ | ------------------- | ----------------------------------------------- |
| id                  | int    | PK                  | Primary key                                     |
| run_id              | int    | FK → ValidationRun  | Parent run                                      |
| field_rule_id       | int    | FK → ValidatorRule  | Field rule that raised it (nullable)            |
| cross_field_rule_id | int    | FK → CrossFieldRule | Cross-field rule that raised it (nullable)      |
| template_keys       | json   |                     | Display name snapshot of the templates involved |
| template_ids        | json   |                     | Template ID snapshot, used for the hash         |
| severity            | string |                     | ERROR, WARNING                                  |
| code                | string |                     | Machine-readable issue code                     |
| message             | string |                     | Issue message                                   |
| issue_hash          | string |                     | Stable hash used to match acknowledgements      |

### RuleOperation

An executable validation operation backed by a Python handler.

| Field       | Type     | Constraints | Description                              |
| ----------- | -------- | ----------- | ---------------------------------------- |
| id          | int      | PK          | Primary key                              |
| code        | string   |             | Key into the Python `OPERATION_REGISTRY` |
| kind        | string   |             | field, cross                             |
| label       | string   |             | Display label                            |
| description | text     |             | Description                              |
| is_active   | boolean  |             | Soft-disable flag                        |
| created_at  | datetime |             | Creation time                            |
| updated_at  | datetime |             | Last update                              |

**Unique Constraint**: (code, kind)

### RuleTypeDefinition

| Field        | Type     | Constraints        | Description                                                    |
| ------------ | -------- | ------------------ | -------------------------------------------------------------- |
| id           | int      | PK                 | Primary key                                                    |
| code         | string   |                    | Matches `ValidatorRule.rule_type` / `CrossFieldRule.rule_type` |
| kind         | string   |                    | field, cross (copied from the operation)                       |
| operation_id | int      | FK → RuleOperation | Backing operation (PROTECT)                                    |
| label        | string   |                    | Display label                                                  |
| description  | text     |                    | Description                                                    |
| is_active    | boolean  |                    | Active flag                                                    |
| sort_order   | int      |                    | Display order                                                  |
| created_at   | datetime |                    | Creation time                                                  |
| updated_at   | datetime |                    | Last update                                                    |

**Unique Constraint**: (code, kind)

### RuleParamDefinition

Schema for one parameter of a rule type. Drives the admin editor and params validation.

| Field         | Type     | Constraints             | Description                                                                                                                                                                                                                                               |
| ------------- | -------- | ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| id            | int      | PK                      | Primary key                                                                                                                                                                                                                                               |
| rule_type_id  | int      | FK → RuleTypeDefinition | Parent rule type                                                                                                                                                                                                                                          |
| key           | string   |                         | Param key inside `params`                                                                                                                                                                                                                                 |
| label         | string   |                         | Display label                                                                                                                                                                                                                                             |
| help_text     | text     |                         | Help text                                                                                                                                                                                                                                                 |
| widget_type   | string   |                         | TEXT, NUMBER, BOOLEAN, SELECT, MULTI_SELECT, TAGS, REGEX_TEXTAREA, TEMPLATE_OPTION_SELECT, TEMPLATE_OPTION_MULTI_SELECT, LEFT_TEMPLATE_OPTION_SELECT, LEFT_TEMPLATE_OPTION_MULTI_SELECT, RIGHT_TEMPLATE_OPTION_SELECT, RIGHT_TEMPLATE_OPTION_MULTI_SELECT |
| is_required   | boolean  |                         | Required param                                                                                                                                                                                                                                            |
| default_value | json     |                         | Default for new rules                                                                                                                                                                                                                                     |
| choices       | json     |                         | Allowed values for select widgets                                                                                                                                                                                                                         |
| sort_order    | int      |                         | Display order                                                                                                                                                                                                                                             |
| created_at    | datetime |                         | Creation time                                                                                                                                                                                                                                             |
| updated_at    | datetime |                         | Last update                                                                                                                                                                                                                                               |

**Unique Constraint**: (rule_type_id, key)

### Pathogen

Registry of pathogens tracked for reportability.

| Field       | Type    | Constraints             | Description                                 |
| ----------- | ------- | ----------------------- | ------------------------------------------- |
| id          | int     | PK                      | Primary key                                 |
| category    | string  |                         | Pathogen category                           |
| description | text    |                         | Description                                 |
| reportable  | boolean |                         | Always reportable (overrides rules)         |
| value_id    | int     | FK → Value (one-to-one) | Metadata value that holds the pathogen name |

**History**: tracked with django-simple-history (`HistoricalPathogen`)

### PathogenReportabilityRule

A conditional rule that makes a file tagged with the pathogen reportable when `Pathogen.reportable` is false.

| Field                 | Type     | Constraints   | Description                               |
| --------------------- | -------- | ------------- | ----------------------------------------- |
| id                    | int      | PK            | Primary key                               |
| pathogen_id           | int      | FK → Pathogen | Parent pathogen                           |
| name                  | string   |               | Optional rule name                        |
| metadata_filters      | json     |               | List of {key, operator, value} conditions |
| metadata_filter_logic | string   |               | AND, OR                                   |
| is_active             | boolean  |               | Active flag                               |
| created_at            | datetime |               | Creation time                             |
| updated_at            | datetime |               | Last update                               |

**History**: tracked with django-simple-history (`HistoricalPathogenReportabilityRule`)

### AccessRequest

| Field                 | Type     | Constraints            | Description                 |
| --------------------- | -------- | ---------------------- | --------------------------- |
| id                    | int      | PK                     | Primary key                 |
| user_id               | int      | FK → User              | Requester                   |
| analytical_dataset_id | int      | FK → AnalyticalDataset | Target dataset              |
| file_id               | int      | FK → File              | Target file                 |
| status                | string   |                        | PENDING, APPROVED, REJECTED |
| denied_by_id          | int      | FK → User              | Who denied                  |
| denial_reason         | text     |                        | Denial reason               |
| created_at            | datetime |                        | Request time                |
| updated_at            | datetime |                        | Last update                 |

### AccessRequestApprover

| Field             | Type     | Constraints        | Description    |
| ----------------- | -------- | ------------------ | -------------- |
| id                | int      | PK                 | Primary key    |
| access_request_id | int      | FK → AccessRequest | Parent request |
| approver_id       | int      | FK → User          | Approver user  |
| created_at        | datetime |                    | Approval time  |
| updated_at        | datetime |                    | Last update    |

### Notification

| Field                     | Type     | Constraints      | Description                           |
| ------------------------- | -------- | ---------------- | ------------------------------------- |
| id                        | int      | PK               | Primary key                           |
| title                     | string   |                  | Notification title                    |
| status                    | string   |                  | info, warning, error, failed, success |
| created_at                | datetime |                  | Creation time                         |
| details                   | text     |                  | Notification body                     |
| content_type_id           | int      | FK → ContentType | Generic FK type                       |
| object_id                 | int      |                  | Generic FK ID                         |
| enable_email_notification | boolean  |                  | Send email                            |
| csv_attachment            | text     |                  | CSV content for email                 |
| notification              | string   |                  | Notification type enum                |

**M2M Relations**: email_recipients → User, inapp_recipients → User

### UserNotificationPreference

| Field         | Type     | Constraints | Description       |
| ------------- | -------- | ----------- | ----------------- |
| id            | int      | PK          | Primary key       |
| user_id       | int      | FK → User   | User              |
| notification  | string   |             | Notification type |
| email_enabled | boolean  |             | Email preference  |
| created_at    | datetime |             | Creation time     |
| updated_at    | datetime |             | Last update       |

**Unique Constraint**: (user_id, notification)

### NotificationRead

Per-user read state for an in-app notification. No row means unread.

| Field           | Type     | Constraints       | Description  |
| --------------- | -------- | ----------------- | ------------ |
| id              | int      | PK                | Primary key  |
| user_id         | int      | FK → User         | Reader       |
| notification_id | int      | FK → Notification | Notification |
| read_at         | datetime |                   | Read time    |

**Unique Constraint**: (user_id, notification_id)

### SystemAlert

Platform-wide alert created in Django admin and shown to all authenticated users.

| Field      | Type     | Constraints | Description                      |
| ---------- | -------- | ----------- | -------------------------------- |
| id         | int      | PK          | Primary key                      |
| title      | string   |             | Alert title                      |
| details    | text     |             | Alert message                    |
| status     | string   |             | info, warning, error             |
| is_active  | boolean  |             | Active flag                      |
| expires_at | datetime |             | Stops displaying after this time |
| created_at | datetime |             | Creation time                    |
| updated_at | datetime |             | Last update                      |

### SystemAlertAcknowledgement

| Field           | Type     | Constraints      | Description          |
| --------------- | -------- | ---------------- | -------------------- |
| id              | int      | PK               | Primary key          |
| user_id         | int      | FK → User        | User                 |
| alert_id        | int      | FK → SystemAlert | Acknowledged alert   |
| acknowledged_at | datetime |                  | Acknowledgement time |

**Unique Constraint**: (user_id, alert_id)

### ReminderSettings

Singleton (pk=1) settings for pending action reminders.

| Field                      | Type     | Constraints | Description                                   |
| -------------------------- | -------- | ----------- | --------------------------------------------- |
| id                         | int      | PK          | Primary key                                   |
| cadence_days               | int      |             | Days between reminder rounds (default 7)      |
| last_run_at                | datetime |             | Last reminder round                           |
| max_age_days               | int      |             | Skip requests older than this (0 = no cutoff) |
| enabled_notification_types | string[] |             | Notification types with reminders on          |
| updated_at                 | datetime |             | Last update                                   |

### ActionItemSettings

Singleton (pk=1) settings for the dashboard "Needs attention" card.

| Field            | Type | Constraints | Description                                          |
| ---------------- | ---- | ----------- | ---------------------------------------------------- |
| id               | int  | PK          | Primary key                                          |
| stale_after_days | int  |             | Items older than this drop off the list (default 30) |

### Deletion

| Field                 | Type     | Constraints      | Description           |
| --------------------- | -------- | ---------------- | --------------------- |
| id                    | int      | PK               | Primary key           |
| content_type_id       | int      | FK → ContentType | Deleted object type   |
| object_id             | int      |                  | Deleted object ID     |
| object_representation | string   |                  | String representation |
| object_model_name     | string   |                  | Model name            |
| justification         | text     |                  | Deletion reason       |
| deleted_by_id         | int      | FK → User        | Who deleted           |
| deleted_at            | datetime |                  | Deletion time         |
| additional_data       | json     |                  | Extra metadata        |

### ArchiveRequest

| Field                     | Type     | Constraints      | Description               |
| ------------------------- | -------- | ---------------- | ------------------------- |
| id                        | int      | PK               | Primary key               |
| content_type_id           | int      | FK → ContentType | Object type               |
| object_id                 | int      |                  | Object ID                 |
| requested_by_id           | int      | FK → User        | Requester                 |
| status                    | string   |                  | PENDING, APPROVED, DENIED |
| justification             | text     |                  | Archive reason            |
| external_storage_location | string   |                  | External storage URL      |
| external_storage_type     | string   |                  | NCBI_SRA, OTHER           |
| retention_requirement_met | boolean  |                  | Met retention period      |
| reviewed_by_id            | int      | FK → User        | Reviewer                  |
| reviewed_at               | datetime |                  | Review time               |
| denial_reason             | text     |                  | Denial reason             |
| created_at                | datetime |                  | Request time              |
| updated_at                | datetime |                  | Last update               |

### DomainWhitelist

| Field       | Type     | Constraints | Description        |
| ----------- | -------- | ----------- | ------------------ |
| id          | int      | PK          | Primary key        |
| domain      | string   | UNIQUE      | Allowed domain     |
| description | string   |             | Domain description |
| created_at  | datetime |             | Creation time      |
| updated_at  | datetime |             | Last update        |

### SeqeraWorkspace

| Field      | Type   | Constraints  | Description     |
| ---------- | ------ | ------------ | --------------- |
| id         | int    | PK           | Primary key     |
| project_id | int    | FK → Project | Parent project  |
| name       | string |              | Workspace name  |
| owner      | string |              | Workspace owner |

### SavedSearch

| Field                 | Type     | Constraints | Description                |
| --------------------- | -------- | ----------- | -------------------------- |
| id                    | int      | PK          | Primary key                |
| created_by_id         | int      | FK → User   | Creator                    |
| lab_id                | int      | FK → Lab    | Lab the search belongs to  |
| name                  | string   |             | Display name               |
| search                | text     |             | Search query text          |
| metadata_filters      | json     |             | Metadata filter conditions |
| metadata_filter_logic | string   |             | AND, OR                    |
| source_types          | json     |             | Source type IDs            |
| shared_with_lab       | boolean  |             | Visible to all lab members |
| show_in_sequences     | boolean  |             | Show in the Sequences tab  |
| show_in_data_catalog  | boolean  |             | Show in the Data Catalog   |
| created_at            | datetime |             | Creation time              |
| updated_at            | datetime |             | Last update                |

### ReportingUpload

Tabular data a user uploads to chart in a project's reporting workspace.

| Field            | Type     | Constraints  | Description             |
| ---------------- | -------- | ------------ | ----------------------- |
| id               | int      | PK           | Primary key             |
| project_id       | int      | FK → Project | Owning project          |
| created_by_id    | int      | FK → User    | Uploader                |
| name             | string   |              | Display name            |
| raw_tabular_data | text     |              | Raw uploaded data (CSV) |
| created_at       | datetime |              | Creation time           |
| updated_at       | datetime |              | Last update             |

### SavedReport

A saved Perspective view scoped to a project. Data source precedence: `reporting_upload`, then `analytical_dataset`, then `data_scope`.

| Field                 | Type     | Constraints            | Description                     |
| --------------------- | -------- | ---------------------- | ------------------------------- |
| id                    | int      | PK                     | Primary key                     |
| created_by_id         | int      | FK → User              | Creator                         |
| project_id            | int      | FK → Project           | Owning project                  |
| reporting_upload_id   | int      | FK → ReportingUpload   | Uploaded data source (optional) |
| analytical_dataset_id | int      | FK → AnalyticalDataset | Dataset data source (optional)  |
| data_scope            | string   |                        | project, catalog                |
| name                  | string   |                        | Display name                    |
| description           | text     |                        | Description                     |
| config                | json     |                        | Saved Perspective viewer state  |
| created_at            | datetime |                        | Creation time                   |
| updated_at            | datetime |                        | Last update                     |

### ReportPreset

A platform-wide Perspective view any authenticated user can open. Writable only by platform admins.

| Field         | Type     | Constraints | Description                    |
| ------------- | -------- | ----------- | ------------------------------ |
| id            | int      | PK          | Primary key                    |
| created_by_id | int      | FK → User   | Platform admin who created it  |
| name          | string   |             | Display name                   |
| description   | text     |             | Description                    |
| display_order | int      |             | Sort order in the preset bar   |
| config        | json     |             | Saved Perspective viewer state |
| created_at    | datetime |             | Creation time                  |
| updated_at    | datetime |             | Last update                    |

### ReportPresetSeed

Ledger of shipped presets already seeded, so a preset an admin deletes is not recreated on the next deploy.

| Field      | Type     | Constraints | Description                    |
| ---------- | -------- | ----------- | ------------------------------ |
| id         | int      | PK          | Primary key                    |
| key        | string   | UNIQUE      | Stable key of a shipped preset |
| created_at | datetime |             | When it was first seeded       |

### AcceptableUsePolicy

Versioned Acceptable Use Policy authored in Django admin. Publishing a version archives the previously published one.

| Field           | Type     | Constraints | Description                |
| --------------- | -------- | ----------- | -------------------------- |
| id              | int      | PK          | Primary key                |
| version         | string   | UNIQUE      | Revision label             |
| title           | string   |             | Policy title               |
| body            | text     |             | Policy text (Markdown)     |
| status          | string   |             | draft, published, archived |
| published_at    | datetime |             | Publish time               |
| published_by_id | int      | FK → User   | Who published              |
| created_at      | datetime |             | Creation time              |
| updated_at      | datetime |             | Last update                |

### AcceptableUsePolicyAcknowledgement

| Field           | Type     | Constraints              | Description                    |
| --------------- | -------- | ------------------------ | ------------------------------ |
| id              | int      | PK                       | Primary key                    |
| user_id         | int      | FK → User                | User                           |
| policy_id       | int      | FK → AcceptableUsePolicy | Acknowledged version (PROTECT) |
| acknowledged_at | datetime |                          | Acknowledgement time           |
| user_agent      | string   |                          | Browser user agent             |

**Unique Constraint**: (user_id, policy_id)

### SitePublicLinks

Singleton (pk=1) row for environment-specific links shown across the site.

| Field          | Type   | Constraints | Description    |
| -------------- | ------ | ----------- | -------------- |
| id             | int    | PK          | Primary key    |
| user_guide_url | string |             | User guide URL |

---

## Relationship Summary

### One-to-Many Relationships

| Parent                  | Child                              | Foreign Key                                  |
| ----------------------- | ---------------------------------- | -------------------------------------------- |
| Organization            | Lab                                | lab.organization_id                          |
| Organization            | User                               | user.organization_id                         |
| Lab                     | Project                            | project.lab_id                               |
| Lab                     | File                               | file.lab_id                                  |
| Lab                     | LabUser                            | labuser.lab_id                               |
| Lab                     | Upload                             | upload.lab_id                                |
| Lab                     | BatchUpload                        | batchupload.lab_id                           |
| Program                 | Project                            | project.program_id                           |
| Project                 | ProjectUser                        | projectuser.project_id                       |
| Project                 | AnalyticalDataset                  | analyticaldataset.project_id                 |
| Project                 | Dataset                            | dataset.owning_project_id                    |
| Project                 | SeqeraWorkspace                    | seqeraworkspace.project_id                   |
| User                    | LabUser                            | labuser.user_id                              |
| User                    | ProjectUser                        | projectuser.user_id                          |
| User                    | Upload                             | upload.user_id                               |
| User                    | BatchUpload                        | batchupload.user_id                          |
| User                    | File                               | file.created_by_id                           |
| User                    | AccessRequest                      | accessrequest.user_id                        |
| File                    | Upload                             | upload.file_id                               |
| File                    | File                               | file.original_file_id (copies)               |
| File                    | FileMetadataTag                    | filemetadatatag.file_id                      |
| File                    | AccessRequest                      | accessrequest.file_id                        |
| BatchUpload             | Upload                             | upload.batch_upload_id                       |
| Dataset                 | DatasetFile                        | datasetfile.dataset_id                       |
| AnalyticalDataset       | File                               | file.analytical_dataset_id                   |
| AnalyticalDataset       | AccessRequest                      | accessrequest.analytical_dataset_id          |
| SourceType              | File                               | file.source_type_id                          |
| SourceType              | MetadataTemplate                   | metadatatemplate.source_type_id              |
| Key                     | MetadataTag                        | metadatatag.key_id                           |
| Key                     | MetadataTemplate                   | metadatatemplate.key_id                      |
| Value                   | MetadataTag                        | metadatatag.value_id                         |
| MetadataTag             | FileMetadataTag                    | filemetadatatag.metadata_tag_id              |
| MetadataTag             | DatasetMetadataTag                 | datasetmetadatatag.metadata_tag_id           |
| MetadataTemplate        | MetadataTemplateOption             | metadatatemplateoption.metadata_template_id  |
| AccessRequest           | AccessRequestApprover              | accessrequestapprover.access_request_id      |
| Lab                     | LabAutoApproval                    | labautoapproval.lab_id                       |
| Lab                     | LabCustomTag                       | labcustomtag.lab_id                          |
| Lab                     | SavedSearch                        | savedsearch.lab_id                           |
| Lab                     | BatchedFileEventBuffer             | batchedfileeventbuffer.lab_id                |
| Project                 | SeqeraMembershipFailure            | seqeramembershipfailure.project_id           |
| Project                 | ReportingUpload                    | reportingupload.project_id                   |
| Project                 | SavedReport                        | savedreport.project_id                       |
| AnalyticalDataset       | DatasetSubscription                | datasetsubscription.analytical_dataset_id    |
| File                    | PostAnalysisPublication            | postanalysispublication.file_id              |
| File                    | FileMetadataRedaction              | filemetadataredaction.file_id                |
| File                    | Correction                         | correction.file_id                           |
| File                    | ValidationRun                      | validationrun.file_id                        |
| PostAnalysisPublication | FileMetadataTag                    | filemetadatatag.publication_id               |
| Key                     | KeyAlias                           | keyalias.key_id                              |
| MetadataTemplate        | MetadataOptionRequest              | metadataoptionrequest.template_id            |
| MetadataTemplate        | ValidatorRule                      | validatorrule.metadata_template_id           |
| MetadataOptionRequest   | MetadataOptionRequestFile          | metadataoptionrequestfile.request_id         |
| LabCustomTag            | LabCustomTagOption                 | labcustomtagoption.lab_custom_tag_id         |
| ValidationRun           | ValidationIssue                    | validationissue.run_id                       |
| RuleOperation           | RuleTypeDefinition                 | ruletypedefinition.operation_id              |
| RuleTypeDefinition      | RuleParamDefinition                | ruleparamdefinition.rule_type_id             |
| Pathogen                | PathogenReportabilityRule          | pathogenreportabilityrule.pathogen_id        |
| Notification            | NotificationRead                   | notificationread.notification_id             |
| SystemAlert             | SystemAlertAcknowledgement         | systemalertacknowledgement.alert_id          |
| AcceptableUsePolicy     | AcceptableUsePolicyAcknowledgement | acceptableusepolicyacknowledgement.policy_id |
| ReportingUpload         | SavedReport                        | savedreport.reporting_upload_id              |

### Many-to-Many Relationships

| Model A               | Model B          | Through Table                                        |
| --------------------- | ---------------- | ---------------------------------------------------- |
| Dataset               | Project          | DatasetProjectAssignment                             |
| MetadataTag           | Dataset          | DatasetMetadataTag                                   |
| MetadataTag           | File             | FileMetadataTag                                      |
| Notification          | User (email)     | notification_email_recipients                        |
| Notification          | User (inapp)     | notification_inapp_recipients                        |
| AccessRequest         | User (approvers) | AccessRequestApprover                                |
| MetadataOptionRequest | File             | MetadataOptionRequestFile                            |
| DatasetSubscription   | SourceType       | analytical_datasets_datasetsubscription_source_types |
