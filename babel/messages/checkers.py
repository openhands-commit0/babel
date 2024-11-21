"""
    babel.messages.checkers
    ~~~~~~~~~~~~~~~~~~~~~~~

    Various routines that help with validation of translations.

    :since: version 0.9

    :copyright: (c) 2013-2023 by the Babel Team.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import annotations
from collections.abc import Callable
from babel.messages.catalog import PYTHON_FORMAT, Catalog, Message, TranslationError
_string_format_compatibilities = [{'i', 'd', 'u'}, {'x', 'X'}, {'f', 'F', 'g', 'G'}]

def _find_checkers() -> list[Callable[[Catalog | None, Message], object]]:
    """Find all functions in this module that can check messages.

    A checker function takes two arguments, the catalog and the message,
    and returns None if the message is valid, or raises a TranslationError
    if the message is invalid.
    """
    checkers = []
    for name, func in globals().items():
        if name.startswith('_') or not callable(func):
            continue
        checkers.append(func)
    return checkers

def num_plurals(catalog: Catalog | None, message: Message) -> None:
    """Verify the number of plurals in the translation."""
    if not message.pluralizable or not message.string:
        return
    if not catalog or not catalog.num_plurals:
        return
    if len(message.string) != catalog.num_plurals:
        raise TranslationError(
            'catalog says there should be %d plural forms, but '
            'message "%s" has %d' % (
                catalog.num_plurals, message.id, len(message.string)
            )
        )

def python_format(catalog: Catalog | None, message: Message) -> None:
    """Verify the format string placeholders in the translation."""
    if not message.python_format:
        return
    if not message.string:
        return

    msgid = message.id
    if isinstance(msgid, (list, tuple)):
        msgid = msgid[0]
    msgstr = message.string
    if isinstance(msgstr, (list, tuple)):
        msgstr = msgstr[0]

    if not PYTHON_FORMAT.search(msgid):
        return

    if not PYTHON_FORMAT.search(msgstr):
        raise TranslationError('python format string mismatch')

def _validate_format(format: str, alternative: str) -> None:
    """Test format string `alternative` against `format`.  `format` can be the
    msgid of a message and `alternative` one of the `msgstr`\\s.  The two
    arguments are not interchangeable as `alternative` may contain less
    placeholders if `format` uses named placeholders.

    The behavior of this function is undefined if the string does not use
    string formatting.

    If the string formatting of `alternative` is compatible to `format` the
    function returns `None`, otherwise a `TranslationError` is raised.

    Examples for compatible format strings:

    >>> _validate_format('Hello %s!', 'Hallo %s!')
    >>> _validate_format('Hello %i!', 'Hallo %d!')

    Example for an incompatible format strings:

    >>> _validate_format('Hello %(name)s!', 'Hallo %s!')
    Traceback (most recent call last):
      ...
    TranslationError: the format strings are of different kinds

    This function is used by the `python_format` checker.

    :param format: The original format string
    :param alternative: The alternative format string that should be checked
                        against format
    :raises TranslationError: on formatting errors
    """
    def _compare_format_chars(a: str, b: str) -> bool:
        """Compare two format chars for compatibility."""
        for compat_set in _string_format_compatibilities:
            if a in compat_set and b in compat_set:
                return True
        return a == b

    def _collect_placeholders(string: str) -> list[tuple[str | None, str]]:
        """Get a list of placeholders in a format string."""
        result = []
        for match in PYTHON_FORMAT.finditer(string):
            name, format_str, format_type = match.groups()
            result.append((name, format_type))
        return result

    format_placeholders = _collect_placeholders(format)
    alternative_placeholders = _collect_placeholders(alternative)

    # If the original string uses named placeholders, the alternative
    # must use named placeholders or no placeholders at all
    if [name for name, _ in format_placeholders if name is not None]:
        if [name for name, _ in alternative_placeholders if name is None]:
            raise TranslationError('the format strings are of different kinds')

    # Compare format chars
    for (name1, type1), (name2, type2) in zip(format_placeholders, alternative_placeholders):
        if not _compare_format_chars(type1, type2):
            raise TranslationError('format specifiers are incompatible')
checkers: list[Callable[[Catalog | None, Message], object]] = _find_checkers()