
# domain_whitelist backend app

A small Django/DRF app providing CRUD endpoints for whitelisted domains,
mirroring your `metadata-tags` pattern.

## Install

1) Add to `INSTALLED_APPS`:

```py
INSTALLED_APPS = [
    # ...
    "django_filters",
    "rest_framework",
    "domain_whitelist",
]
```

2) Include URLs in your API urls (e.g., `config/urls.py`):

```py
from django.urls import path, include

urlpatterns = [
    # ...
    path("api/", include("domain_whitelist.urls")),
]
```

3) Run migrations:

```bash
python manage.py makemigrations domain_whitelist
python manage.py migrate
```

## Endpoints (via DRF router)
- `GET    /api/domain-whitelist/`          list
- `POST   /api/domain-whitelist/`          create
- `GET    /api/domain-whitelist/{id}/`     retrieve
- `PATCH  /api/domain-whitelist/{id}/`     partial update
- `PUT    /api/domain-whitelist/{id}/`     update
- `DELETE /api/domain-whitelist/{id}/`     destroy

### Filtering / Search / Ordering
- Filtering: `?domain=asu&description=lab`
- Search:    `?search=example`
- Ordering:  `?ordering=domain` or `?ordering=-created_at`
