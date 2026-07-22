# View Layer

## `get_queryset` Delegates to the User Model for Permission Filtering

Across every ViewSet that returns user-scoped data, `get_queryset` does not contain access-control logic itself: it delegates to the corresponding method on the `User` model (`get_access_requests()`, `get_analytical_datasets()`, `get_archive_requests()`). This keeps permission logic in one place and means the ViewSet automatically picks up any changes made to those model methods.

Any developer adding a new ViewSet that returns user-scoped data should follow this pattern rather than reimplementing access logic in the view.

---

## `_get_optimized_queryset` as a Dedicated N+1 Method

Rather than inlining `select_related` and `prefetch_related` calls directly in `get_queryset`, several ViewSets extract all query optimisations into a private `_get_optimized_queryset(queryset)` method. This makes it easy to see exactly what is being prefetched, and ensures optimisations are applied consistently across actions that use the same queryset.

This pattern appears on `AccessRequestViewSet`, `AnalyticalDatasetViewSet`, `FileViewSet`, and `ProjectUserViewSet`. When adding a new `SerializerMethodField` that traverses a relationship, check `_get_optimized_queryset` first and add the required prefetch there: not inside the serializer or the action method.

---

## `OptionalPageNumberPagination`: Pagination is Opt-In, Not Default

The same `OptionalPageNumberPagination` class (activated only when `?pagination=true` is present in the request) is defined independently in at least five view modules: `files-views`, `access_requests-views`, `uploads-views`, `deletions-views`, `datasets-views`, `metadata_requirements-views`, and `analytical-datasets-views`. Without the query parameter, the full list is returned unpaginated.

This is a deliberate API design choice, not a missing feature. Clients that need paginated responses must explicitly opt in. Developers adding new list endpoints should use this same pagination class rather than defaulting to DRF's standard `PageNumberPagination`, to stay consistent with the rest of the API.

---

## List vs. Retrieve Have Different Access Rules on `FileViewSet`

`FileViewSet.get_queryset` applies fundamentally different filtering depending on the action type. On list actions, files are scoped to labs where the user is an active member, with `DRAFT`/`PROCESSING` files visible only if created by the requesting user. On retrieve (detail) actions, **any authenticated user can access any file directly** with no filtering applied.

This asymmetry is intentional and must be preserved. Adding filtering logic to the retrieve path would break direct file access by ID, which is used by other parts of the system (e.g. notification links).

---

## Bulk Operations Follow Synchronous Validation + Asynchronous Execution

`FileViewSet.bulk_delete` uses a consistent two-phase approach: validate everything synchronously before enqueuing anything, then enqueue the actual work asynchronously and return a `202 Accepted`. If any file fails validation, **nothing** is enqueued and a `400` is returned. Completion and per-file failures are reported via an aggregated notification rather than in the HTTP response.

The same two-phase approach appears in `AnalyticalDatasetViewSet.bulk_copy_files`, where Phase 1 uses `bulk_create` (which does not fire `post_save` signals) to create all requests as `PENDING`, and Phase 2 individually saves auto-approvable requests so the `post_save` signal sees accurate total counts and cannot prematurely mark the dataset as `APPROVED`.

Any developer adding a new bulk operation should follow this pattern: validate all-or-nothing synchronously, execute asynchronously, and use `bulk_create` where signal suppression during batch inserts is required.

---

## Validation and Promotion Are Separate Endpoints on `FileViewSet`

File metadata validation and PRIMARY promotion are deliberately split into two endpoints:

- `POST /files/<id>/validate`: runs the full validation engine and returns errors, warnings, and the eligibility verdict **without changing any state**. Safe to call repeatedly.
- `POST /files/<id>/set-primary`: runs the same engine and promotes the file if it passes. Errors block promotion; warnings block until the client explicitly acknowledges them by submitting `acknowledged_warning_ids`.

Acknowledgement hashes are bound to the specific rule and offending values: any change to the underlying data invalidates the acknowledgement, preventing a client from acknowledging a warning and then changing the data to something worse.

---

## `get_permissions` Overridden to Give List/Retrieve Lighter Permission Requirements

Several ViewSets override `get_permissions` to apply a two-tier permission model: list and retrieve actions require only authentication, while create, update, and delete actions require hierarchical permissions. This pattern appears on `FileViewSet`, `DatasetViewSet`, and `ProjectViewSet`.

The intent is that reading data is broadly accessible to authenticated users (since `get_queryset` already scopes the data to what they can see), while writes require explicit role-based permissions on top.

---

## Serializer Selection via `get_serializer_class` Based on Action

Every ViewSet with more than one serializer shape implements `get_serializer_class` to select the appropriate serializer by action name (e.g. `list`, `retrieve`, `create`, `partial_update`). This is the standard pattern throughout the codebase: there are no ViewSets that use a single serializer for all actions on resources that have both list and detail representations.

Notably, `OrganizationViewSet` uses three distinct serializers: list, detail/retrieve, and patch. `MetadataTemplateViewSet` switches between read and write serializers. When adding a new action that needs different output shape, add a branch to `get_serializer_class` rather than overriding the serializer inline.

---

## `get_object` Overridden to Allow Archived Resources Through for Specific Actions

`ProjectViewSet.get_object` overrides the default DRF behaviour specifically for `archive` and `hard-delete` actions. By default, `get_queryset` excludes archived projects, which would prevent the archive or hard-delete action from finding its own target. The override bypasses the active-only filter for those two actions only.

This is a pattern to watch for whenever a resource has a filtered `get_queryset` and also needs write actions that target resources outside the default filter scope.

---

## Soft Delete Instead of Hard Delete on Users and Organizations

`UserViewSet.perform_destroy` does not delete the user from the database. Instead it sets `deleted_by`, appends `"(Deleted)"` to the name, disables the account, and removes lab and project associations. `OrganizationViewSet.perform_destroy` similarly sets `active=False` rather than issuing a `DELETE`.

Both are blocked from actual deletion if conditions aren't met: user deletion is gated by `UserManagementPermission`, and organization deletion is blocked at both the model level and the view level if the organization has users.

---

## Subscription Preview Scope Intentionally Ignores `allow_cross_lab`

`AnalyticalDatasetViewSet._subscription_preview_queryset` explicitly notes that `allow_cross_lab` does not affect the preview results: it only affects what would be auto-copied versus access-requested at subscription evaluation time. The preview always shows the user the full set of files that match the rule within their visibility scope, regardless of whether those files would be copied directly or would trigger an access request.

The `subscription_detail` URL pattern constrains `sub_id` to digits (`\d+`) specifically to prevent the literal string `"preview"` from being matched by this route: DRF evaluates patterns in declaration order and a looser pattern would consume the `preview` path before the dedicated action could handle it.

---

## `build_log` Endpoints Return Empty String, Not an Error, When No Log Exists

`LabViewSet.build_log`, `ProjectViewSet.build_log`, and `AnalyticalDatasetViewSet.build_log` all follow the same contract: return the most recent captured GCP/Cloud Build provisioning error as a string, and return an **empty string** (not a 404 or null) when no error has been recorded. This allows the UI to reliably render a "no error" state without null-checking.

---

## `local_upload_handler` Exists Solely for Local Development

`uploads-views.py` contains a `local_upload_handler` endpoint decorated with `@permission_classes([AllowAny])` that emulates a GCS signed URL PUT upload. It is explicitly documented as a local development tool to allow frontend testing without real GCP infrastructure, and carries `AllowAny` permissions.

This endpoint must never be reachable in production. Any environment configuration review should confirm it is gated behind a dev-only URL configuration.

