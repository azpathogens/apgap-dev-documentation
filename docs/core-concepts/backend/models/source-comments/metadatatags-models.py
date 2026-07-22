def validate_gps_value(value: str, key_name: str) -> None:
    """Validate that a string matches the expected GPS coordinate format.

    Per NCBI/SRA specification: "d[d.dddd] N|S d[dd.dddd] E|W"
    At least 4 decimal places are required for both latitude and longitude.

    Args:
        value: The coordinate string to validate.
        key_name: The metadata key name, used in the error message.

    Raises:
        ValidationError: If the value does not match GPS_PATTERN.
    """


# Canonical date formats for parsing metadata date values
# The first format (YYYY-MM-DD) is the normalized output format
DATE_FORMATS = [
    "%Y-%m-%d",  # Canonical format: 2026-01-23
    "%m/%d/%Y",  # US format: 01/23/2026
    "%m/%d/%y",  # US short year: 01/23/26
    "%d/%m/%Y",  # European format: 23/01/2026
    "%d/%m/%y",  # European short year: 23/01/26
    "%Y-%m-%d %H:%M:%S",  # With time: 2026-01-23 14:30:00
    "%Y-%m-%dT%H:%M:%S",  # ISO 8601: 2026-01-23T14:30:00
    "%Y-%m-%dT%H:%M:%S.%f",  # ISO 8601 with microseconds
]


class Key(models.Model):
    """
    Predefined keys for metadata tags.
    """

    @classmethod
    def get_pathogen_key(cls):
        """The Key flagged as the pathogen key, or None if none is configured"""

    @staticmethod
    def normalize_name(name):
        """
        Normalize the name to uppercase and remove multiple spaces.
        """

    def clean(self):
        """
        Validate the model fields.
        - Ensure name is stored in uppercase and trimmed of spaces.
        - Validate data_type is a valid choice.
        - Block silent shadowing of a historical name reserved by `KeyAlias`.
        """

        # Shadow-protection: an alias name -> KeyA reserves that name.
        # Letting someone create KeyB (or rename KeyB) under the same name
        # would silently break the rename trail since `_resolve_key` would
        # hit the canonical lookup before consulting KeyAlias. Round-trip
        # renames (A->B->A) are allowed because the conflicting alias
        # points back at THIS key, so `.exclude(key_id=self.pk)` clears it.
        # KeyAlias is defined later in this module — clean() is called at
        # runtime, so the forward reference resolves naturally.

    def validate_value(self, value_name):
        """
        Validate that a value string is appropriate for this key's data_type.

        Args:
            value_name: The value string to validate

        Raises:
            ValidationError: If the value is not valid for the key's data_type
        """
        # TEXT, SELECT, and LIST don't need format validation
        # SELECT values are validated against available options at the template level
        # LIST values are free-form (text or numbers) — only the non-empty check above applies

    def save(self, *args, **kwargs):  # noqa: DJ012
        """
        Call clean before saving to ensure case consistency.

        On a rename (i.e. an UPDATE that changes ``name``), insert a
        ``KeyAlias`` row mapping the previous canonical name to this Key
        in the same transaction. This is the safety net that lets
        name-based lookups in ``metadata_filter_eval._resolve_key`` and
        the seed_validation_rules ``_resolve_template`` continue to find
        this Key by its old name. Idempotent: a duplicate alias is
        silently absorbed by the unique constraint.
        """


class KeyAlias(models.Model):
    """Records every prior `Key.name` so name-based lookups survive renames.

    The unique constraint on ``name`` makes the table double as a guard
    against silently shadowing a historical name with a brand-new Key:
    if someone tries to ``Key.objects.create(name=<historical name>)``,
    the alias-side INSERT either pre-empts (when the alias was inserted
    first) or the FK-side INSERT fails on the Key.name unique constraint.
    Either way the operator is forced to deal with the ambiguity rather
    than absorb it silently.

    Populated automatically by ``Key.save`` on every rename. The
    `migrate_renamed_keys` management command and the seed-time
    ``KEY_RENAMES`` dict both go through ``Key.save`` so they pick up
    aliases for free.
    """


class Value(models.Model):
    """
    Predefined values for metadata tags.
    """

    @staticmethod
    def normalize_name(name):
        """
        Normalize the name to uppercase and remove multiple spaces.
        """

    def clean(self):
        """
        Ensure name is stored in uppercase and trimmed of spaces.
        Also removes multiple spaces.
        """

    def save(self, *args, **kwargs):
        """
        Call clean before saving to ensure case consistency.
        """


class MetadataTag(models.Model):
    """
    A metadata tag that can be assigned to datasets.
    The key and value are predefined to ensure consistency.
    """
