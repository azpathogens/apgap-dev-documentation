# CSV-Handler Layer

## CSV Import Handlers Follow a Consistent Handler Class Pattern

CSV import logic is encapsulated in dedicated handler classes (`CSVImportHandler`, `ValueImportHandler`) rather than living in views or serializers. Both handlers are instantiated with context (lab, key) that scopes all subsequent operations, and expose a primary `process_csv` or equivalent method that returns a results dictionary with success counts, errors, and warnings.

This pattern keeps CSV parsing and file-lookup logic out of the view layer and makes the handlers independently testable. Any new CSV import surface should follow the same structure: a class instantiated with context, a single entry-point method, and a structured results dict as output.

---

## Per-Row Exceptions Are Caught So a Single Bad Row Never Aborts the Whole Upload

`ValueImportHandler` explicitly documents that per-row exceptions are caught individually, so one bad row does not abort processing of the rest of the CSV. `CSVImportHandler._process_row` follows the same design: errors are collected and returned in the results dict rather than raised.

This is the required pattern for any bulk import operation. Raising on the first error would leave partial state and force users to fix one row at a time. Any new import handler must catch per-row exceptions, accumulate them in an errors list, and continue to the next row.

---

## Pre-Existing Rows Are Reused, Not Duplicated: Warnings, Not Errors

`ValueImportHandler` documents that pre-existing `Value`, `MetadataTag`, or `MetadataTemplateOption` rows are reused rather than creating duplicates. When a row already exists, a **warning** is emitted rather than an error, and the existing row does not count against the error total.

`CSVImportHandler._create_metadata_tag` follows the same pattern: it uses get-or-create logic for `Value` and `MetadataTag` rows. Idempotency is a first-class requirement for all import handlers: running the same CSV twice should produce the same state, not duplicate rows or errors.

---

## The Info Row Is Optional and Validated, Not Required

`CSVImportHandler` supports an optional second-row info row (indicating `OPTIONAL`/`REQUIRED` per column) in uploaded CSVs. The handler detects whether this row is present via `_is_info_row`, and if present, validates it against the expected values derived from the templates. If absent, processing continues without error.

Importantly, `_validate_info_row` returns `None` (not an error) when no info row is present: the caller must not treat an absent info row as invalid. When the info row is present but incorrect, a structured list of per-column mismatch messages is returned.

The export side (`CSVExportHandler.add_metadata_info_row`) generates the matching info row format so that exported templates can be re-imported without modification.

---

## Multi-Select and LIST Values Are Pipe-Separated in CSV

`CSVImportHandler._create_metadata_tag` handles multi-select and LIST field types by splitting values on a pipe character (`|`) within a single CSV cell. This is the canonical serialisation format for multi-value fields in CSV exports and imports throughout the codebase.

`LIST` type accepts any free-form text or numeric string (no option validation against template options). `SELECT` type validates each value against predefined template options. Both are normalised via the key's `data_type` before validation, which includes date normalisation for date-type fields.

---

## Metadata CSV Export Resolves to the Original File for Copies

`collect_metadata_rows` in `files-metadata_csv` explicitly resolves copied files (files in analytical datasets) back to their original file before reading metadata tags, because metadata lives on the original file, not the copy. Forgetting this would produce empty metadata rows for all files in analytical datasets.

The module exposes three entry points for different use cases: `collect_metadata_rows` (returns header + rows for composition), `build_metadata_csv_string` (returns a complete CSV string), and `write_metadata_csv` (streams directly to a response object). The caller is responsible for setting `Content-Type` and `Content-Disposition` when using the streaming variant.

---

## Export Queryset Accepts an Optional Pre-Optimised Queryset

`CSVExportHandler.generate_template_csv` accepts an optional `base_queryset` parameter. When provided, the handler uses the caller's already-optimised queryset (with `select_related`/`prefetch_related` already applied) instead of constructing a new one. When absent, it falls back to a basic `select_related` on key.

This pattern: accepting an optional pre-optimised queryset rather than always constructing one internally: should be followed by any handler or utility that may be called from a context where the queryset is already warmed, to avoid redundant DB hits.

---

## Pathogen Import Is Upsert-Only: Deletions Must Be Explicit

The Pathogen CSV import handler is explicitly scoped to upsert operations by name only. Deletions are not handled by the import path and must go through the API or Django admin explicitly. This is documented at the module level as a deliberate constraint, not an omission.

Any CSV import handler that modifies a registry-style model (one where records persist independently of the import) should document the same constraint explicitly: imports add or update, never delete.

