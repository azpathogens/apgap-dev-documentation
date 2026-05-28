# Service Layer

## Business Logic Lives in the Service Layer, Not in Views or Signals

The service layer exists explicitly to keep business logic out of views and signals. `ProjectArchiveService.process_archiving_behavior` is called by the `post_save` signal handler (`handle_project_archived`) rather than the signal containing the logic itself, and `ProjectDeletionService.hard_delete_project` is called by the view's `hard_delete` action rather than the view containing the deletion steps.

This separation means the same operations can be triggered from the API, Django admin, or management commands without duplicating logic. Any multi-step operation with side effects (GCP calls, dataset deletions, audit records) should live in a service class, not inline in a view or signal.

---

## Idempotency as a Requirement for Service Methods Driven by Signals

`ProjectArchiveService.process_archiving_behavior` is explicitly documented as idempotent. This is a direct consequence of being called from a `post_save` signal: `post_save` fires on every save, not only the first time the archived state is set. The method must be safe to call multiple times without producing duplicate side effects (double-deleting datasets, double-triggering GCP cleanup, etc.).

Any service method that is invoked from a signal, a retry-able Celery task, or any other context where it may fire more than once must be designed for idempotency.

---

## `transaction.atomic` on Write-Path Service Methods

Both `ProjectArchiveService.archive_project` and `ProjectDeletionService.hard_delete_project` are decorated with `@transaction.atomic`. This ensures that if any step within the method fails, the entire operation is rolled back: the project is not left in a partially-archived or partially-deleted state in the database.

Note that `process_archiving_behavior` (the side-effect handler called from the signal) is **not** wrapped in `transaction.atomic`: it triggers async cleanup tasks and dataset deletions that must be allowed to proceed independently. The atomic boundary wraps only the synchronous DB state change, not the async infrastructure cleanup.

---

## GCP Cleanup Is Separated into Its Own Service Class

Both `ProjectResourceCleanupService` and `LabResourceCleanupService` exist as dedicated classes, separate from the deletion/archival service classes. GCP resource cleanup (triggering Cloud Build destroy, tearing down Seqera workspaces) is treated as a distinct concern from the database-level deletion operation.

This separation means GCP cleanup can be triggered independently: for example, to retry a failed cleanup without re-running the database deletion: and makes it easier to stub or skip GCP calls in tests.

---

## Lab Deletion Is Gated by Build Status, Not by a Soft-Delete Flag

`LabDeletionService.delete_failed_lab` only permits deletion of labs whose `build_status` is `FAILURE`, `TIMEOUT`, or `CANCELLED`. This is a hard precondition checked in the service layer. Unlike user and organisation deletion (which use soft deletes), a failed lab is **hard deleted** from the database: the lab record and all associated `LabUser` records are removed via `CASCADE`.

