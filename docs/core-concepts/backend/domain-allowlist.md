
# Domain Allowlist

A small Django/DRF app providing CRUD endpoints for allowed domains,
mirroring your `metadata-tags` pattern.

In APGAP this app is used to restrict from what domains email addresses for new accounts are being accepted.

## Install

1) Add to `INSTALLED_APPS`:

```py
INSTALLED_APPS = [
    # ...
    "django_filters",
    "rest_framework",
    "domain_allowlist",
]
```

2) Include URLs in your API urls (e.g., `config/urls.py`):

```py
from django.urls import path, include

urlpatterns = [
    # ...
    path("api/", include("domain_allowlist.urls")),
]
```

3) Run migrations:

```bash
python manage.py makemigrations domain_allowlist
python manage.py migrate
```

## Endpoints (via DRF router)
- `GET    /api/domain-allowlist/`          list
- `POST   /api/domain-allowlist/`          create
- `GET    /api/domain-allowlist/{id}/`     retrieve
- `PATCH  /api/domain-allowlist/{id}/`     partial update
- `PUT    /api/domain-allowlist/{id}/`     update
- `DELETE /api/domain-allowlist/{id}/`     destroy

### Filtering / Search / Ordering
- Filtering: `?domain=asu&description=lab`
- Search:    `?search=example`
- Ordering:  `?ordering=domain` or `?ordering=-created_at`
