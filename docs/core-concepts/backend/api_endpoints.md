# API Endpoints Reference

This document provides a comprehensive reference of all available API endpoints in the ASU APGAP backend.

**Base URL:** `/api/`

**Authentication:** All endpoints require authentication unless otherwise noted. Use JWT tokens obtained from the authentication endpoints.

---

## Authentication

**Base Path:** `/authentication/`

**POST `/authentication/login/`**

Login with email/password credentials.

**Request:**

```json
{
  "email": "user@example.com",
  "password": "your-password"
}
```

**Response:**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1...",
  "user": {
    "pk": 1,
    "email": "user@example.com"
  }
}
```

**POST `/authentication/google/login/`**

Login with Google OAuth code.

**Request:**

```json
{
  "code": "google-oauth-authorization-code"
}
```

**POST `/authentication/token/refresh/`**

Refresh access token.

**Request:**

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1..."
}
```

**Response:**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1..."
}
```

**POST `/authentication/token/verify/`**

Verify token validity.

**Request:**

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1..."
}
```

---

## Users

**Base Path:** `/api/users/`

**GET `/api/users/`**

List all users.

**Response:**

```json
[
  {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "first_name": "John",
    "last_name": "Doe",
    "is_platform_admin": false,
    "is_data_analyst": false,
    "is_active": true,
    "organization": {
      "id": 1,
      "display_name": "Arizona State University"
    }
  }
]
```

**POST `/api/users/`**

Create a new user.

**Request:**

```json
{
  "email": "newuser@example.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "organization": 1,
  "is_platform_admin": false,
  "is_data_analyst": false,
  "lab": 1,
  "is_lab_admin": false,
  "project": 1
}
```

**GET `/api/users/{id}/`**

Retrieve user details with permissions and memberships.

**Response:**

```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "first_name": "John",
  "last_name": "Doe",
  "is_platform_admin": false,
  "is_data_analyst": false,
  "is_active": true,
  "is_azdhs_user": false,
  "organization": {
    "id": 1,
    "display_name": "Arizona State University"
  },
  "permissions": {
    "groups": ["Lab Director"],
    "permissions": ["labs.view_lab", "labs.change_lab"]
  },
  "lab_memberships": [
    {
      "id": 1,
      "display_name": "Genomics Lab",
      "role": "Lab Director",
      "projects": [
        {
          "id": 1,
          "display_name": "COVID-19 Sequencing",
          "role": "Bioinformatics User"
        }
      ]
    }
  ],
  "project_memberships": [
    {
      "id": 1,
      "display_name": "COVID-19 Sequencing",
      "role": "Bioinformatics User"
    }
  ]
}
```

**PATCH `/api/users/{id}/`**

Update user.

**Request:**

```json
{
  "first_name": "John",
  "last_name": "Smith",
  "organization": 2,
  "is_platform_admin": true
}
```

**DELETE `/api/users/{id}/`**

Soft delete (deactivate) user.

**GET `/api/users/me/`**

Get current authenticated user's details.

**POST `/api/users/{id}/reactivate/`**

Reactivate a deactivated user.

**Additional Endpoints**

| Method   | Endpoint                      | Permission         | Description                                                                                 |
| -------- | ----------------------------- | ------------------ | ------------------------------------------------------------------------------------------- |
| GET      | `/api/users/aup-report/`      | Platform Admin     | Download a CSV of every user and the Acceptable Use Policy version they accepted.           |
| GET      | `/api/users/aup-report/rows/` | Platform Admin     | The same report as JSON, for the on-screen table.                                           |
| GET/POST | `/api/users/orientation/`     | Any authenticated  | GET returns `{"has_seen_orientation": bool}`. POST sets it to `true` (idempotent).          |

---

## Organizations

**Base Path:** `/api/organizations/`

**GET `/api/organizations/`**

List all organizations.

**Response:**

```json
[
  {
    "id": 1,
    "display_name": "Arizona State University",
    "active": true,
    "default_approve_analytical_dataset_requests": false
  }
]
```

**POST `/api/organizations/`**

Create a new organization.

**Request:**

```json
{
  "display_name": "New Organization",
  "default_approve_analytical_dataset_requests": false
}
```

**GET `/api/organizations/{id}/`**

Retrieve organization details.

**PATCH `/api/organizations/{id}/`**

Update organization settings.

**Request:**

```json
{
  "default_approve_analytical_dataset_requests": true
}
```

**DELETE `/api/organizations/{id}/`**

Soft delete organization (sets active=false). Fails if organization has users.

---

## Labs

**Base Path:** `/api/labs/`

**GET `/api/labs/`**

List labs accessible to user.

**Response:**

```json
[
  {
    "id": 1,
    "display_name": "Genomics Lab",
    "description": "Main genomics research lab",
    "project_id": "gcp-project-123",
    "organization": {
      "id": 1,
      "display_name": "Arizona State University"
    },
    "projects": [
      {
        "id": 1,
        "display_name": "COVID-19 Sequencing",
        "status": "ACTIVE"
      }
    ]
  }
]
```

**POST `/api/labs/`**

Create a new lab.

**Request:**

```json
{
  "display_name": "New Lab",
  "description": "Lab description",
  "organization": 1,
  "lab_director_id": 1
}
```

**GET `/api/labs/{id}/members/`**

Get all lab members.

**Response:**

```json
{
  "lab_users": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "role": "Lab Director",
      "is_lab_admin": true,
      "organization": { "id": 1, "display_name": "ASU" }
    }
  ],
  "project_users": [
    {
      "id": 1,
      "user_id": 2,
      "user_name": "Jane Smith",
      "user_email": "jane@example.com",
      "project_id": 1,
      "project_name": "COVID-19 Sequencing",
      "permission_id": 3,
      "permission_name": "Bioinformatics User"
    }
  ]
}
```

**POST `/api/labs/{id}/assign-user/`**

Assign a user to the lab.

**Request:**

```json
{
  "user_id": 2,
  "is_lab_director": false
}
```

**POST `/api/labs/{id}/remove-user/`**

Remove a user from the lab.

**Request:**

```json
{
  "user_id": 2
}
```

**Additional Endpoints**

Lab detail actions use `LabHierarchicalPermission` unless noted. Lifecycle actions answer 400 with a `detail` reason when the transition is not allowed.

| Method | Endpoint                             | Permission                                  | Description                                                                                                         |
| ------ | ------------------------------------ | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| GET    | `/api/labs/{id}/build-log/`          | Can view the lab                            | Last captured GCP/Cloud Build provisioning error: `{"last_build_error": ""}`.                                       |
| GET    | `/api/labs/recent-activity/`         | Platform Admin                              | One row per lab with activity in the last `?days=` (1 to 365, default 7): uploads, updates, builds, failures.       |
| GET    | `/api/labs/{id}/project-users/`      | Can view the lab                            | Distinct users with project assignments in the lab, each with their assignments and auto-approval level.           |
| POST   | `/api/labs/{id}/auto-approval/`      | Lab Director (`change_lab`), Platform Admin | Set a lab member's dataset auto-approval level. Body: `{"user_id": 2, "level": "OWN_UPLOADS"}`; level is `NONE`, `OWN_UPLOADS` or `ALL_LAB`. |
| POST   | `/api/labs/{id}/deactivate/`         | Platform Admin                              | Make the lab read-only once every project is archived.                                                              |
| POST   | `/api/labs/{id}/reactivate/`         | Platform Admin                              | Return an inactive lab to active.                                                                                   |
| POST   | `/api/labs/{id}/archive/`            | Platform Admin                              | Tear down the lab's GCP resources and keep its record. Body: `{"archive_note": "..."}` (min 20 chars). Returns 202. |
| POST   | `/api/labs/{id}/delete/`             | Platform Admin                              | Tear down an empty lab's GCP resources and remove it with no record kept. Returns 202.                              |
| POST   | `/api/labs/{id}/retry-teardown/`     | Platform Admin                              | Pick up a stalled or failed archive or delete teardown. Returns 202.                                                |
| POST   | `/api/labs/{id}/request-archive/`    | Lab Director of the lab                     | Ask platform admins to archive the lab. Body: `{"justification": "..."}` (min 20 chars). Returns 201.               |

---

## Projects

**Base Path:** `/api/projects/`

**GET `/api/projects/`**

List projects accessible to user.

**Query Parameters:**

- `lab` - Filter by lab ID
- `status` - Filter by status (ACTIVE, ARCHIVED)

**Response:**

```json
[
  {
    "id": 1,
    "display_name": "COVID-19 Sequencing",
    "lab": 1,
    "program": null,
    "active": true,
    "status": "ACTIVE",
    "description": "Project description",
    "gcs_bucket": "project-bucket-123",
    "output_bucket": "gs://output-bucket",
    "opt_out_of_seqera": false,
    "build_status": "SUCCESS"
  }
]
```

**POST `/api/projects/`**

Create a new project.

**Request:**

```json
{
  "display_name": "New Project",
  "lab": 1,
  "description": "Project description",
  "opt_out_of_seqera": false
}
```

**GET `/api/projects/{id}/resource-detail/`**

Get detailed project information.

**Response:**

```json
{
  "id": 1,
  "display_name": "COVID-19 Sequencing",
  "description": "Project description",
  "opt_out_of_seqera": false,
  "seqera_launchpad_url": "https://tower.nf/...",
  "vertex_notebook_uri": "https://notebooks.cloud.google.com/...",
  "output_bucket": "gs://output-bucket",
  "project_id": "gcp-project-id",
  "project_users": [...],
  "lab_directors": [...]
}
```

**POST `/api/projects/{id}/archive/`**

Archive a project (Lab Director only).

**POST `/api/projects/{id}/hard-delete/`**

Permanently delete a project (Platform Admin only).

**Request:**

```json
{
  "deletion_justification": "Reason for deletion (minimum 10 characters)"
}
```

**Additional Endpoints**

"Project access" means the caller passes `ProjectHierarchicalPermission` for that project (global permission, lab membership, or project membership).

| Method | Endpoint                                         | Permission                                                    | Description                                                                                          |
| ------ | ------------------------------------------------ | ------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| GET    | `/api/projects/permission-groups/`               | Any authenticated                                             | Groups assignable on a project (excludes Platform Admin, Lab Director and Data Analyst).             |
| GET    | `/api/projects/manage-access-project-list/`      | Lab Director (403 otherwise)                                  | Every project in an active lab, for managing project access.                                         |
| GET    | `/api/projects/{id}/build-status/`               | Project access                                                | Cloud Build status: `{"status": "..."}`. 404 when the project has no build.                           |
| GET    | `/api/projects/{id}/build-log/`                  | Project access                                                | Last captured provisioning error: `{"last_build_error": ""}`.                                        |
| GET    | `/api/projects/{id}/seqera-log/`                 | Platform Admin                                                | Full Seqera provisioning error detail: `{"seqera_error_detail": ""}`.                                |
| POST   | `/api/projects/{id}/retry-seqera-provisioning/`  | Platform Admin                                                | Re-run Seqera provisioning in Celery. Returns 202. 400 if the project opted out of Seqera.           |
| GET    | `/api/projects/{id}/notebook-status/`            | Project access                                                | Vertex AI Workbench notebook state: `{"state": "ACTIVE"}` (or `STOPPED`, `UNKNOWN`, ...).            |
| POST   | `/api/projects/{id}/notebook-start/`             | Project member, Lab Director of the lab, Platform Admin       | Start the project's notebook. Returns 202 with `{"state": "..."}`.                                   |
| POST   | `/api/projects/{id}/notebook-stop/`              | Project member, Lab Director of the lab, Platform Admin       | Stop the project's notebook. Returns 202 with `{"state": "..."}`.                                    |
| POST   | `/api/projects/{id}/retry-notebook-access/`      | Platform Admin                                                | Re-sync the notebook viewer IAM. Returns `{"detail", "success"}`.                                    |
| POST   | `/api/projects/{id}/retry-seqera-member/`        | Lab Director of the lab, Platform Admin                       | Retry adding one user to the Seqera workspace. Body: `{"failure_id": 3}`. Returns `{"detail", "success"}`. |

**Project Users**

**Base Path:** `/api/project-users/`

**POST `/api/project-users/`**

Add user to project.

**Request:**

```json
{
  "user": 2,
  "project": 1,
  "permission_group": 3
}
```

**Response:**

```json
{
  "id": 1,
  "user": {
    "id": 2,
    "email": "jane@example.com",
    "name": "Jane Smith",
    "organization": "ASU"
  },
  "project": {
    "id": 1,
    "display_name": "COVID-19 Sequencing"
  },
  "permission_group": {
    "id": 3,
    "name": "Bioinformatics User"
  }
}
```

**PATCH `/api/project-users/{id}/`**

Update project user role.

**Request:**

```json
{
  "permission_group": 4
}
```

---

## Files

**Base Path:** `/api/files/`

**GET `/api/files/`**

List files with optional pagination.

**Query Parameters:**

- `lab` - Filter by lab ID
- `status` - Filter by status (DRAFT, PROCESSING, PRIMARY, ARCHIVED)
- `created_by` - Filter by creator ID
- `pagination` - Enable pagination (`true`)
- `page`, `page_size` - Pagination controls
- `search` - Search in gcs_file_path

**Response:**

```json
[
  {
    "id": 1,
    "lab": 1,
    "lab_name": "Genomics Lab",
    "gcs_file_path": "lab-1/sample.fastq",
    "file_type": "fastq",
    "file_size": 1048576,
    "status": "PRIMARY",
    "description": null,
    "created_by": 1,
    "created_by_name": "John Doe",
    "created_at": "2024-01-15T10:30:00Z",
    "source_type": 1,
    "source_type_name": "Illumina",
    "batch_upload_id": null,
    "batch_upload_name": null,
    "copied_to_datasets": []
  }
]
```

**POST `/api/files/`**

Create file record or upload file.

**Request (upload with file):**

```
Content-Type: multipart/form-data

file: (binary file data)
lab: 1
```

**Request (metadata only):**

```json
{
  "lab": 1,
  "gcs_file_path": "path/to/file.txt",
  "file_type": "txt",
  "file_size": 1024
}
```

**GET `/api/files/{id}/`**

Retrieve file details.

**Response:**

```json
{
  "id": 1,
  "lab": { "id": 1, "display_name": "Genomics Lab", ... },
  "gcs_file_path": "lab-1/sample.fastq",
  "gcs_url": "gs://bucket/lab-1/sample.fastq",
  "file_type": "fastq",
  "file_size": 1048576,
  "status": "PRIMARY",
  "description": null,
  "created_by": 1,
  "created_by_email": "john@example.com",
  "created_by_name": "John Doe",
  "meets_retention_requirement": true,
  "metadata_tags": [
    { "key": "sample_id", "value": "S001", "data_type": "TEXT" }
  ],
  "copied_to_datasets": []
}
```

**DELETE `/api/files/{id}/`**

Delete file (requires justification).

**Request:**

```json
{
  "justification": "Reason for deletion (minimum 10 characters)"
}
```

**POST `/api/files/{id}/associate-metadata/`**

Set metadata tags for file (replaces existing).

**Request:**

```json
[
  { "key": "sample_id", "value": "S001", "source_type": 1 },
  { "key": "platforms", "value": ["illumina", "pacbio"], "source_type": 1 }
]
```

**Response:**

```json
{
  "file_id": 1,
  "metadata_set": [
    {
      "key": "sample_id",
      "value": "S001",
      "key_created": false,
      "value_created": false
    }
  ],
  "added": 2,
  "removed": 1,
  "kept": 0,
  "total": 2
}
```

**GET `/api/files/{id}/metadata-tags/`**

Get all metadata tags for file.

**Response:**

```json
{
  "file_id": 1,
  "metadata_tags": [
    {
      "key": "sample_id",
      "value": "S001",
      "data_type": "TEXT",
      "source_type": 1,
      "source_type_name": "Illumina",
      "is_required": true,
      "sort_order": 1
    }
  ],
  "count": 1
}
```

**POST `/api/files/{id}/set-primary/`**

Promote file to PRIMARY status.

**Additional Endpoints**

List-style actions marked "Any authenticated" still only return files the caller can see. The other actions use `FileHierarchicalPermission` (`view_file` unless noted).

| Method | Endpoint                               | Permission                         | Description                                                                                                                       |
| ------ | -------------------------------------- | ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| GET    | `/api/files/catalog_filter_options/`   | Any authenticated                  | Distinct source types and pathogens present on catalog files: `{"source_types": [...], "pathogens": [...]}`.                      |
| POST   | `/api/files/upload/`                   | File hierarchical permission       | Multipart upload. Form fields: `file`, `lab`. Returns the file detail with 201.                                                  |
| GET    | `/api/files/{id}/download-url/`        | Can view the file                  | Returns `download_url` (a `gs://` path), `file_name`, `file_size`, `file_type`.                                                   |
| POST   | `/api/files/{id}/remove-metadata/`     | `change_file`                      | Remove metadata tags from a DRAFT file. Body: `[{"key": "sample_id", "value": "S001"}]`.                                          |
| POST   | `/api/files/redact-metadata/`          | Can edit every targeted file       | Redact or un-redact cells. Body: `{"changes": [{"file_id": 12, "key": "collection_date", "redacted": true}]}`. All or nothing.     |
| POST   | `/api/files/metadata_csv/`             | Any authenticated                  | CSV of filename, status and metadata. Body `{"file_ids": [...]}`, or omit it and pass the list query params. 404 when empty.     |
| GET    | `/api/files/selection-ids/`            | Any authenticated                  | Every file matching the list filters, unpaginated, as light records: `{"count", "results"}`.                                      |
| POST   | `/api/files/bulk-delete/`              | `delete_file`                      | Hard delete a batch in Celery. Body: `{"file_ids": [...], "justification": "..."}`. Returns 202; 400 if any file fails checks.   |
| POST   | `/api/files/{id}/validate/`            | Can view the file                  | Preview metadata validation without changing state. Body: `{"acknowledged_warning_ids": [...]}` (optional).                       |
| GET    | `/api/files/{id}/validation-runs/`     | Can view the file                  | Last 100 validation runs for the file, each with its issues.                                                                      |

---

## Uploads

**Base Path:** `/api/uploads/`

**GUI Uploads**

**POST `/api/uploads/`**

Create GUI upload (returns signed URL).

**Request:**

```json
{
  "filename": "sample.fastq",
  "content_type": "application/octet-stream",
  "lab": 1,
  "time_to_live": 3600,
  "file_size": 1048576
}
```

**Response:**

```json
{
  "id": 1,
  "filename": "sample.fastq",
  "content_type": "application/octet-stream",
  "lab": 1,
  "time_to_live": 3600,
  "file_size": 1048576,
  "upload_url": "https://storage.googleapis.com/...",
  "ingest_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-01-15T10:30:00Z",
  "file": 1,
  "status": "PENDING"
}
```

**Batch Uploads**

**GET `/api/uploads/batch-uploads/`**

List batch uploads.

**Response:**

```json
[
  {
    "id": 1,
    "user": "john@example.com",
    "lab": "Genomics Lab",
    "ingest_bucket": "batch-upload-lab1-20240115-abc123",
    "kind": "FASTQ",
    "time_to_live": 86400,
    "description": "Batch upload for sequencing data",
    "created_at": "2024-01-15T10:30:00Z",
    "expires_at": "2024-01-16T10:30:00Z",
    "is_expired": false,
    "file_count": 5
  }
]
```

**POST `/api/uploads/batch-uploads/`**

Create batch upload.

**Request:**

```json
{
  "lab": 1,
  "kind": "FASTQ",
  "time_to_live": 86400,
  "description": "Batch upload for sequencing data"
}
```

**Response:**

```json
{
  "id": 1,
  "lab": 1,
  "ingest_bucket": "batch-upload-lab1-20240115-abc123",
  "kind": "FASTQ",
  "time_to_live": 86400,
  "description": "Batch upload for sequencing data"
}
```

**GET `/api/uploads/batch-uploads/{id}/download_service_account_key/`**

Download service account keyfile.

**Query Parameters:**

- `as_file` - Return as downloadable file (`true`) or JSON response

**Additional Endpoints**

| Method | Endpoint                                     | Permission                                          | Description                                                                                                                    |
| ------ | -------------------------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| GET    | `/api/uploads/{id}/upload_url/`              | Any authenticated (scoped to visible uploads)       | Signed upload URL for a GUI upload: `upload_url`, `filename`, `content_type`. Kept for compatibility; `POST /api/uploads/` already returns it. |
| POST   | `/api/uploads/batch-uploads/{id}/revoke/`    | Endpoint owner, Lab Director of the lab, Platform Admin | Close the batch upload endpoint now and queue deletion of its ingest bucket and service account keys. Cannot be undone. 400 if already revoked or files are still processing. |

---

## Datasets (Data Catalog)

**Base Path:** `/api/datasets/`

**GET `/api/datasets/`**

List searchable datasets.

**Query Parameters:**

- `type` - Filter by type (GUI, BATCH)
- `owning_project` - Filter by owning project ID
- `assigned_projects` - Filter by assigned project IDs
- `metadata_tags` - Filter by metadata tag IDs
- `metadata_tag_match_partial` - `true` for OR, `false` for AND (default)
- `search` - Search in display_name
- `pagination`, `page`, `page_size` - Pagination controls

**Response:**

```json
[
  {
    "id": 1,
    "display_name": "COVID Samples Dataset",
    "description": "Dataset description",
    "type": "GUI",
    "searchable": true,
    "owning_project": { "id": 1, "display_name": "COVID-19 Sequencing" },
    "assigned_projects": [{ "id": 2, "display_name": "Analysis Project" }],
    "file_count": 50,
    "total_file_size": 52428800,
    "metadata_tags": [
      {
        "id": 1,
        "metadata_tag": { "id": 1, "key": "organism", "value": "SARS-CoV-2" }
      }
    ]
  }
]
```

**POST `/api/datasets/`**

Create a new dataset.

**Request:**

```json
{
  "owning_project": 1,
  "display_name": "New Dataset",
  "description": "Dataset description",
  "type": "GUI",
  "searchable": true,
  "metadata_tags": [1, 2, 3]
}
```

**POST `/api/datasets/{id}/request-access/`**

Request access to dataset for a project.

**Request:**

```json
{
  "project_id": 2,
  "message": "We need access for our analysis project"
}
```

**Additional Endpoints**

Every dataset endpoint also requires Data Catalog access (Platform Admin, Data Analyst, or any lab or project membership).

| Method | Endpoint                                                 | Permission                         | Description                                                                                       |
| ------ | -------------------------------------------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------- |
| POST   | `/api/datasets/{id}/project-assignments/`                | `change_dataset`                   | Assign a project to the dataset. Body: `{"project_id": 2}`.                                       |
| GET    | `/api/datasets/{id}/download_service_account_keyfile/`   | `view_dataset`                     | Download the service account keyfile of a BATCH dataset as JSON. 400 for non-batch datasets.      |
| GET    | `/api/datasets/{id}/blade_view/`                         | Data Catalog access                | Dataset details formatted for the frontend blade view.                                            |

---

## Analytical Datasets

**Base Path:** `/api/analytical-datasets/`

**GET `/api/analytical-datasets/`**

List analytical datasets.

**Response:**

```json
[
  {
    "id": 1,
    "name": "Analysis Dataset 1",
    "date": "2024-01-15T10:30:00Z",
    "status": "PENDING",
    "gcs_bucket": "analytical-dataset-bucket",
    "project": 1,
    "lab_name": "Genomics Lab",
    "project_name": "COVID-19 Sequencing",
    "created_by": 1,
    "created_by_email": "john@example.com",
    "created_by_name": "John Doe",
    "file_count": 10
  }
]
```

**POST `/api/analytical-datasets/`**

Create analytical dataset.

**Request:**

```json
{
  "name": "New Analysis Dataset",
  "project": 1,
  "description": "Dataset for analysis"
}
```

**GET `/api/analytical-datasets/{id}/`**

Retrieve analytical dataset with files.

**Response:**

```json
{
  "id": 1,
  "name": "Analysis Dataset 1",
  "description": "Dataset description",
  "gcs_bucket": "analytical-dataset-bucket",
  "lab": 1,
  "lab_name": "Genomics Lab",
  "project": 1,
  "project_name": "COVID-19 Sequencing",
  "email": "john@example.com",
  "created_by": "John Doe",
  "created_by_name": "John Doe",
  "file_count": 10,
  "files": [
    {
      "id": 1,
      "gcs_file_path": "file.fastq",
      "file_type": "fastq",
      "file_size": 1048576,
      "status": "PRIMARY",
      "original_file_id": 5,
      "original_file_path": "lab-1/original.fastq",
      "lab_name": "Genomics Lab",
      "metadata_tags": [...]
    }
  ],
  "access_requests": [
    {
      "id": 1,
      "name": "sample.fastq",
      "lab_name": "Other Lab",
      "status": "PENDING",
      "denied_by": null,
      "denial_reason": null
    }
  ]
}
```

**POST `/api/analytical-datasets/{id}/approve/`**

Approve pending access requests (Lab Director).

**Response:**

```json
{
  "status": "approved",
  "approved_count": 3
}
```

**POST `/api/analytical-datasets/{id}/deny/`**

Deny pending access requests (Lab Director).

**Request:**

```json
{
  "denial_reason": "Data cannot be shared due to IRB restrictions"
}
```

**Response:**

```json
{
  "status": "denied",
  "denied_count": 3
}
```

**Additional Endpoints**

"Dataset access" means Platform Admin or access to the dataset's project. "Subscription writer" means Platform Admin, the dataset's creator, or a Lab Director of the dataset's lab.

| Method           | Endpoint                                                         | Permission                                                 | Description                                                                                              |
| ---------------- | ---------------------------------------------------------------- | ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| GET              | `/api/analytical-datasets/{id}/files/`                           | Dataset access                                             | Files in the dataset. Pagination and `?search=` behave like `/api/files/`.                               |
| DELETE           | `/api/analytical-datasets/{id}/files/{file_id}/`                 | Platform Admin, dataset creator, Lab Director of the lab   | Remove a file from the dataset (database record and GCS blob). Returns 204.                              |
| POST             | `/api/analytical-datasets/{id}/retry-copies/`                    | Dataset access                                             | Re-enqueue copies for approved requests that never landed: `{"enqueued_count": 2}`.                      |
| GET              | `/api/analytical-datasets/{id}/metadata_csv/`                    | Dataset access                                             | CSV of metadata for every file in the dataset.                                                           |
| GET              | `/api/analytical-datasets/{id}/build-log/`                       | Dataset access                                             | Last captured GCS bucket creation error: `{"last_build_error": ""}`.                                     |
| POST             | `/api/analytical-datasets/{id}/request-access/`                  | Dataset access                                             | Request access to files. Body: `{"files": [1, 2]}`. Returns `{"created": [...], "existing": [...]}`.     |
| POST             | `/api/analytical-datasets/{id}/request-access-by-filter/`        | Dataset access                                             | Request access to every PRIMARY file matching catalog filters. Body: `{"filters": {...}, "exclude_file_ids": [...]}`. |
| GET/POST         | `/api/analytical-datasets/{id}/subscriptions/`                   | GET: dataset access. POST: subscription writer             | List or create subscription rules that add future PRIMARY files matching metadata filters.               |
| GET/PATCH/DELETE | `/api/analytical-datasets/{id}/subscriptions/{sub_id}/`          | GET: dataset access. PATCH/DELETE: subscription writer     | Read, update, or delete one subscription.                                                                |
| POST             | `/api/analytical-datasets/{id}/subscriptions/preview/`           | Dataset access                                             | Preview matches for an unsaved rule: `match_count`, `already_in_dataset_count`, `sample_files`.          |
| POST             | `/api/analytical-datasets/{id}/subscriptions/{sub_id}/preview/`  | Dataset access                                             | Preview matches for a saved rule.                                                                        |
| POST             | `/api/analytical-datasets/{id}/subscriptions/{sub_id}/backfill/` | Subscription writer                                        | Request the files the rule matches right now. 400 if the rule is inactive or the dataset is being deleted. |

Subscription fields: `name`, `description`, `metadata_filters`, `metadata_filter_logic` (`AND` or `OR`), `source_types`, `allow_cross_lab`, `is_active`.

---

## Notifications

**Base Path:** `/api/notifications/`

**GET `/api/notifications/`**

List notifications for current user.

**Response:**

```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Access Request Approved",
      "details": "Your access request has been approved",
      "status": "info",
      "notification": "ACCESS_REQUEST_APPROVED",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

**GET `/api/notifications/preferences/`**

Get notification preferences.

**Response:**

```json
[
  {
    "notification": "ACCESS_REQUEST",
    "email_enabled": true
  }
]
```

**PUT `/api/notifications/preferences/`**

Update notification preferences (batch).

**Request:**

```json
[
  {
    "notification": "ACCESS_REQUEST",
    "email_enabled": false
  }
]
```

**Additional Endpoints**

| Method    | Endpoint                                             | Permission         | Description                                                                                           |
| --------- | ---------------------------------------------------- | ------------------ | ----------------------------------------------------------------------------------------------------- |
| PUT       | `/api/notifications/preferences/{notification}/`     | Any authenticated  | Update a single notification preference.                                                              |
| GET       | `/api/notifications/unread-count/`                   | Any authenticated  | Unread in-app notifications for the current user: `{"count": 3}`.                                     |
| POST      | `/api/notifications/mark-read/`                      | Any authenticated  | Mark notifications read. Body: `{"ids": [1, 2]}` and/or `{"all": true}`. Returns `{"marked", "count"}`. |
| GET       | `/api/notifications/action-items/`                   | Any authenticated  | Failures and flags the caller should clean up. Pass `?lab=<id>` for one lab's dashboard. Returns `{"count", "results"}`. |
| GET       | `/api/notifications/system-alerts/`                  | Any authenticated  | Active, non-expired system alerts the caller has not acknowledged.                                    |
| GET       | `/api/notifications/system-alerts/all/`              | Any authenticated  | Every system alert ever created, with `is_currently_active`.                                          |
| POST      | `/api/notifications/system-alerts/{id}/acknowledge/` | Any authenticated  | Stop showing an alert to the caller. Idempotent. Returns 204.                                         |
| GET/PATCH | `/api/notifications/reminder-settings/`              | Platform Admin     | Read or update reminder settings: `cadence_days`, `max_age_days`, `enabled_notification_types`.       |

---

## Metadata Tags

**Base Path:** `/api/metadata-tags/`

**GET `/api/metadata-tags/`**

List metadata tags.

**Query Parameters:**

- `key` - Filter by key name
- `value` - Filter by value name

**Response:**

```json
[
  {
    "id": 1,
    "key": { "id": 1, "name": "organism", "data_type": "TEXT" },
    "value": { "id": 1, "name": "SARS-CoV-2" }
  }
]
```

**Additional Endpoints**

| Method | Endpoint                                                 | Permission                                               | Description                                                                                                   |
| ------ | -------------------------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| GET    | `/api/metadata-tags/keys/`                               | Platform Admin                                           | All predefined metadata keys (lab custom keys are excluded).                                                  |
| POST   | `/api/metadata-tags/upload-values-csv/`                  | Platform Admin                                           | Bulk create values for one key. Multipart: `csv_file` (single `value` column), `key`, optional `source_type_ids`, `apply_to_core`. Returns 201, 207, or 400. |
| GET    | `/api/metadata-tags/corrections/`                        | Platform Admin                                           | Read-only audit of baseline metadata corrections. Filter with `?file=<id>`. Also `GET .../corrections/{id}/`. |
| GET    | `/api/metadata-tags/option-requests/`                    | Platform Admin (any authenticated with `?file=<id>`)     | List option requests. Filters: `status`, `file`.                                                              |
| POST   | `/api/metadata-tags/option-requests/`                    | Any authenticated                                        | Suggest a new option for a SELECT field.                                                                      |
| GET    | `/api/metadata-tags/option-requests/{id}/`               | Platform Admin                                           | Retrieve one option request.                                                                                  |
| PATCH  | `/api/metadata-tags/option-requests/{id}/`               | Sole attacher, while PENDING                             | Edit a pending request.                                                                                       |
| POST   | `/api/metadata-tags/option-requests/{id}/approve/`       | Platform Admin                                           | Approve. Body: `{"review_justification": "...", "proposed_value": "..."}` (both optional). Returns the request and `promotion_results`. |
| POST   | `/api/metadata-tags/option-requests/{id}/reject/`        | Platform Admin                                           | Reject. Body: `{"review_justification": "..."}`.                                                              |
| GET    | `/api/metadata-tags/option-request-files/`               | Any authenticated (own links only)                       | The caller's file-to-request links. Filters: `status`, `lab`. Also `GET .../{id}/`.                           |
| PATCH  | `/api/metadata-tags/option-request-files/{id}/`          | Link owner                                               | Toggle `auto_promote_on_approval` while the request is PENDING.                                               |
| POST   | `/api/metadata-tags/option-request-files/{id}/detach/`   | Link owner                                               | Drop the link. The parent request is cancelled when its last link is removed.                                 |

---

## Metadata Requirements

**Base Path:** `/api/metadata-requirements/`

**Source Types**

**GET `/api/metadata-requirements/source-types/`**

List source types.

**Response:**

```json
[
  {
    "id": 1,
    "name": "Illumina",
    "sort_order": 1
  }
]
```

**POST `/api/metadata-requirements/source-types/`**

Create source type.

**Request:**

```json
{
  "name": "Oxford Nanopore",
  "sort_order": 2
}
```

**Templates**

**GET `/api/metadata-requirements/templates/`**

List metadata templates.

**Query Parameters:**

- `source_type` - Filter by source type ID
- `is_required` - Filter by required status
- `is_core` - Filter by core status

**Response:**

```json
[
  {
    "id": 1,
    "key": { "id": 1, "name": "sample_id", "data_type": "TEXT" },
    "source_type": { "id": 1, "name": "Illumina" },
    "is_required": true,
    "is_core": true,
    "sort_order": 1,
    "template_options": [{ "id": 1, "value": { "id": 1, "name": "option1" } }]
  }
]
```

**POST `/api/metadata-requirements/templates/`**

Create template.

**Request:**

```json
{
  "key": "new_field",
  "source_type": 1,
  "is_required": false,
  "is_core": false,
  "sort_order": 10,
  "data_type": "SELECT",
  "options": ["option1", "option2"]
}
```

**GET `/api/metadata-requirements/templates/download_csv/`**

Download CSV template.

**Query Parameters:**

- `source_type` - Source type ID
- `include_info_row` - Include requirement info (`true`/`false`)

**POST `/api/metadata-requirements/templates/upload_csv/`**

Upload CSV with metadata.

**Request:**

```
Content-Type: multipart/form-data

csv_file: (CSV file)
lab: 1
source_type: 1
validate_only: false
```

**Response:**

```json
{
  "success": true,
  "success_count": 10,
  "error_count": 0,
  "processed_files": ["file1.fastq", "file2.fastq"],
  "message": "Successfully processed 10 files",
  "errors": [],
  "warnings": []
}
```

**Additional Endpoints**

Reads are open to any authenticated user. Standard create, update, and delete on source types, requirements, and templates need a Lab Director or Platform Admin.

| Method                  | Endpoint                                                   | Permission           | Description                                                                                                   |
| ----------------------- | ---------------------------------------------------------- | -------------------- | ------------------------------------------------------------------------------------------------------------- |
| GET                     | `/api/metadata-requirements/source-types/{id}/requirements/` | Any authenticated  | Requirements for this source type plus universal ones (no source type).                                       |
| GET                     | `/api/metadata-requirements/source-types/statistics/`      | Any authenticated    | Totals, top 5 source types by requirement count, source types with none, universal requirement count.         |
| GET/POST                | `/api/metadata-requirements/requirements/`                 | See note above       | List (`?simple=true` for the light serializer, `?pagination=true` to paginate) or create requirements.        |
| GET/PUT/PATCH/DELETE    | `/api/metadata-requirements/requirements/{id}/`            | See note above       | Read, update, or delete one requirement.                                                                      |
| POST                    | `/api/metadata-requirements/requirements/bulk_create/`     | Any authenticated    | Create many requirements from a JSON list. All are validated before any is saved.                             |
| DELETE                  | `/api/metadata-requirements/requirements/bulk_delete/`     | Any authenticated    | Delete requirements by id. Body: `{"ids": [1, 2]}`.                                                           |
| GET                     | `/api/metadata-requirements/requirements/universal/`       | Any authenticated    | Requirements that apply to all source types.                                                                  |
| GET                     | `/api/metadata-requirements/requirements/by_source_type/`  | Any authenticated    | Requirements grouped by source type name, plus a `universal` key.                                             |
| POST                    | `/api/metadata-requirements/requirements/{id}/duplicate/`  | Any authenticated    | Copy a requirement, optionally to another `source_type`.                                                      |
| GET                     | `/api/metadata-requirements/templates/schema/`             | Any authenticated    | Templates, their validator rules, and cross-field rules in one payload. Query: `source_type` (id or `core`), `kind` (`BASELINE` default, or `POST_ANALYSIS`). |
| GET                     | `/api/metadata-requirements/templates/download_xlsx/`      | Any authenticated    | Excel template. Query: `source_type`, `file_ids`, `all_drafts_lab` (all optional).                            |
| GET                     | `/api/metadata-requirements/templates/upload_csv_status/`  | Any authenticated (own tasks only) | Poll an `upload_csv` task. Query: `task_id`. Returns `{"state", "result"}`.                     |

---

## Domain Whitelist

**Base Path:** `/api/domain-whitelist/`

**GET `/api/domain-whitelist/`**

List whitelisted domains.

**Response:**

```json
[
  {
    "id": 1,
    "domain": "asu.edu",
    "description": "Arizona State University",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

**POST `/api/domain-whitelist/`**

Add domain to whitelist.

**Request:**

```json
{
  "domain": "example.edu",
  "description": "Example University"
}
```

---

## Deletions

**Base Path:** `/api/deletions/`

**Archive Requests**

**GET `/api/deletions/archive-requests/`**

List archive requests.

**Response:**

```json
[
  {
    "id": 1,
    "status": "PENDING",
    "justification": "Data no longer needed",
    "external_storage_location": "https://archive.example.com/file123",
    "retention_requirement_met": true,
    "requested_by": { "id": 1, "email": "john@example.com" },
    "reviewed_by": null,
    "reviewed_at": null,
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

**POST `/api/deletions/archive-requests/`**

Create archive request.

**Request:**

```json
{
  "content_type": 15,
  "object_id": 1,
  "justification": "Data no longer needed for research",
  "external_storage_location": "https://archive.example.com/file123"
}
```

**POST `/api/deletions/archive-requests/{id}/approve/`**

Approve archive request.

**POST `/api/deletions/archive-requests/{id}/deny/`**

Deny archive request.

**Request:**

```json
{
  "denial_reason": "Retention period not met"
}
```

**Additional Endpoints**

| Method | Endpoint                                              | Permission                                   | Description                                                                                                  |
| ------ | ----------------------------------------------------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| GET    | `/api/deletions/`                                     | Platform Admin, staff, Lab Director          | Deletion audit trail. Lab Directors only see File deletions for labs they direct. Query: `start_date`, `end_date`, `model_type`, `search`, `ordering`. |
| GET    | `/api/deletions/{id}/`                                | Platform Admin, staff, Lab Director          | One deletion record with full detail.                                                                        |
| GET    | `/api/deletions/archive-requests/my-requests/`        | Any authenticated                            | Archive requests the caller created, for files in active labs.                                               |
| GET    | `/api/deletions/archive-requests/pending-approvals/`  | Any authenticated (results scoped)           | Pending requests the caller can approve: all of them for platform admins, their labs' for Lab Directors.     |

---

## Pathogens

**Base Path:** `/api/pathogens/`

The pathogen registry and conditional reportability rules. Reads (`list`, `retrieve`) are open to any authenticated user; everything else needs a Platform Admin.

| Method               | Endpoint                                             | Permission         | Description                                                                                        |
| -------------------- | ---------------------------------------------------- | ------------------ | -------------------------------------------------------------------------------------------------- |
| GET/POST             | `/api/pathogens/`                                    | Read: any. Write: Platform Admin | List or create pathogens.                                                            |
| GET/PUT/PATCH/DELETE | `/api/pathogens/{id}/`                               | Read: any. Write: Platform Admin | Read, update, or delete one pathogen.                                                |
| POST                 | `/api/pathogens/upload-csv/`                         | Platform Admin     | Upsert pathogens from a CSV. Multipart: `csv_file` (max 10 MB). Returns 201, 207, or 400.          |
| GET                  | `/api/pathogens/candidates/`                         | Platform Admin     | Pathogen metadata option names not yet in the registry: `{"names": [...]}`.                        |
| GET/POST             | `/api/pathogens/reportability-rules/`                | Read: any. Write: Platform Admin | List or create rules. Filters: `pathogen`, `is_active`.                              |
| GET/PUT/PATCH/DELETE | `/api/pathogens/reportability-rules/{id}/`           | Read: any. Write: Platform Admin | Read, update, or delete one rule.                                                    |
| POST                 | `/api/pathogens/reportability-rules/preview/`        | Platform Admin     | Preview matches for an unsaved rule. Body: `metadata_filters` (at least one), `metadata_filter_logic`, optional `sample_size` (max 50). |
| POST                 | `/api/pathogens/reportability-rules/{id}/preview/`   | Platform Admin     | Preview matches for a saved rule.                                                                  |

**Pathogen fields:** `id`, `name`, `category`, `description`, `reportable`, `value` (read only), `active_reportability_rule_count` (read only).

**Rule fields:** `id`, `pathogen`, `name`, `metadata_filters`, `metadata_filter_logic`, `is_active`, `created_at`, `updated_at`.

Preview responses return `{"match_count": 12, "sample_files": [...]}`, counted over PRIMARY files the caller can see.

---

## Metadata Validations

**Base Path:** `/api/metadata-validations/`

Admin API for the validation rule engine. Reads are open to any authenticated user. Create, update, and delete need a Platform Admin or a Lab Director.

| Method               | Endpoint                                             | Description                                                                                         |
| -------------------- | ---------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| GET                  | `/api/metadata-validations/rule-types/`              | Catalog of active rule types with their param schema: `{"rule_types": [...]}`. Used by the rule editor. |
| GET/POST             | `/api/metadata-validations/rules/`                   | Field-level validator rules. Filters: `metadata_template`, `rule_type`, `severity`, `is_active`, `rule_group`. |
| GET/PUT/PATCH/DELETE | `/api/metadata-validations/rules/{id}/`              | One field-level rule.                                                                               |
| GET/POST             | `/api/metadata-validations/cross-field-rules/`       | Cross-field rules. Filters: `source_type`, `rule_type`, `severity`, `is_active`.                    |
| GET/PUT/PATCH/DELETE | `/api/metadata-validations/cross-field-rules/{id}/`  | One cross-field rule.                                                                               |
| GET                  | `/api/metadata-validations/operations/`              | Read-only list of underlying operations. Filters: `kind`, `is_active`. Also `GET .../{id}/`.        |
| GET/POST             | `/api/metadata-validations/rule-type-definitions/`   | Rule type definitions (labels, descriptions, operation). Filters: `kind`, `is_active`, `operation`, `code`. |
| GET/PUT/PATCH/DELETE | `/api/metadata-validations/rule-type-definitions/{id}/` | One rule type definition.                                                                        |
| GET/POST             | `/api/metadata-validations/rule-param-definitions/`  | Param definitions for rule types. Filters: `rule_type`, `widget_type`, `is_required`.               |
| GET/PUT/PATCH/DELETE | `/api/metadata-validations/rule-param-definitions/{id}/` | One param definition.                                                                           |

List endpoints accept `?ordering=` (for example `sort_order`, `id`).

---

## Saved Searches

**Base Path:** `/api/saved-searches/`

Saved Data Catalog and sequence filters. Any authenticated user can call these. You see your own searches and those shared with a lab you belong to. Only the creator can update or delete a search.

| Method               | Endpoint                     | Description                                                                                 |
| -------------------- | ---------------------------- | ------------------------------------------------------------------------------------------- |
| GET                  | `/api/saved-searches/`       | List visible searches. Filters: `lab`, `show_in_sequences`, `show_in_data_catalog`.         |
| POST                 | `/api/saved-searches/`       | Create a search. `created_by` is set to the caller.                                         |
| GET/PUT/PATCH/DELETE | `/api/saved-searches/{id}/`  | Read, update, or delete one search.                                                         |

**Request:**

```json
{
  "lab": 1,
  "name": "Recent SARS-CoV-2",
  "search": "",
  "metadata_filters": [],
  "metadata_filter_logic": "AND",
  "source_types": [1],
  "shared_with_lab": false,
  "show_in_sequences": true,
  "show_in_data_catalog": false
}
```

At least one of `show_in_sequences` or `show_in_data_catalog` must be true.

---

## Reporting

**Base Path:** `/api/reporting/`

| Method               | Endpoint                               | Permission                                                      | Description                                                                                         |
| -------------------- | -------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| GET                  | `/api/reporting/file-metadata/`        | Any authenticated (scoped to what you can see)                  | Tabular primary file metadata as `{schema, rows}`. Scope with one of `lab`, `project`, `dataset`; no scope means the whole catalog. |
| GET                  | `/api/reporting/catalog-overview/`     | Any authenticated (scoped to what you can see)                  | Chart data for the Catalog Overview page and lab dashboard. Query: `lab`, `source_type`.            |
| GET/POST             | `/api/reporting/reports/`              | Read: project access. Create: project access                    | Saved reports. Filter with `?project=<id>`.                                                         |
| GET/PUT/PATCH/DELETE | `/api/reporting/reports/{id}/`         | Write: creator, Lab Director of the project's lab, Platform Admin | One saved report.                                                                                 |
| GET/POST             | `/api/reporting/uploads/`              | Read: project access. Create: project access                    | Ad hoc tabular data uploaded to a project for charting. Filter with `?project=<id>`.                |
| GET/PUT/PATCH/DELETE | `/api/reporting/uploads/{id}/`         | Write: creator, Lab Director of the project's lab, Platform Admin | One upload. Detail includes `raw_tabular_data`.                                                   |
| GET/POST             | `/api/reporting/presets/`              | Read: any authenticated. Write: Platform Admin                  | Platform-wide report presets.                                                                       |
| GET/PUT/PATCH/DELETE | `/api/reporting/presets/{id}/`         | Read: any authenticated. Write: Platform Admin                  | One preset.                                                                                         |

**Saved report fields:** `project`, `reporting_upload`, `analytical_dataset`, `data_scope`, `name`, `description`, `config`. The project is fixed at creation, and a bound upload or analytical dataset must belong to the same project.

**Upload fields:** `project`, `name`, `raw_tabular_data`.

---

## Acceptable Use Policy

**Base Path:** `/api/acceptable-use/`

**GET `/api/acceptable-use/current/`**

Get the current policy and whether you have accepted it. Any authenticated user. Returns 204 when no policy is published.

**Response:**

```json
{
  "id": 3,
  "version": "2",
  "title": "Acceptable Use Policy",
  "body_html": "<p>...</p>",
  "published_at": "2026-01-01T00:00:00Z",
  "acknowledged_at": null
}
```

**POST `/api/acceptable-use/acknowledge/`**

Accept the current policy. Any authenticated user. Returns 201 on first acceptance and 200 if already accepted. Returns 409 with `"code": "aup_version_changed"` if `policy_id` is not the current version, and 404 if no policy is published.

**Request:**

```json
{
  "policy_id": 3
}
```

**Policy Gate**

`AcceptableUsePolicyMiddleware` blocks every `/api/` request from an authenticated user who has not accepted the current policy. It resolves the user from the session or any of the API's authentication classes. Blocked requests get:

```json
{
  "detail": "You must acknowledge the Acceptable Use Policy before using APGAP.",
  "code": "aup_acknowledgment_required"
}
```

with status 403. These prefixes are exempt: `/api/acceptable-use/`, `/api/users/me/`, `/api/version/`, `/api/schema/`, `/api/docs/`, `/api/auth/`, `/api/auth-token/`. Login and token refresh live outside `/api/` and are never gated. Anonymous requests pass through and get the view's usual 401. When no policy is published, nobody is blocked.

---

## Post-Analysis Publications

**Base Path:** `/api/post-analysis-publications/`

Dated sets of post-analysis metadata on a PRIMARY file. Reading needs view access to the file. Changing a set needs edit access to the file (`change_file`) and an active lab.

| Method | Endpoint                                              | Description                                                                                                     |
| ------ | ----------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| GET    | `/api/post-analysis-publications/?file=<id>`          | List a file's publications. Viewers see PUBLISHED sets; editors also see the open DRAFT. Returns `file_id`, `source_file_id`, `can_edit`, `publications`. |
| POST   | `/api/post-analysis-publications/open-draft/`         | Open or return the DRAFT for a PRIMARY original file. Body: `{"file": 12}`.                                    |
| POST   | `/api/post-analysis-publications/{id}/tags/`          | Replace the draft's tags. Body: `{"tags": [{"key": "...", "value": "...", "source_type": 1}]}`.              |
| POST   | `/api/post-analysis-publications/{id}/remove-tag/`    | Soft remove one live tag. Body: `{"metadata_tag_id": 5}` or `{"key": "...", "value": "..."}`.                  |
| POST   | `/api/post-analysis-publications/{id}/validate/`      | Preview POST_ANALYSIS validation without publishing. Body: `{"acknowledged_warning_ids": [...]}` (optional).    |
| POST   | `/api/post-analysis-publications/{id}/publish/`       | Validate and publish the draft. Returns 400 with a `code` such as `ALREADY_PUBLISHED`, `EMPTY_PUBLICATION`, `VALIDATION_ERRORS` or `UNACKNOWLEDGED_WARNINGS` when blocked. |

---

## Lab Custom Tags

**Base Path:** `/api/lab-custom-tags/`

Per-lab custom post-analysis tag definitions.

**GET `/api/lab-custom-tags/`**

List a lab's custom tags with their options. Pass `?file=<id>` (needs view access to the file) or `?lab=<id>` (needs lab access). Returns `{"lab_id": 1, "custom_tags": [...]}`.

**POST `/api/lab-custom-tags/`**

Create a custom tag. With `file`, you need edit access to that file. With only `lab`, you need to be a Platform Admin or a Lab Director or lab admin of that lab. The lab must be active. A name that matches a predefined key is rejected.

**Request:**

```json
{
  "lab": 1,
  "name": "lineage_note",
  "data_type": "SELECT",
  "is_private": false,
  "multiple_select": false,
  "options": ["a", "b"]
}
```

---

## Admin: Labs and Projects

**Base Path:** `/api/admin/labs-projects/`

Platform Admin only.

| Method | Endpoint                            | Description                                                                                                                  |
| ------ | ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| GET    | `/api/admin/labs-projects/`         | Paginated (10 per page, `page_size` up to 100) active, billing-provisioned labs with nested projects and GCP project IDs. Query: `search`, `search_field` (`all`, `lab`, `project`, `project_id`, `billing_id`, `created`). |
| GET    | `/api/admin/labs-projects/export/`  | CSV of every lab and project with GCP project and billing IDs. Ignores pagination and search.                                |

---

## Version

**GET `/api/version/`**

API version and public site configuration. No authentication required, and exempt from the policy gate.

**Response:**

```json
{
  "version": "1.0.0",
  "api": "APGAP-backend",
  "user_guide_url": "https://...",
  "upload_size_recommendations": {}
}
```

---

## Internal Webhooks

These endpoints receive Google Cloud Pub/Sub push messages. They are not for client use. They authenticate with `PubSubAuthentication` (`asu_apgap/datasets/api/authentication.py`), which verifies the OIDC bearer token's signature, audience (`API_BASE_URL`), verified email, and that the email is `PUBSUB_SERVICE_ACCOUNT`. Verification is skipped when `API_BASE_URL` is `http://localhost:8000`.

| Method | Endpoint                                                           | Purpose                                                       |
| ------ | ------------------------------------------------------------------ | ------------------------------------------------------------- |
| POST   | `/api/uploads/ingest-notifications/`                               | Batch ingest bucket object events; triggers DLP scans.        |
| POST   | `/api/uploads/dlp-completion-notifications/`                       | Cloud DLP inspect job completion.                             |
| POST   | `/api/uploads/scrubber-completion-notifications/`                  | SRA scrubber workflow completion.                             |
| POST   | `/api/datasets/{dataset_id}/ingest-notification/`                  | Batch dataset ingest bucket events.                           |
| POST   | `/api/notifications/analytical-dataset-delete-notifications/`      | Object deletions in analytical dataset buckets.               |
| POST   | `/api/notifications/lab-billing-change-notifications/`             | GCP billing account changes on lab projects.                  |

**PUT `/api/uploads/local-upload/{ingest_uuid}/`** is a local development stand-in for a GCS signed upload URL. It uses no authentication and refuses requests outside local development.

---

## API Documentation

| Method | Endpoint       | Description                |
| ------ | -------------- | -------------------------- |
| GET    | `/api/schema/` | OpenAPI schema (JSON/YAML) |
| GET    | `/api/docs/`   | Swagger UI documentation   |

---

## Common Response Codes

| Code | Description                      |
| ---- | -------------------------------- |
| 200  | Success                          |
| 201  | Created                          |
| 204  | No Content (successful delete)   |
| 207  | Multi-Status (partial success)   |
| 400  | Bad Request (validation error)   |
| 401  | Unauthorized (not authenticated) |
| 403  | Forbidden (no permission)        |
| 404  | Not Found                        |
| 500  | Internal Server Error            |

## Pagination

Many list endpoints support optional pagination:

- Add `?pagination=true` to enable pagination
- Use `?page=N` to specify page number
- Use `?page_size=N` to specify items per page (max 100)

When pagination is enabled, responses include:

```json
{
  "count": 100,
  "next": "http://api/endpoint/?pagination=true&page=2",
  "previous": null,
  "results": [...]
}
```

## Filtering and Search

Most list endpoints support:

- **Filtering:** Use query parameters matching field names (e.g., `?status=PENDING`)
- **Search:** Use `?search=term` to search across multiple fields
- **Ordering:** Use `?ordering=field` or `?ordering=-field` for descending

## Error Responses

Error responses follow this format:

```json
{
  "error": "Error message",
  "detail": "Detailed description or field-specific errors"
}
```

Field validation errors:

```json
{
  "field_name": ["Error message for this field"]
}
```
