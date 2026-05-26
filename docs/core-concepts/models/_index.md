# Models

## GCS-Backed Property Caching (`Lab`, `Project`)

Properties that read from GCS `project_id`, `vertex_notebook_uri`, `notebook_sa_email`, `seqera_output_bucket` follow a consistent cache-first pattern: return the cached DB value if present, otherwise read from GCS and cache for future requests. Two explicit lifecycle methods exist on both `Lab` and `Project`:

- `populate_terraform_cache()` called after a Cloud Build completes to warm the cache in a **single DB write**, avoiding race conditions with Django signals.
- `refresh_terraform_cache()` forces a full cache clear and re-fetch, also as a single atomic save for the same reason.

`_apply_and_save_terraform_cache` additionally normalises values on the way in: `vertex_notebook_uri` gets an `https://` prefix when missing, and `seqera_output_bucket` is stored without the `gs://` prefix (added back on read). Empty values fall back to `FAILED_TO_GET_OUTPUT` when `build_status` is `FAILURE`. All GCP-touching properties return a dummy value when GCP interactions are disabled.


---

## Name Normalisation via `clean()` + `save()` (`Key`, `Value`)

Both `Key` and `Value` enforce uppercase, trimmed, deduplicated-space names. The pattern is identical across both models: `clean()` does the normalisation and validation, `save()` calls `clean()` before persisting. This means the constraint is enforced on every save path, not just form submissions.

---

## Rename Aliasing for Lookup Stability (`Key` → `KeyAlias`)

When a `Key` is renamed, `Key.save()` inserts a `KeyAlias` row mapping the old name to the current `Key` in the same transaction. This ensures name-based lookups (`metadata_filter_eval._resolve_key`, `seed_validation_rules._resolve_template`) continue to find the key by its historical name. The alias write is idempotent duplicates are silently absorbed by the unique constraint.

`KeyAlias` also acts as a guard: its unique constraint on `name` prevents a new `Key` from being created with a name previously used by a different key, which would silently break the rename trail.

---

## Role-Based Access Scoping on User Query Methods (`User`)

Every `get_*` method on `User` follows the same three-tier access pattern: platform admins / superusers see everything in active labs; lab directors see everything within their labs; all others see only what they are directly assigned to or have created. This pattern is consistent across `get_projects()`, `get_accessible_batch_uploads()`, `get_analytical_datasets()`, `get_access_requests()`, and `get_archive_requests()`.

---

## Lazy Celery Task Import to Avoid Circular Imports (`File`)

The dynamic subscription evaluation task is imported lazily inside `_enqueue_dynamic_subscription_evaluation()` rather than at module level, specifically to avoid a circular import (the Celery task module imports `File` for type lookups). Errors during enqueue are explicitly not allowed to block a successful file promotion a missed enqueue is considered recoverable, a broken promotion is not.

---

## Hard Delete: Status-vs-DB-Delete Branching (`File`)

`hard_delete()` on an original file does not always delete the DB row. If copies of the file exist in analytical datasets, the original is marked `DELETED` in the database and its GCS blob is removed, but the row is retained so copies retain their foreign key reference. The row is only physically deleted when no copies remain. When a copy is the last active copy of an already-deleted original, the orphaned original row is cleaned up at that point.

---

## Bulk vs. Single Delete Notification Suppression (`File`)

`hard_delete()` accepts an optional `bulk_batch_id`. When present, per-file notification dispatch is suppressed the bulk task is responsible for sending one aggregated notification for the whole batch. The `bulk_batch_id` is written to the `Deletion` row's `additional_data` for auditability.


