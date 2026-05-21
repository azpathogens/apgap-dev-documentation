"""csv import handler for bulk-creating metadata values and tags under a single key."""


class ValueImportHandler:
    """
    Parses a CSV with a single ``value`` column and bulk-creates
    Value rows + MetadataTag rows binding each Value to ``key``.

    Each new Value is also linked as a MetadataTemplateOption to the
    MetadataTemplate(s) for ``key`` under the supplied source types
    (and/or the core template), so the values become selectable in
    the file metadata forms. Templates are auto-created when missing.

    Pre-existing Value, MetadataTag, or MetadataTemplateOption rows
    are reused; a warning is emitted but they do not count as errors.
    Per-row exceptions are caught so a single bad row never aborts
    the rest of the upload.
    """
