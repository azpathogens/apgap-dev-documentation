class SavedSearchCreateUpdateSerializer(serializers.ModelSerializer):
    """Create/update serializer for `SavedSearch`.

    On every write, `validate_metadata_filters` resolves each condition's
    display-name `key` into a stable `key_id` and dual-writes both into the
    persisted JSON. Renames of `Key.name` thereafter do not break the
    saved search because the runtime evaluator (`_resolve_key`) prefers the
    FK-stable `key_id`. Conditions whose key cannot be resolved are stored
    as-is so the legacy "match nothing" tolerance still applies.
    """
