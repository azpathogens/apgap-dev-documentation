---
title: Backend Setup
---

# Backend 


Follow these steps in order to get local development up and running:

1. **Set up environment files** (see [Environment Secrets](#environment-secrets) below)
2. **Set up service account keyfile** (see [Service Account Keyfile](#service-account-keyfile) below)
3. **Build containers**: `docker compose -f docker-compose.local.yml build`
4. **Start containers**: `docker compose -f docker-compose.local.yml up`
5. **Run migrations**: `docker compose -f docker-compose.local.yml run django python manage.py migrate`
6. **Add your email domain to the whitelist** (see [Domain Whitelist Setup](#domain-whitelist-setup) below) - **Required before creating any users**
7. **Create a superuser**: `docker compose -f docker-compose.local.yml run django python manage.py createsuperuser`
8. *(Optional)* **Populate sample data**: `docker compose -f docker-compose.local.yml run django python manage.py populate_dummy_data --count 5` - fills the empty database so the UI has something to show (see [Sample Data](/core-concepts/backend/deployment#sample-data))
9. Access the application at **http://localhost:8000**

## Local Development Environment

### Prerequisites

- Python 3.12
- Docker and Docker Compose
- Git
- Pre-commit


### Environment Secrets

The application requires several secret environment variables to function properly. These should be stored in:

```
.envs/.local/.secrets
```

Secret values can be found in the Secret Manager for the application deployment. Required values for local development include:

- `GOOGLE_OAUTH_CLIENT_ID`
- `GOOGLE_OAUTH_CLIENT_SECRET`
- `GOOGLE_OAUTH_REDIRECT_URL` - **Must be set to `postmessage` for local development** (see note below)
- `SENDGRID_API_KEY`
- `SEQERA_API_TOKEN`
- `SEQERA_ORGANIZATION_ID`

**Important:** The `GOOGLE_OAUTH_REDIRECT_URL` must be set to `postmessage` when running locally with a frontend that uses Google OAuth's popup-based authentication flow. This tells Google's OAuth to return the authorization code via JavaScript `postMessage` instead of redirecting to a URL.

Example `.envs/.local/.secrets` file:

```bash
GOOGLE_OAUTH_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
GOOGLE_OAUTH_REDIRECT_URL=postmessage
SENDGRID_API_KEY=your-sendgrid-key
SEQERA_API_TOKEN=your-seqera-token
SEQERA_ORGANIZATION_ID=your-seqera-org-id
```

Never commit these secrets to the repository. The `.envs/.local/.secrets` file is included in `.gitignore`.

Non-sensitive environment variables for local development are located in:

```
.envs/.local/
```

### Service Account Keyfile

The application uses a service account to interact with Google Cloud Services:

- Service account: `dev-app-backend@asu-ap-gap-test-2360.iam.gserviceaccount.com`
- This account is permissioned to interact with GCS and run Module deployments on project creation
- The keyfile should be placed at: `secrets/keyfile_DEV.json`
- This file is also included in `.gitignore` and should never be committed to the repository

### Domain Whitelist Setup

The application validates user email addresses against a whitelist of approved domains. **All users, including superusers, must have an email domain in the whitelist before they can be created.** You must add at least one domain to the whitelist before creating any users.

#### Option 1: Via Django Shell (Recommended for Initial Setup)

Since you need to whitelist a domain before creating a superuser, use the Django shell for initial setup:

```bash
docker compose -f docker-compose.local.yml run django python manage.py shell_plus
```

Then in the shell:

```python
from asu_apgap.domain_whitelist.models import DomainWhitelist

# Add your email domain (replace with your actual domain)
DomainWhitelist.objects.create(domain="asu.edu", description="Arizona State University")

# Or add multiple domains
domains_to_add = [
    ("asu.edu", "Arizona State University"),
    ("azdhs.gov", "Arizona Department of Health Services"),
    ("tgen.org", "Translational Genomics Research Institute"),
    ("gmail.com", "Gmail (for testing)"),
]
for domain, description in domains_to_add:
    DomainWhitelist.objects.get_or_create(domain=domain, defaults={"description": description})
```

Exit the shell with `exit()`, then proceed to create your superuser.

#### Option 2: Via Django Admin (After Superuser Exists)

Once you have a superuser:

1. Access the admin interface at **http://localhost:8000/admin**
2. Log in with your superuser credentials
3. Navigate to **Domain Whitelist** in the sidebar
4. Click **Add Domain Whitelist**
5. Enter the domain (e.g., `asu.edu`, `gmail.com`, `example.com`)
6. Optionally add a description
7. Click **Save**

#### Option 3: Via API (Requires Authentication)

```bash
curl -X POST http://localhost:8000/api/domain-whitelist/ \
  -H "Authorization: Bearer your-access-token" \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.edu", "description": "Example University"}'
```

### Local Services

`docker compose -f docker-compose.local.yml up` starts five containers. All Django based containers share the same image and the env files in `.envs/.local/`.

| Service         | Container                       | Port   | Command                                                                                             |
| --------------- | ------------------------------- | ------ | --------------------------------------------------------------------------------------------------- |
| `django`        | `asu_apgap_local_django`        | `8000` | `/start`: runs migrations and seed commands, then `runserver_plus`                                  |
| `celery_worker` | `asu_apgap_local_celery_worker` |        | `/start-celeryworker`: one worker consuming both the `celery` and `ingest` queues                   |
| `celery_beat`   | `asu_apgap_local_celery_beat`   |        | `/start-celerybeat`: beat with the `django_celery_beat` database scheduler                          |
| `postgres`      | `asu_apgap_local_postgres`      |        | PostgreSQL, data kept in the `asu_apgap_local_postgres_data` volume                                 |
| `redis`         | `asu_apgap_local_redis`         | `6379` | Redis 7.2, used as the Celery broker and result backend and for distributed locks                  |

On every start, `/start` runs these commands before the server comes up, so you do not need to run them by hand:

```bash
python manage.py migrate
python manage.py ensure_adhs_organization
python manage.py setup_permission_groups
python manage.py seed_metadata_templates
python manage.py seed_pathogens
python manage.py seed_validation_rules
```

The source tree is mounted into each container, so code changes reload `django` automatically. The Celery containers do not reload: restart them after changing a task.

```bash
docker compose -f docker-compose.local.yml restart celery_worker celery_beat
```

### Running Tests

Tests use pytest with the `config.settings.test` settings module:

```bash
docker compose -f docker-compose.local.yml run --rm django pytest
```

Run a single file or test by passing its path:

```bash
docker compose -f docker-compose.local.yml run --rm django pytest asu_apgap/labs/tests/test_views.py
docker compose -f docker-compose.local.yml run --rm django pytest asu_apgap/labs/tests/test_views.py -k test_name
```

The test database is kept between runs (`--reuse-db`). After adding or changing migrations, or after rebuilding the image, recreate it once:

```bash
docker compose -f docker-compose.local.yml run --rm django pytest --create-db
```

CI runs the same suite on every pull request and push to `development`, `uat`, and `main` (see [Development Workflow](/quick-start/development_workflow/)).

### Linting

Linting runs through pre-commit hooks: ruff (lint and format), django-upgrade, djLint for templates, and the standard pre-commit checks (trailing whitespace, YAML/JSON/TOML syntax, private keys). Install the hooks once so they run on every commit:

```bash
pre-commit install
```

Run them against the whole repository, the same way CI does:

```bash
pre-commit run --all-files
```
