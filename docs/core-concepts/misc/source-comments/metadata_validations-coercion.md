"""
Pure-function coercion helpers for untrusted user input.

Every helper returns `(ok: bool, value)`. Handlers only treat a value as
numeric / date / url / etc. if `ok` is True. The goal is defensive:
*refuse* to coerce anything ambiguous (bool-as-number, hex strings, etc.)
rather than accept and hope for the best.
"""

# Regex for ISO-like dates. We intentionally keep the parser list tight:
# every format is unambiguous.
_DATE_FORMATS = (
    "%Y-%m-%d",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%SZ",
    "%Y-%m-%d %H:%M:%S",
    "%Y/%m/%d",
)

# MM/DD/YYYY is ambiguous with DD/MM/YYYY. We accept it but only when the
# month is unambiguously > 12 or we're in US locale mode. The seed defaults
# to ISO-8601; MM/DD/YYYY is a soft secondary format callers can opt into.
_AMBIGUOUS_DATE_FORMATS = (
    "%m/%d/%Y",
    "%m/%d/%y",
)


def coerce_number(value: object) -> tuple[bool, Decimal | None]:
    """
    Try to parse a finite decimal number from `value`.

    Rejects: bool, None, empty/whitespace, NaN, ±Inf, complex, hex/octal
    literals, underscores-as-separators, EU thousands separators, bytes.
    """


def coerce_date(value: object, *, allow_ambiguous: bool = False) -> tuple[bool, date | None]:
    """
    Parse a date from a string or return a `date`/`datetime` unchanged (as a date).

    `allow_ambiguous=True` additionally tries MM/DD/YYYY formats.
    """


def is_alphanumeric(value: object) -> bool:
    """
    Restrictive alphanumeric: ASCII letters + digits only. Explicitly rejects
    whitespace, punctuation, emoji, RTL overrides, full-width characters,
    and null bytes.
    """


def is_nwss_site_id(value: object) -> bool:
    """NWSS site_id: #####-###-##-##-##"""


def is_nwss_sample_id(value: object) -> bool:
    """
    NWSS jurisdiction sample id: <=20 chars, alnum + underscore + hyphen, no ws.
    """


def is_npdes(value: object) -> bool:
    """
    NPDES permit number: <2-letter state><7 digits>, OR sentinel "-1".
    """


def is_gps(value: object) -> bool:
    """
    Accept either decimal "lat,lon" (e.g. "33.4,-112.0") or the
    legacy DMS-ish "23.70000 N 90.37500 E" form used elsewhere in the codebase.
    """


def safe_float(value: object) -> float | None:
    """Return float or None; rejects NaN/Inf."""


def normalize_for_compare(value: str) -> str:
    """Case-insensitive + NFC + whitespace-trimmed comparison key."""
