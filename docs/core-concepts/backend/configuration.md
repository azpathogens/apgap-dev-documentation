# Configuration

All backend configuration is read from environment variables in `config/settings/`. `base.py` holds the shared settings, and `local.py`, `test.py`, and `production.py` override them per environment. Variables are read with `django-environ`, so booleans accept `True`/`False` and lists are comma separated.

### Environment Files

Local development loads three files from `.envs/.local/`, listed under `env_file` for every service in `docker-compose.local.yml`:

| File        | Tracked in git | Contents                                                                                           |
| ----------- | -------------- | -------------------------------------------------------------------------------------------------- |
| `.django`   | Yes            | Non secret settings: Redis URLs, GCP project and bucket names, Cloud Build trigger IDs, API URL     |
| `.postgres` | Yes            | `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`               |
| `.secrets`  | No             | OAuth client, SendGrid key, Seqera token (see [Environment Secrets](/quick-start/backend/#environment-secrets)) |

`DATABASE_URL` is not set in any file. The container entrypoint builds it from the `POSTGRES_*` variables, which is why one off commands must use `docker compose run` rather than `exec`.

**Important:** A few settings have no default, so Django fails to start if they are missing: `PROJECT_DEPLOYMENT_STATE_BUCKET`, `DATAOPS_PROJECT_ID`, `SENDGRID_API_KEY`, and `SENDGRID_FROM_EMAIL`. Production also requires `DJANGO_SECRET_KEY` and `DJANGO_GCP_STORAGE_BUCKET_NAME`.

### Feature Flags

These flags switch external side effects on or off. Check them first when something works in one environment and not another.

| Variable                       | Default | Effect                                                                                                                         |
| ------------------------------ | ------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `ENABLE_GCP_INTERACTIONS`      | `False` | Allows labs and projects to read GCP resource details (project IDs, buckets) from GCS state and call GCP APIs                  |
| `ENABLE_CLOUD_BUILD_TRIGGER`   | `False` | Allows lab signals and lab lifecycle actions (archive, delete) to submit Cloud Build triggers                                  |
| `ENABLE_NOTEBOOK_VIEWER_SYNC`  | `False` | Syncs service account IAM for Vertex AI Workbench notebook access. Also requires `ENABLE_GCP_INTERACTIONS`                     |
| `ENABLE_EMAIL_NOTIFICATIONS`   | `False` | Sends notification emails through SendGrid. In-app notifications are created either way                                     |
| `ENABLE_DLP_SCAN`              | `True`  | Runs the GCP DLP PII scan on uploaded files                                                                                    |
| `ENABLE_SRA_SCRUBBER_WORKFLOW` | `True`  | Runs the SRA human scrubber workflow on FASTQ files after a clean DLP scan                                                     |
| `INGEST_EVENT_DRIVEN_DLP`      | `False` | Relies on the DLP completion webhook instead of the polling task                                                               |
| `INGEST_EVENT_DRIVEN_SCRUBBER` | `False` | Relies on the scrubber completion webhook instead of the polling task                                                          |
| `ENFORCE_METADATA_VALIDATION`  | `True`  | Runs the metadata validation engine when files are promoted to primary. When `False`, only presence checks run                 |

The test settings (`config/settings/test.py`) force `ENABLE_GCP_INTERACTIONS`, `ENABLE_CLOUD_BUILD_TRIGGER`, and `ENABLE_NOTEBOOK_VIEWER_SYNC` to `False`.

**Important:** `ENABLE_EMAIL_NOTIFICATIONS` is set in `.envs/.local/.django`. Emails sent locally go to the real addresses of the users in your database.

### Core Settings

| Variable                            | Default                                | Purpose                                                                 |
| ----------------------------------- | -------------------------------------- | ----------------------------------------------------------------------- |
| `DJANGO_DEBUG`                      | `False`                                | Django debug mode. `local.py` turns it on                               |
| `DATABASE_URL`                      | none                                   | Built by the entrypoint from `POSTGRES_*`                               |
| `REDIS_URL`                         | `redis://redis:6379/0`                 | Redis client used for distributed locks and debouncing                  |
| `CELERY_BROKER_URL`                 | `redis://localhost:6379/0`             | Celery broker and result backend                                        |
| `CELERY_VISIBILITY_TIMEOUT`         | `3600`                                 | Seconds before an unacknowledged task is redelivered                    |
| `API_BASE_URL`                      | `http://localhost:8000`                | Public URL of this backend, used as the Pub/Sub push endpoint and OIDC audience |
| `FRONTEND_URL`                      | `http://localhost:4200`                | Frontend origin, used for notification links and resumable upload CORS |
| `FRONTEND_URL_REDIRECT`             | `http://localhost:4200/callback/`      | Where the browser lands after login                                     |
| `FRONTEND_URL_REDIRECT_ERROR`       | `http://localhost:4200/`               | Where the browser lands after a failed login                            |
| `GOOGLE_OAUTH_CLIENT_ID`            | empty                                  | Google OAuth client, must match the frontend                            |
| `GOOGLE_OAUTH_CLIENT_SECRET`        | empty                                  | Google OAuth secret                                                     |
| `GOOGLE_OAUTH_REDIRECT_URL`         | empty                                  | `postmessage` for the popup login flow                                  |
| `USER_GUIDE_URL`                    | `https://docs.azpathogens.org/`        | Link to the end user guide shown in the app                             |
| `DATA_GOVERNANCE_GROUP`             | empty                                  | Email notified when an organization's default approval setting changes |
| `SEQUENCE_RETENTION_YEARS`          | `5`                                    | Years a sequence must be kept before it can be archived without an external location |

### Google Cloud

| Variable                                    | Default                          | Purpose                                                                    |
| ------------------------------------------- | -------------------------------- | -------------------------------------------------------------------------- |
| `GOOGLE_APPLICATION_CREDENTIALS`            | none                             | Path to the service account keyfile (`/app/secrets/keyfile_DEV.json` locally) |
| `HOST_GCP_PROJECT_ID`                       | empty                            | Host project for DLP jobs, the URL signer secret, and the scrubber workflow |
| `DATAOPS_PROJECT_ID`                        | required                         | Project that owns the ingest buckets and Pub/Sub topics                    |
| `PROJECT_DEPLOYMENT_STATE_BUCKET`           | required                         | Bucket holding Terraform state that labs and projects read resource details from |
| `DATAOPS_RAW_GUI_INGEST_GCS_BUCKET`         | `dataops-raw-ingest`             | Landing bucket for GUI uploads                                             |
| `DATAOPS_RAW_GUI_INGEST_TOPIC_NAME`         | `raw-gui-ingest-notification`    | Pub/Sub topic for GUI upload events                                        |
| `ANALYTICAL_DATASET_DELETE_TOPIC_NAME`      | `analytical-dataset-delete-notification` | Pub/Sub topic for analytical dataset bucket deletes                |
| `PUBSUB_SERVICE_ACCOUNT`                    | empty                            | Service account expected in the OIDC token of Pub/Sub push requests        |
| `URL_SIGNER_SECRET_NAME`                    | `url_signer_sa_key`              | Secret Manager secret holding the key used to sign upload URLs              |
| `CLOUD_BUILD_GCP_PROJECT_ID`                | empty                            | Project where Cloud Build triggers live                                    |
| `CLOUD_BUILD_GCP_LOCATION`                  | empty                            | Region of the Cloud Build triggers                                         |
| `CLOUD_BUILD_GCP_*_TRIGGER_ID`              | empty                            | Trigger IDs for lab and project create, destroy, and billing apply builds  |
| `LAB_BILLING_ACCOUNT_ID`                    | empty                            | Billing account for new lab projects when the lab does not set one         |
| `VERTEX_NOTEBOOK_INSTANCE_NAME`             | `vertex-workbench`               | Workbench instance name, must match the Terraform module                   |
| `VERTEX_NOTEBOOK_ZONE`                      | `us-central1-a`                  | Workbench instance zone                                                    |
| `NOTEBOOK_VIEWER_IAM_ROLE`                  | `roles/iam.serviceAccountUser`   | Role granted for notebook access                                           |

### Upload Ingest

These settings control the DLP scan and SRA scrubber stages. See [Ingest Pipeline](/workflows/ingest-pipeline/) for how the stages fit together.

| Variable                              | Default       | Purpose                                                                         |
| ------------------------------------- | ------------- | ------------------------------------------------------------------------------- |
| `DLP_POLL_MAX_RETRIES`                | `120`         | DLP poll attempts                                                               |
| `DLP_POLL_INTERVAL`                   | `60`          | Seconds between DLP polls                                                       |
| `DLP_POLL_LOCK_EXPIRE`                | `65`          | Poll lock TTL in seconds, must exceed the poll interval                         |
| `DLP_JOB_CREATION_RATE_LIMIT`         | `5/s`         | Per worker rate limit for creating DLP jobs                                     |
| `SRA_SCRUBBER_WORKFLOW_ID`            | empty         | Cloud Workflows ID of the scrubber                                              |
| `SRA_SCRUBBER_WORKFLOW_OUTPUT_BUCKET` | empty         | Bucket the scrubber writes cleaned files to                                     |
| `SRA_SCRUBBER_WORKFLOW_LOCATION`      | `us-central1` | Workflow region                                                                 |
| `SRA_SCRUBBER_WORKFLOW_PROJECT_ID`    | empty         | Workflow project, falls back to `HOST_GCP_PROJECT_ID`                           |
| `SRA_SCRUBBER_POLL_MAX_RETRIES`       | `120`         | Scrubber poll attempts                                                          |
| `SRA_SCRUBBER_POLL_INTERVAL`          | `60`          | Seconds between scrubber polls                                                  |
| `SRA_SCRUBBER_POLL_MINUTES_BASE`      | `120`         | Base scrubber time budget per file, in minutes                                  |
| `SRA_SCRUBBER_POLL_MINUTES_PER_GB`    | `3.0`         | Extra minutes per decompressed GB                                               |
| `SRA_SCRUBBER_POLL_MINUTES_MAX`       | `480`         | Upper limit of the scrubber budget                                              |
| `DLP_COMPLETE_TOPIC`                  | empty         | Topic the DLP job publishes to when done. Empty means no completion event       |
| `SRA_SCRUBBER_COMPLETE_TOPIC`         | empty         | Topic the scrubber publishes to when done. Empty means no completion event      |
| `PROCESSING_DEADLINE_BUFFER_MINUTES`  | `60`          | Buffer added to a file's `processing_deadline`                                  |
| `STUCK_FILE_CLEANUP_HOURS`            | `3`           | Fallback age for failing `PROCESSING` files that have no deadline               |

### Notifications

| Variable                                    | Default | Purpose                                                              |
| ------------------------------------------- | ------- | -------------------------------------------------------------------- |
| `SENDGRID_API_KEY`                          | required | SendGrid API key                                                    |
| `SENDGRID_FROM_EMAIL`                       | required | Sender address for notification emails                              |
| `FILE_UPLOAD_NOTIFICATION_DEBOUNCE_SECONDS` | `60`    | Window for grouping upload events into one notification per uploader and lab |
| `FILE_FAILED_NOTIFICATION_DEBOUNCE_SECONDS` | `300`   | Window for grouping processing failures into one notification       |

### Integrations

| Variable                 | Default | Purpose                                                                                  |
| ------------------------ | ------- | ---------------------------------------------------------------------------------------- |
| `SEQERA_API_TOKEN`       | empty   | Seqera Platform access token (see [Seqera Integration](/core-concepts/backend/integrations/seqera/)) |
| `SEQERA_ORGANIZATION_ID` | empty   | Seqera organization that project workspaces are created in                               |

### Production Only

`config/settings/production.py` reads these in addition to the settings above:

| Variable                         | Default         | Purpose                                         |
| -------------------------------- | --------------- | ----------------------------------------------- |
| `DJANGO_SECRET_KEY`              | required        | Django secret key                               |
| `DJANGO_ALLOWED_HOSTS`           | `example.com`   | Hostnames Django will serve                     |
| `DJANGO_GCP_STORAGE_BUCKET_NAME` | required        | Bucket for static and media files               |
| `DJANGO_ADMIN_URL`               | `admin/`        | Path of the Django admin                        |
| `DJANGO_SECURE_SSL_REDIRECT`     | `False`         | Redirect HTTP to HTTPS inside Django            |
| `SENDGRID_API_URL`               | `https://api.sendgrid.com/v3/` | SendGrid API endpoint            |

In deployed environments these values come from the Helm values files and from secrets pulled out of Secret Manager during the Cloud Build deploy (see [Deployment](/core-concepts/backend/deployment/)).
