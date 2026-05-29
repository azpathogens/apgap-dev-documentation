# Filter Layer

## Shared Metadata Filter Evaluator (`files-metadata_filter_eval`)

The metadata filter logic lives in a single shared module (`files/api/metadata_filter_eval.py`) rather than on `FileFilter` itself. `FileFilter` (the HTTP data-catalog endpoint) and the dynamic-dataset subscription evaluator (`evaluate_dynamic_subscriptions` Celery task) both consume it, and keeping the implementation centralised ensures the two callers cannot drift apart 

Any developer adding or changing filter behaviour for metadata tags must do so in this module, not in `FileFilter` directly, or the subscription evaluator will silently diverge.

---

## Key Resolution: `key_id` First, Display Name as Fallback

Across the filter layer, resolving a filter condition to a `Key` row follows a consistent preference order:

1. `condition["key_id"]`: the FK-stable integer dual-written by the saved-search and subscription serializers. Renames cannot break this path.
2. `condition["key"]`: the legacy display-name string, looked up against `Key.name`. If the key has since been renamed, the `KeyAlias` table provides a fallback through the historical name.

When neither path resolves, the condition returns an empty match (`Q(pk__in=[])`) rather than raising an error, preserving the existing "unknown key matches nothing" semantics. This means a saved filter with an unresolvable key silently matches nothing.

---

## Legacy vs. Forward Condition Shape: Both Must Be Accepted

Filter conditions support two valid key-identification shapes and both must continue to be accepted:

- **Legacy:** `{"key": "<name>", ...}`: name-based, used by older clients and unmigrated saved rows.
- **Forward:** `{"key": "<name>", "key_id": <int>, ...}`: what the dual-write serializer produces. `key_id` alone (no `key` string) is also accepted.

Dropping support for the legacy shape would silently break any saved searches or subscription rules written before the dual-write was introduced.

---

## `inject_key_ids`: Idempotent Dual-Write at Save Time

`inject_key_ids()` is the function that performs the dual-write of `key_id` alongside `key` at serializer save time. It is consumed by both `SavedSearchCreateUpdateSerializer` and `DatasetSubscriptionSerializer`. Key properties:

- It operates on a shallow copy of each condition dict: the input is not mutated.
- It is idempotent: a condition that already carries a valid `key_id` is not overwritten unless that ID no longer resolves, in which case a fresh resolution by name is attempted.
- Conditions that cannot be resolved are passed through unchanged, preserving the original `key` string for human auditability.

---

## Unknown Keys Are Tolerated at Validation Time

`validate_metadata_filters_payload()` performs pre-flight structural validation (bad shape, unknown operator for a key's data type) without executing a query. Crucially, unknown keys are explicitly tolerated here: a renamed or missing key should not block saving the rule, it should just match nothing at runtime.

This means validation will not catch a typo in a key name. Developers should not rely on this function to confirm that a key exists.

---

## `filter_queryset` Override for Default Exclusion Logic (`ProjectFilter`, `AnalyticalDatasetFilter`)

Both `ProjectFilter` and `AnalyticalDatasetFilter` override `filter_queryset()` to apply default behaviour that cannot be expressed as a simple field filter.

`ProjectFilter` uses the override to exclude archived projects by default unless `include_archived=True` or `status=ARCHIVED` is explicitly provided. The default exclusion is handled here rather than in the individual field method, because field methods are only called when their parameter is present in the request.

`AnalyticalDatasetFilter` uses the override to handle the `lab` parameter even when it is sent with an empty value. If `lab=` is present in the request but empty, the filter returns an empty queryset (not all datasets). If `lab` is absent entirely, the queryset is returned unchanged. This distinction: empty string vs. absent: cannot be handled by a standard django-filters field.

---

## Multi-Value Filter Pattern (Repeated Parameters or Comma-Separated)

Several filters support multiple values for the same field via either repeated query parameters (`?lab=1&lab=2`) or comma-separated values (`?lab=1,2`). This pattern appears in `UploadFilter`, `BatchUploadFilter`, and `AnalyticalDatasetFilter`. The parsing is handled in dedicated private methods (`_parse_lab_ids`, `filter_by_lab_names`, `filter_by_user_emails`) rather than relying on django-filters' built-in multi-value support.


---

## Privileged vs. Non-Privileged File Visibility (`FileFilter`)

`FileFilter.filter_by_created_by()` applies different filtering rules depending on whether the requesting user is privileged. A user is privileged if they are a superuser, platform admin, or lab director for the relevant lab.

- **Non-privileged users:** Files are scoped to labs where the user is an active member. All `PRIMARY` files in those labs are visible. `DRAFT` and `PROCESSING` files are only visible if created by that user. All other statuses are excluded.
- **Privileged users:** No filtering by `created_by` or lab membership: all files are shown.

This filter only applies on list actions. On retrieve (detail) actions, any authenticated user can access any file directly.

---

## `Exists` + `OuterRef` Preferred Over `filter().distinct()` for Annotation-Safe Filtering

`AnalyticalDatasetFilter.filter_has_pending_access_requests()` uses `Exists` with `OuterRef` rather than `.filter(access_requests__status=...).distinct()`. The reason is documented explicitly: the `distinct()` approach forces a JOIN duplication that interacts badly with the `Prefetch` objects set up by `_get_optimized_queryset`, and can return duplicate rows. `Exists` composes cleanly with prefetches and guarantees each dataset appears exactly once.

This is the preferred pattern for any filter that checks for the existence of a related object on a queryset that uses `Prefetch`.

