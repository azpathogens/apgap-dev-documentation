# Manager Layer

## QuerySet + Manager Mirroring

Every custom manager in the codebase follows the same structural pattern: a `QuerySet` class defines the filtering methods, and a `Manager` class mirrors each of those methods by delegating directly to the `QuerySet`. This exists specifically to support method chaining: since Django managers don't chain by default, the QuerySet holds the real logic and the manager is purely a pass-through entry point.

This pattern appears across `Lab`, `File`, `ArchiveRequest`, and `AnalyticalDataset`. When adding a new filtering method, it must be added to **both** the QuerySet and the Manager, or it will not be available as a starting point on `Model.objects.<method>()`.


---

## `active_lab` / `in_active_labs` as a Standard Queryset Scope

Scoping to active labs is a first-class queryset method across every manager that touches lab-owned data. The method name varies slightly by context: `active_lab()` on `FileQuerySet`, `in_active_lab()` on `ProjectQuerySet`, `in_active_labs()` on `ArchiveRequestQuerySet` and `AnalyticalDatasetQuerySet`: but the intent is identical: exclude anything belonging to an inactive lab.

These methods are designed to be chainable in either order:

```python
File.objects.active_lab().for_user(user)
File.objects.for_user(user).active_lab()
```

Any new queryset that surfaces data owned by a lab should include this scope or explicitly document why it doesn't apply.


---

## `for_user` Visibility Rules: Consistent Three-Tier Access

Every `for_user()` method across `LabQuerySet`, `FileQuerySet`, and `ProjectModelManager` enforces the same access hierarchy:

1. **Platform Admins / global permission holders**: see everything (scoped to active labs).
2. **Lab members with appropriate permissions** (directors, readers): see all resources within their labs.
3. **Project members / direct assignees**: see only resources they are explicitly assigned to.

`ProjectModelManager.for_user()` adds a fourth concern: it deduplicates the resulting list, since a user could qualify through multiple paths (lab membership and direct project assignment simultaneously).

Developers adding new resource types that need user-scoped visibility should follow this same three-tier structure rather than inventing a new access model.

---

## Status-Based QuerySet Methods on `ArchiveRequestQuerySet`

`ArchiveRequestQuerySet` exposes `pending()`, `approved()`, and `denied()` as first-class chainable methods rather than requiring callers to filter by status string directly. This keeps status string literals out of call sites and makes it easier to change status values in one place.

The same pattern should be followed for any model that has a status field with a meaningful workflow: expose named QuerySet methods rather than expecting callers to know the status values.

---

## Lazy Import to Avoid Circular Imports in Managers (`ProjectModelManager`)

`ProjectModelManager.active()` and `ProjectModelManager.archived()` import `ProjectStatus` inside the method body rather than at the top of the file. This is because `models.py` imports `ProjectModelManager`, and `ProjectStatus` is also defined in `models.py`: a top-level import would create a circular dependency.

This is the same lazy import pattern seen in the model layer (`File._enqueue_dynamic_subscription_evaluation`). When a manager needs to reference a model-layer constant or class, import it inside the method.

---

## `inapp_recipients` Pre-Filtered at Write Time (`NotificationManager`)

`NotificationManager.for_user()` performs no additional filtering on notification type or preference when returning in-app notifications: it queries only by user against the `inapp_recipients` field. This is because `inapp_recipients` is already populated at notification creation time with only users who have in-app notifications enabled for that type. The filtering happens at write time, not read time.

Developers sending notifications must ensure `inapp_recipients` is correctly scoped at creation: adding a user to `inapp_recipients` without checking their preference will cause them to receive notifications they have opted out of.

