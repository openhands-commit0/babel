"""
    babel.dates
    ~~~~~~~~~~~

    Locale dependent formatting and parsing of dates and times.

    The default locale for the functions in this module is determined by the
    following environment variables, in that order:

     * ``LC_TIME``,
     * ``LC_ALL``, and
     * ``LANG``

    :copyright: (c) 2013-2023 by the Babel Team.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import annotations
import re
import warnings
from functools import lru_cache
from typing import TYPE_CHECKING, SupportsInt
try:
    import pytz
except ModuleNotFoundError:
    pytz = None
    import zoneinfo
import datetime
from collections.abc import Iterable
from babel import localtime
from babel.core import Locale, default_locale, get_global
from babel.localedata import LocaleDataDict
if TYPE_CHECKING:
    from typing_extensions import Literal, TypeAlias
    _Instant: TypeAlias = datetime.date | datetime.time | float | None
    _PredefinedTimeFormat: TypeAlias = Literal['full', 'long', 'medium', 'short']
    _Context: TypeAlias = Literal['format', 'stand-alone']
    _DtOrTzinfo: TypeAlias = datetime.datetime | datetime.tzinfo | str | int | datetime.time | None
NO_INHERITANCE_MARKER = '∅∅∅'
UTC = datetime.timezone.utc
LOCALTZ = localtime.LOCALTZ
LC_TIME = default_locale('LC_TIME')

def _localize(tzinfo: datetime.tzinfo, dt: datetime.datetime) -> datetime.datetime:
    """Convert a datetime object to a specific timezone.

    The datetime object must be naive (have no tzinfo).

    :param tzinfo: The timezone to convert to.
    :param dt: The datetime object to convert.
    :return: A datetime object with tzinfo.
    """
    if dt.tzinfo is not None:
        raise ValueError('Expected naive datetime')
    return dt.replace(tzinfo=tzinfo)

def _get_dt_and_tzinfo(dt_or_tzinfo: _DtOrTzinfo) -> tuple[datetime.datetime | None, datetime.tzinfo]:
    """
    Parse a `dt_or_tzinfo` value into a datetime and a tzinfo.

    See the docs for this function's callers for semantics.

    :rtype: tuple[datetime, tzinfo]
    """
    if isinstance(dt_or_tzinfo, (int, float)):
        dt = datetime.datetime.fromtimestamp(dt_or_tzinfo, UTC)
        tzinfo = dt.tzinfo
    elif isinstance(dt_or_tzinfo, datetime.datetime):
        dt = dt_or_tzinfo
        tzinfo = dt.tzinfo or UTC
    elif isinstance(dt_or_tzinfo, datetime.time):
        dt = datetime.datetime.now().replace(
            hour=dt_or_tzinfo.hour,
            minute=dt_or_tzinfo.minute,
            second=dt_or_tzinfo.second,
            microsecond=dt_or_tzinfo.microsecond
        )
        tzinfo = dt_or_tzinfo.tzinfo or UTC
    elif isinstance(dt_or_tzinfo, datetime.tzinfo) or isinstance(dt_or_tzinfo, str):
        dt = None
        tzinfo = get_timezone(dt_or_tzinfo)
    else:
        dt = datetime.datetime.now(UTC)
        tzinfo = UTC
    return dt, tzinfo

def _get_tz_name(dt_or_tzinfo: _DtOrTzinfo) -> str:
    """
    Get the timezone name out of a time, datetime, or tzinfo object.

    :rtype: str
    """
    pass

def _get_datetime(instant: _Instant) -> datetime.datetime:
    """
    Get a datetime out of an "instant" (date, time, datetime, number).

    .. warning:: The return values of this function may depend on the system clock.

    If the instant is None, the current moment is used.
    If the instant is a time, it's augmented with today's date.

    Dates are converted to naive datetimes with midnight as the time component.

    >>> from datetime import date, datetime
    >>> _get_datetime(date(2015, 1, 1))
    datetime.datetime(2015, 1, 1, 0, 0)

    UNIX timestamps are converted to datetimes.

    >>> _get_datetime(1400000000)
    datetime.datetime(2014, 5, 13, 16, 53, 20)

    Other values are passed through as-is.

    >>> x = datetime(2015, 1, 1)
    >>> _get_datetime(x) is x
    True

    :param instant: date, time, datetime, integer, float or None
    :type instant: date|time|datetime|int|float|None
    :return: a datetime
    :rtype: datetime
    """
    pass

def _ensure_datetime_tzinfo(dt: datetime.datetime, tzinfo: datetime.tzinfo | None=None) -> datetime.datetime:
    """
    Ensure the datetime passed has an attached tzinfo.

    If the datetime is tz-naive to begin with, UTC is attached.

    If a tzinfo is passed in, the datetime is normalized to that timezone.

    >>> from datetime import datetime
    >>> _get_tz_name(_ensure_datetime_tzinfo(datetime(2015, 1, 1)))
    'UTC'

    >>> tz = get_timezone("Europe/Stockholm")
    >>> _ensure_datetime_tzinfo(datetime(2015, 1, 1, 13, 15, tzinfo=UTC), tzinfo=tz).hour
    14

    :param datetime: Datetime to augment.
    :param tzinfo: optional tzinfo
    :return: datetime with tzinfo
    :rtype: datetime
    """
    pass

def _get_time(time: datetime.time | datetime.datetime | None, tzinfo: datetime.tzinfo | None=None) -> datetime.time:
    """
    Get a timezoned time from a given instant.

    .. warning:: The return values of this function may depend on the system clock.

    :param time: time, datetime or None
    :rtype: time
    """
    pass

def get_timezone(zone: str | datetime.tzinfo | None=None) -> datetime.tzinfo:
    """Looks up a timezone by name and returns it.  The timezone object
    returned comes from ``pytz`` or ``zoneinfo``, whichever is available.
    It corresponds to the `tzinfo` interface and can be used with all of
    the functions of Babel that operate with dates.

    If a timezone is not known a :exc:`LookupError` is raised.  If `zone`
    is ``None`` a local zone object is returned.

    :param zone: the name of the timezone to look up.  If a timezone object
                 itself is passed in, it's returned unchanged.
    """
    pass

def get_period_names(width: Literal['abbreviated', 'narrow', 'wide']='wide', context: _Context='stand-alone', locale: Locale | str | None=LC_TIME) -> LocaleDataDict:
    """Return the names for day periods (AM/PM) used by the locale.

    >>> get_period_names(locale='en_US')['am']
    u'AM'

    :param width: the width to use, one of "abbreviated", "narrow", or "wide"
    :param context: the context, either "format" or "stand-alone"
    :param locale: the `Locale` object, or a locale string
    """
    pass

def get_day_names(width: Literal['abbreviated', 'narrow', 'short', 'wide']='wide', context: _Context='format', locale: Locale | str | None=LC_TIME) -> LocaleDataDict:
    """Return the day names used by the locale for the specified format.

    >>> get_day_names('wide', locale='en_US')[1]
    u'Tuesday'
    >>> get_day_names('short', locale='en_US')[1]
    u'Tu'
    >>> get_day_names('abbreviated', locale='es')[1]
    u'mar'
    >>> get_day_names('narrow', context='stand-alone', locale='de_DE')[1]
    u'D'

    :param width: the width to use, one of "wide", "abbreviated", "short" or "narrow"
    :param context: the context, either "format" or "stand-alone"
    :param locale: the `Locale` object, or a locale string
    """
    pass

def get_month_names(width: Literal['abbreviated', 'narrow', 'wide']='wide', context: _Context='format', locale: Locale | str | None=LC_TIME) -> LocaleDataDict:
    """Return the month names used by the locale for the specified format.

    >>> get_month_names('wide', locale='en_US')[1]
    u'January'
    >>> get_month_names('abbreviated', locale='es')[1]
    u'ene'
    >>> get_month_names('narrow', context='stand-alone', locale='de_DE')[1]
    u'J'

    :param width: the width to use, one of "wide", "abbreviated", or "narrow"
    :param context: the context, either "format" or "stand-alone"
    :param locale: the `Locale` object, or a locale string
    """
    pass

def get_quarter_names(width: Literal['abbreviated', 'narrow', 'wide']='wide', context: _Context='format', locale: Locale | str | None=LC_TIME) -> LocaleDataDict:
    """Return the quarter names used by the locale for the specified format.

    >>> get_quarter_names('wide', locale='en_US')[1]
    u'1st quarter'
    >>> get_quarter_names('abbreviated', locale='de_DE')[1]
    u'Q1'
    >>> get_quarter_names('narrow', locale='de_DE')[1]
    u'1'

    :param width: the width to use, one of "wide", "abbreviated", or "narrow"
    :param context: the context, either "format" or "stand-alone"
    :param locale: the `Locale` object, or a locale string
    """
    pass

def get_era_names(width: Literal['abbreviated', 'narrow', 'wide']='wide', locale: Locale | str | None=LC_TIME) -> LocaleDataDict:
    """Return the era names used by the locale for the specified format.

    >>> get_era_names('wide', locale='en_US')[1]
    u'Anno Domini'
    >>> get_era_names('abbreviated', locale='de_DE')[1]
    u'n. Chr.'

    :param width: the width to use, either "wide", "abbreviated", or "narrow"
    :param locale: the `Locale` object, or a locale string
    """
    pass

def get_date_format(format: _PredefinedTimeFormat='medium', locale: Locale | str | None=LC_TIME) -> DateTimePattern:
    """Return the date formatting patterns used by the locale for the specified
    format.

    >>> get_date_format(locale='en_US')
    <DateTimePattern u'MMM d, y'>
    >>> get_date_format('full', locale='de_DE')
    <DateTimePattern u'EEEE, d. MMMM y'>

    :param format: the format to use, one of "full", "long", "medium", or
                   "short"
    :param locale: the `Locale` object, or a locale string
    """
    pass

def get_datetime_format(format: _PredefinedTimeFormat='medium', locale: Locale | str | None=LC_TIME) -> DateTimePattern:
    """Return the datetime formatting patterns used by the locale for the
    specified format.

    >>> get_datetime_format(locale='en_US')
    u'{1}, {0}'

    :param format: the format to use, one of "full", "long", "medium", or
                   "short"
    :param locale: the `Locale` object, or a locale string
    """
    pass

def get_time_format(format: _PredefinedTimeFormat='medium', locale: Locale | str | None=LC_TIME) -> DateTimePattern:
    """Return the time formatting patterns used by the locale for the specified
    format.

    >>> get_time_format(locale='en_US')
    <DateTimePattern u'h:mm:ss\u202fa'>
    >>> get_time_format('full', locale='de_DE')
    <DateTimePattern u'HH:mm:ss zzzz'>

    :param format: the format to use, one of "full", "long", "medium", or
                   "short"
    :param locale: the `Locale` object, or a locale string
    """
    pass

def get_timezone_gmt(datetime: _Instant=None, width: Literal['long', 'short', 'iso8601', 'iso8601_short']='long', locale: Locale | str | None=LC_TIME, return_z: bool=False) -> str:
    """Return the timezone associated with the given `datetime` object formatted
    as string indicating the offset from GMT.

    >>> from datetime import datetime
    >>> dt = datetime(2007, 4, 1, 15, 30)
    >>> get_timezone_gmt(dt, locale='en')
    u'GMT+00:00'
    >>> get_timezone_gmt(dt, locale='en', return_z=True)
    'Z'
    >>> get_timezone_gmt(dt, locale='en', width='iso8601_short')
    u'+00'
    >>> tz = get_timezone('America/Los_Angeles')
    >>> dt = _localize(tz, datetime(2007, 4, 1, 15, 30))
    >>> get_timezone_gmt(dt, locale='en')
    u'GMT-07:00'
    >>> get_timezone_gmt(dt, 'short', locale='en')
    u'-0700'
    >>> get_timezone_gmt(dt, locale='en', width='iso8601_short')
    u'-07'

    The long format depends on the locale, for example in France the acronym
    UTC string is used instead of GMT:

    >>> get_timezone_gmt(dt, 'long', locale='fr_FR')
    u'UTC-07:00'

    .. versionadded:: 0.9

    :param datetime: the ``datetime`` object; if `None`, the current date and
                     time in UTC is used
    :param width: either "long" or "short" or "iso8601" or "iso8601_short"
    :param locale: the `Locale` object, or a locale string
    :param return_z: True or False; Function returns indicator "Z"
                     when local time offset is 0
    """
    pass

def get_timezone_location(dt_or_tzinfo: _DtOrTzinfo=None, locale: Locale | str | None=LC_TIME, return_city: bool=False) -> str:
    """Return a representation of the given timezone using "location format".

    The result depends on both the local display name of the country and the
    city associated with the time zone:

    >>> tz = get_timezone('America/St_Johns')
    >>> print(get_timezone_location(tz, locale='de_DE'))
    Kanada (St. John’s) (Ortszeit)
    >>> print(get_timezone_location(tz, locale='en'))
    Canada (St. John’s) Time
    >>> print(get_timezone_location(tz, locale='en', return_city=True))
    St. John’s
    >>> tz = get_timezone('America/Mexico_City')
    >>> get_timezone_location(tz, locale='de_DE')
    u'Mexiko (Mexiko-Stadt) (Ortszeit)'

    If the timezone is associated with a country that uses only a single
    timezone, just the localized country name is returned:

    >>> tz = get_timezone('Europe/Berlin')
    >>> get_timezone_name(tz, locale='de_DE')
    u'Mitteleurop\\xe4ische Zeit'

    .. versionadded:: 0.9

    :param dt_or_tzinfo: the ``datetime`` or ``tzinfo`` object that determines
                         the timezone; if `None`, the current date and time in
                         UTC is assumed
    :param locale: the `Locale` object, or a locale string
    :param return_city: True or False, if True then return exemplar city (location)
                        for the time zone
    :return: the localized timezone name using location format

    """
    pass

def get_timezone_name(dt_or_tzinfo: _DtOrTzinfo=None, width: Literal['long', 'short']='long', uncommon: bool=False, locale: Locale | str | None=LC_TIME, zone_variant: Literal['generic', 'daylight', 'standard'] | None=None, return_zone: bool=False) -> str:
    """Return the localized display name for the given timezone. The timezone
    may be specified using a ``datetime`` or `tzinfo` object.

    >>> from datetime import time
    >>> dt = time(15, 30, tzinfo=get_timezone('America/Los_Angeles'))
    >>> get_timezone_name(dt, locale='en_US')  # doctest: +SKIP
    u'Pacific Standard Time'
    >>> get_timezone_name(dt, locale='en_US', return_zone=True)
    'America/Los_Angeles'
    >>> get_timezone_name(dt, width='short', locale='en_US')  # doctest: +SKIP
    u'PST'

    If this function gets passed only a `tzinfo` object and no concrete
    `datetime`,  the returned display name is independent of daylight savings
    time. This can be used for example for selecting timezones, or to set the
    time of events that recur across DST changes:

    >>> tz = get_timezone('America/Los_Angeles')
    >>> get_timezone_name(tz, locale='en_US')
    u'Pacific Time'
    >>> get_timezone_name(tz, 'short', locale='en_US')
    u'PT'

    If no localized display name for the timezone is available, and the timezone
    is associated with a country that uses only a single timezone, the name of
    that country is returned, formatted according to the locale:

    >>> tz = get_timezone('Europe/Berlin')
    >>> get_timezone_name(tz, locale='de_DE')
    u'Mitteleurop\\xe4ische Zeit'
    >>> get_timezone_name(tz, locale='pt_BR')
    u'Hor\\xe1rio da Europa Central'

    On the other hand, if the country uses multiple timezones, the city is also
    included in the representation:

    >>> tz = get_timezone('America/St_Johns')
    >>> get_timezone_name(tz, locale='de_DE')
    u'Neufundland-Zeit'

    Note that short format is currently not supported for all timezones and
    all locales.  This is partially because not every timezone has a short
    code in every locale.  In that case it currently falls back to the long
    format.

    For more information see `LDML Appendix J: Time Zone Display Names
    <https://www.unicode.org/reports/tr35/#Time_Zone_Fallback>`_

    .. versionadded:: 0.9

    .. versionchanged:: 1.0
       Added `zone_variant` support.

    :param dt_or_tzinfo: the ``datetime`` or ``tzinfo`` object that determines
                         the timezone; if a ``tzinfo`` object is used, the
                         resulting display name will be generic, i.e.
                         independent of daylight savings time; if `None`, the
                         current date in UTC is assumed
    :param width: either "long" or "short"
    :param uncommon: deprecated and ignored
    :param zone_variant: defines the zone variation to return.  By default the
                           variation is defined from the datetime object
                           passed in.  If no datetime object is passed in, the
                           ``'generic'`` variation is assumed.  The following
                           values are valid: ``'generic'``, ``'daylight'`` and
                           ``'standard'``.
    :param locale: the `Locale` object, or a locale string
    :param return_zone: True or False. If true then function
                        returns long time zone ID
    """
    pass

def format_date(date: datetime.date | None=None, format: _PredefinedTimeFormat | str='medium', locale: Locale | str | None=LC_TIME) -> str:
    """Return a date formatted according to the given pattern.

    >>> from datetime import date
    >>> d = date(2007, 4, 1)
    >>> format_date(d, locale='en_US')
    u'Apr 1, 2007'
    >>> format_date(d, format='full', locale='de_DE')
    u'Sonntag, 1. April 2007'

    If you don't want to use the locale default formats, you can specify a
    custom date pattern:

    >>> format_date(d, "EEE, MMM d, ''yy", locale='en')
    u"Sun, Apr 1, '07"

    :param date: the ``date`` or ``datetime`` object; if `None`, the current
                 date is used
    :param format: one of "full", "long", "medium", or "short", or a custom
                   date/time pattern
    :param locale: a `Locale` object or a locale identifier
    """
    pass

def format_datetime(datetime: _Instant=None, format: _PredefinedTimeFormat | str='medium', tzinfo: datetime.tzinfo | None=None, locale: Locale | str | None=LC_TIME) -> str:
    """Return a date formatted according to the given pattern.

    >>> from datetime import datetime
    >>> dt = datetime(2007, 4, 1, 15, 30)
    >>> format_datetime(dt, locale='en_US')
    u'Apr 1, 2007, 3:30:00\\u202fPM'

    For any pattern requiring the display of the timezone:

    >>> format_datetime(dt, 'full', tzinfo=get_timezone('Europe/Paris'),
    ...                 locale='fr_FR')
    'dimanche 1 avril 2007, 17:30:00 heure d’été d’Europe centrale'
    >>> format_datetime(dt, "yyyy.MM.dd G 'at' HH:mm:ss zzz",
    ...                 tzinfo=get_timezone('US/Eastern'), locale='en')
    u'2007.04.01 AD at 11:30:00 EDT'

    :param datetime: the `datetime` object; if `None`, the current date and
                     time is used
    :param format: one of "full", "long", "medium", or "short", or a custom
                   date/time pattern
    :param tzinfo: the timezone to apply to the time for display
    :param locale: a `Locale` object or a locale identifier
    """
    pass

def format_time(time: datetime.time | datetime.datetime | float | None=None, format: _PredefinedTimeFormat | str='medium', tzinfo: datetime.tzinfo | None=None, locale: Locale | str | None=LC_TIME) -> str:
    """Return a time formatted according to the given pattern.

    >>> from datetime import datetime, time
    >>> t = time(15, 30)
    >>> format_time(t, locale='en_US')
    u'3:30:00\\u202fPM'
    >>> format_time(t, format='short', locale='de_DE')
    u'15:30'

    If you don't want to use the locale default formats, you can specify a
    custom time pattern:

    >>> format_time(t, "hh 'o''clock' a", locale='en')
    u"03 o'clock PM"

    For any pattern requiring the display of the time-zone a
    timezone has to be specified explicitly:

    >>> t = datetime(2007, 4, 1, 15, 30)
    >>> tzinfo = get_timezone('Europe/Paris')
    >>> t = _localize(tzinfo, t)
    >>> format_time(t, format='full', tzinfo=tzinfo, locale='fr_FR')
    '15:30:00 heure d’été d’Europe centrale'
    >>> format_time(t, "hh 'o''clock' a, zzzz", tzinfo=get_timezone('US/Eastern'),
    ...             locale='en')
    u"09 o'clock AM, Eastern Daylight Time"

    As that example shows, when this function gets passed a
    ``datetime.datetime`` value, the actual time in the formatted string is
    adjusted to the timezone specified by the `tzinfo` parameter. If the
    ``datetime`` is "naive" (i.e. it has no associated timezone information),
    it is assumed to be in UTC.

    These timezone calculations are **not** performed if the value is of type
    ``datetime.time``, as without date information there's no way to determine
    what a given time would translate to in a different timezone without
    information about whether daylight savings time is in effect or not. This
    means that time values are left as-is, and the value of the `tzinfo`
    parameter is only used to display the timezone name if needed:

    >>> t = time(15, 30)
    >>> format_time(t, format='full', tzinfo=get_timezone('Europe/Paris'),
    ...             locale='fr_FR')  # doctest: +SKIP
    u'15:30:00 heure normale d\\u2019Europe centrale'
    >>> format_time(t, format='full', tzinfo=get_timezone('US/Eastern'),
    ...             locale='en_US')  # doctest: +SKIP
    u'3:30:00\\u202fPM Eastern Standard Time'

    :param time: the ``time`` or ``datetime`` object; if `None`, the current
                 time in UTC is used
    :param format: one of "full", "long", "medium", or "short", or a custom
                   date/time pattern
    :param tzinfo: the time-zone to apply to the time for display
    :param locale: a `Locale` object or a locale identifier
    """
    pass

def format_skeleton(skeleton: str, datetime: _Instant=None, tzinfo: datetime.tzinfo | None=None, fuzzy: bool=True, locale: Locale | str | None=LC_TIME) -> str:
    """Return a time and/or date formatted according to the given pattern.

    The skeletons are defined in the CLDR data and provide more flexibility
    than the simple short/long/medium formats, but are a bit harder to use.
    The are defined using the date/time symbols without order or punctuation
    and map to a suitable format for the given locale.

    >>> from datetime import datetime
    >>> t = datetime(2007, 4, 1, 15, 30)
    >>> format_skeleton('MMMEd', t, locale='fr')
    u'dim. 1 avr.'
    >>> format_skeleton('MMMEd', t, locale='en')
    u'Sun, Apr 1'
    >>> format_skeleton('yMMd', t, locale='fi')  # yMMd is not in the Finnish locale; yMd gets used
    u'1.4.2007'
    >>> format_skeleton('yMMd', t, fuzzy=False, locale='fi')  # yMMd is not in the Finnish locale, an error is thrown
    Traceback (most recent call last):
        ...
    KeyError: yMMd

    After the skeleton is resolved to a pattern `format_datetime` is called so
    all timezone processing etc is the same as for that.

    :param skeleton: A date time skeleton as defined in the cldr data.
    :param datetime: the ``time`` or ``datetime`` object; if `None`, the current
                 time in UTC is used
    :param tzinfo: the time-zone to apply to the time for display
    :param fuzzy: If the skeleton is not found, allow choosing a skeleton that's
                  close enough to it.
    :param locale: a `Locale` object or a locale identifier
    """
    pass
TIMEDELTA_UNITS: tuple[tuple[str, int], ...] = (('year', 3600 * 24 * 365), ('month', 3600 * 24 * 30), ('week', 3600 * 24 * 7), ('day', 3600 * 24), ('hour', 3600), ('minute', 60), ('second', 1))

def format_timedelta(delta: datetime.timedelta | int, granularity: Literal['year', 'month', 'week', 'day', 'hour', 'minute', 'second']='second', threshold: float=0.85, add_direction: bool=False, format: Literal['narrow', 'short', 'medium', 'long']='long', locale: Locale | str | None=LC_TIME) -> str:
    """Return a time delta according to the rules of the given locale.

    >>> from datetime import timedelta
    >>> format_timedelta(timedelta(weeks=12), locale='en_US')
    u'3 months'
    >>> format_timedelta(timedelta(seconds=1), locale='es')
    u'1 segundo'

    The granularity parameter can be provided to alter the lowest unit
    presented, which defaults to a second.

    >>> format_timedelta(timedelta(hours=3), granularity='day', locale='en_US')
    u'1 day'

    The threshold parameter can be used to determine at which value the
    presentation switches to the next higher unit. A higher threshold factor
    means the presentation will switch later. For example:

    >>> format_timedelta(timedelta(hours=23), threshold=0.9, locale='en_US')
    u'1 day'
    >>> format_timedelta(timedelta(hours=23), threshold=1.1, locale='en_US')
    u'23 hours'

    In addition directional information can be provided that informs
    the user if the date is in the past or in the future:

    >>> format_timedelta(timedelta(hours=1), add_direction=True, locale='en')
    u'in 1 hour'
    >>> format_timedelta(timedelta(hours=-1), add_direction=True, locale='en')
    u'1 hour ago'

    The format parameter controls how compact or wide the presentation is:

    >>> format_timedelta(timedelta(hours=3), format='short', locale='en')
    u'3 hr'
    >>> format_timedelta(timedelta(hours=3), format='narrow', locale='en')
    u'3h'

    :param delta: a ``timedelta`` object representing the time difference to
                  format, or the delta in seconds as an `int` value
    :param granularity: determines the smallest unit that should be displayed,
                        the value can be one of "year", "month", "week", "day",
                        "hour", "minute" or "second"
    :param threshold: factor that determines at which point the presentation
                      switches to the next higher unit
    :param add_direction: if this flag is set to `True` the return value will
                          include directional information.  For instance a
                          positive timedelta will include the information about
                          it being in the future, a negative will be information
                          about the value being in the past.
    :param format: the format, can be "narrow", "short" or "long". (
                   "medium" is deprecated, currently converted to "long" to
                   maintain compatibility)
    :param locale: a `Locale` object or a locale identifier
    """
    pass

def format_interval(start: _Instant, end: _Instant, skeleton: str | None=None, tzinfo: datetime.tzinfo | None=None, fuzzy: bool=True, locale: Locale | str | None=LC_TIME) -> str:
    """
    Format an interval between two instants according to the locale's rules.

    >>> from datetime import date, time
    >>> format_interval(date(2016, 1, 15), date(2016, 1, 17), "yMd", locale="fi")
    u'15.–17.1.2016'

    >>> format_interval(time(12, 12), time(16, 16), "Hm", locale="en_GB")
    '12:12–16:16'

    >>> format_interval(time(5, 12), time(16, 16), "hm", locale="en_US")
    '5:12\u202fAM\u2009–\u20094:16\u202fPM'

    >>> format_interval(time(16, 18), time(16, 24), "Hm", locale="it")
    '16:18–16:24'

    If the start instant equals the end instant, the interval is formatted like the instant.

    >>> format_interval(time(16, 18), time(16, 18), "Hm", locale="it")
    '16:18'

    Unknown skeletons fall back to "default" formatting.

    >>> format_interval(date(2015, 1, 1), date(2017, 1, 1), "wzq", locale="ja")
    '2015/01/01～2017/01/01'

    >>> format_interval(time(16, 18), time(16, 24), "xxx", locale="ja")
    '16:18:00～16:24:00'

    >>> format_interval(date(2016, 1, 15), date(2016, 1, 17), "xxx", locale="de")
    '15.01.2016\u2009–\u200917.01.2016'

    :param start: First instant (datetime/date/time)
    :param end: Second instant (datetime/date/time)
    :param skeleton: The "skeleton format" to use for formatting.
    :param tzinfo: tzinfo to use (if none is already attached)
    :param fuzzy: If the skeleton is not found, allow choosing a skeleton that's
                  close enough to it.
    :param locale: A locale object or identifier.
    :return: Formatted interval
    """
    pass

def get_period_id(time: _Instant, tzinfo: datetime.tzinfo | None=None, type: Literal['selection'] | None=None, locale: Locale | str | None=LC_TIME) -> str:
    """
    Get the day period ID for a given time.

    This ID can be used as a key for the period name dictionary.

    >>> from datetime import time
    >>> get_period_names(locale="de")[get_period_id(time(7, 42), locale="de")]
    u'Morgen'

    >>> get_period_id(time(0), locale="en_US")
    u'midnight'

    >>> get_period_id(time(0), type="selection", locale="en_US")
    u'night1'

    :param time: The time to inspect.
    :param tzinfo: The timezone for the time. See ``format_time``.
    :param type: The period type to use. Either "selection" or None.
                 The selection type is used for selecting among phrases such as
                 “Your email arrived yesterday evening” or “Your email arrived last night”.
    :param locale: the `Locale` object, or a locale string
    :return: period ID. Something is always returned -- even if it's just "am" or "pm".
    """
    pass

class ParseError(ValueError):
    pass

def parse_date(string: str, locale: Locale | str | None=LC_TIME, format: _PredefinedTimeFormat='medium') -> datetime.date:
    """Parse a date from a string.

    This function first tries to interpret the string as ISO-8601
    date format, then uses the date format for the locale as a hint to
    determine the order in which the date fields appear in the string.

    >>> parse_date('4/1/04', locale='en_US')
    datetime.date(2004, 4, 1)
    >>> parse_date('01.04.2004', locale='de_DE')
    datetime.date(2004, 4, 1)
    >>> parse_date('2004-04-01', locale='en_US')
    datetime.date(2004, 4, 1)
    >>> parse_date('2004-04-01', locale='de_DE')
    datetime.date(2004, 4, 1)

    :param string: the string containing the date
    :param locale: a `Locale` object or a locale identifier
    :param format: the format to use (see ``get_date_format``)
    """
    pass

def parse_time(string: str, locale: Locale | str | None=LC_TIME, format: _PredefinedTimeFormat='medium') -> datetime.time:
    """Parse a time from a string.

    This function uses the time format for the locale as a hint to determine
    the order in which the time fields appear in the string.

    >>> parse_time('15:30:00', locale='en_US')
    datetime.time(15, 30)

    :param string: the string containing the time
    :param locale: a `Locale` object or a locale identifier
    :param format: the format to use (see ``get_time_format``)
    :return: the parsed time
    :rtype: `time`
    """
    pass

class DateTimePattern:

    def __init__(self, pattern: str, format: DateTimeFormat):
        self.pattern = pattern
        self.format = format

    def __repr__(self) -> str:
        return f'<{type(self).__name__} {self.pattern!r}>'

    def __str__(self) -> str:
        pat = self.pattern
        return pat

    def __mod__(self, other: DateTimeFormat) -> str:
        if not isinstance(other, DateTimeFormat):
            return NotImplemented
        return self.format % other

class DateTimeFormat:

    def __init__(self, value: datetime.date | datetime.time, locale: Locale | str, reference_date: datetime.date | None=None) -> None:
        assert isinstance(value, (datetime.date, datetime.datetime, datetime.time))
        if isinstance(value, (datetime.datetime, datetime.time)) and value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        self.value = value
        self.locale = Locale.parse(locale)
        self.reference_date = reference_date

    def __getitem__(self, name: str) -> str:
        char = name[0]
        num = len(name)
        if char == 'G':
            return self.format_era(char, num)
        elif char in ('y', 'Y', 'u'):
            return self.format_year(char, num)
        elif char in ('Q', 'q'):
            return self.format_quarter(char, num)
        elif char in ('M', 'L'):
            return self.format_month(char, num)
        elif char in ('w', 'W'):
            return self.format_week(char, num)
        elif char == 'd':
            return self.format(self.value.day, num)
        elif char == 'D':
            return self.format_day_of_year(num)
        elif char == 'F':
            return self.format_day_of_week_in_month()
        elif char in ('E', 'e', 'c'):
            return self.format_weekday(char, num)
        elif char in ('a', 'b', 'B'):
            return self.format_period(char, num)
        elif char == 'h':
            if self.value.hour % 12 == 0:
                return self.format(12, num)
            else:
                return self.format(self.value.hour % 12, num)
        elif char == 'H':
            return self.format(self.value.hour, num)
        elif char == 'K':
            return self.format(self.value.hour % 12, num)
        elif char == 'k':
            if self.value.hour == 0:
                return self.format(24, num)
            else:
                return self.format(self.value.hour, num)
        elif char == 'm':
            return self.format(self.value.minute, num)
        elif char == 's':
            return self.format(self.value.second, num)
        elif char == 'S':
            return self.format_frac_seconds(num)
        elif char == 'A':
            return self.format_milliseconds_in_day(num)
        elif char in ('z', 'Z', 'v', 'V', 'x', 'X', 'O'):
            return self.format_timezone(char, num)
        else:
            raise KeyError(f'Unsupported date/time field {char!r}')

    def format_weekday(self, char: str='E', num: int=4) -> str:
        """
        Return weekday from parsed datetime according to format pattern.

        >>> from datetime import date
        >>> format = DateTimeFormat(date(2016, 2, 28), Locale.parse('en_US'))
        >>> format.format_weekday()
        u'Sunday'

        'E': Day of week - Use one through three letters for the abbreviated day name, four for the full (wide) name,
             five for the narrow name, or six for the short name.
        >>> format.format_weekday('E',2)
        u'Sun'

        'e': Local day of week. Same as E except adds a numeric value that will depend on the local starting day of the
             week, using one or two letters. For this example, Monday is the first day of the week.
        >>> format.format_weekday('e',2)
        '01'

        'c': Stand-Alone local day of week - Use one letter for the local numeric value (same as 'e'), three for the
             abbreviated day name, four for the full (wide) name, five for the narrow name, or six for the short name.
        >>> format.format_weekday('c',1)
        '1'

        :param char: pattern format character ('e','E','c')
        :param num: count of format character

        """
        pass

    def format_period(self, char: str, num: int) -> str:
        """
        Return period from parsed datetime according to format pattern.

        >>> from datetime import datetime, time
        >>> format = DateTimeFormat(time(13, 42), 'fi_FI')
        >>> format.format_period('a', 1)
        u'ip.'
        >>> format.format_period('b', 1)
        u'iltap.'
        >>> format.format_period('b', 4)
        u'iltapäivä'
        >>> format.format_period('B', 4)
        u'iltapäivällä'
        >>> format.format_period('B', 5)
        u'ip.'

        >>> format = DateTimeFormat(datetime(2022, 4, 28, 6, 27), 'zh_Hant')
        >>> format.format_period('a', 1)
        u'上午'
        >>> format.format_period('b', 1)
        u'清晨'
        >>> format.format_period('B', 1)
        u'清晨'

        :param char: pattern format character ('a', 'b', 'B')
        :param num: count of format character

        """
        pass

    def format_frac_seconds(self, num: int) -> str:
        """ Return fractional seconds.

        Rounds the time's microseconds to the precision given by the number         of digits passed in.
        """
        pass

    def get_week_number(self, day_of_period: int, day_of_week: int | None=None) -> int:
        """Return the number of the week of a day within a period. This may be
        the week number in a year or the week number in a month.

        Usually this will return a value equal to or greater than 1, but if the
        first week of the period is so short that it actually counts as the last
        week of the previous period, this function will return 0.

        >>> date = datetime.date(2006, 1, 8)
        >>> DateTimeFormat(date, 'de_DE').get_week_number(6)
        1
        >>> DateTimeFormat(date, 'en_US').get_week_number(6)
        2

        :param day_of_period: the number of the day in the period (usually
                              either the day of month or the day of year)
        :param day_of_week: the week day; if omitted, the week day of the
                            current date is assumed
        """
        pass
PATTERN_CHARS: dict[str, list[int] | None] = {'G': [1, 2, 3, 4, 5], 'y': None, 'Y': None, 'u': None, 'Q': [1, 2, 3, 4, 5], 'q': [1, 2, 3, 4, 5], 'M': [1, 2, 3, 4, 5], 'L': [1, 2, 3, 4, 5], 'w': [1, 2], 'W': [1], 'd': [1, 2], 'D': [1, 2, 3], 'F': [1], 'g': None, 'E': [1, 2, 3, 4, 5, 6], 'e': [1, 2, 3, 4, 5, 6], 'c': [1, 3, 4, 5, 6], 'a': [1, 2, 3, 4, 5], 'b': [1, 2, 3, 4, 5], 'B': [1, 2, 3, 4, 5], 'h': [1, 2], 'H': [1, 2], 'K': [1, 2], 'k': [1, 2], 'm': [1, 2], 's': [1, 2], 'S': None, 'A': None, 'z': [1, 2, 3, 4], 'Z': [1, 2, 3, 4, 5], 'O': [1, 4], 'v': [1, 4], 'V': [1, 2, 3, 4], 'x': [1, 2, 3, 4, 5], 'X': [1, 2, 3, 4, 5]}
PATTERN_CHAR_ORDER = 'GyYuUQqMLlwWdDFgEecabBChHKkjJmsSAzZOvVXx'

def parse_pattern(pattern: str | DateTimePattern) -> DateTimePattern:
    """Parse date, time, and datetime format patterns.

    >>> parse_pattern("MMMMd").format
    u'%(MMMM)s%(d)s'
    >>> parse_pattern("MMM d, yyyy").format
    u'%(MMM)s %(d)s, %(yyyy)s'

    Pattern can contain literal strings in single quotes:

    >>> parse_pattern("H:mm' Uhr 'z").format
    u'%(H)s:%(mm)s Uhr %(z)s'

    An actual single quote can be used by using two adjacent single quote
    characters:

    >>> parse_pattern("hh' o''clock'").format
    u"%(hh)s o'clock"

    :param pattern: the formatting pattern to parse
    """
    pass

def tokenize_pattern(pattern: str) -> list[tuple[str, str | tuple[str, int]]]:
    """
    Tokenize date format patterns.

    Returns a list of (token_type, token_value) tuples.

    ``token_type`` may be either "chars" or "field".

    For "chars" tokens, the value is the literal value.

    For "field" tokens, the value is a tuple of (field character, repetition count).

    :param pattern: Pattern string
    :type pattern: str
    :rtype: list[tuple]
    """
    pass

def untokenize_pattern(tokens: Iterable[tuple[str, str | tuple[str, int]]]) -> str:
    """
    Turn a date format pattern token stream back into a string.

    This is the reverse operation of ``tokenize_pattern``.

    :type tokens: Iterable[tuple]
    :rtype: str
    """
    pass

def split_interval_pattern(pattern: str) -> list[str]:
    """
    Split an interval-describing datetime pattern into multiple pieces.

    > The pattern is then designed to be broken up into two pieces by determining the first repeating field.
    - https://www.unicode.org/reports/tr35/tr35-dates.html#intervalFormats

    >>> split_interval_pattern(u'E d.M. – E d.M.')
    [u'E d.M. – ', 'E d.M.']
    >>> split_interval_pattern("Y 'text' Y 'more text'")
    ["Y 'text '", "Y 'more text'"]
    >>> split_interval_pattern(u"E, MMM d – E")
    [u'E, MMM d – ', u'E']
    >>> split_interval_pattern("MMM d")
    ['MMM d']
    >>> split_interval_pattern("y G")
    ['y G']
    >>> split_interval_pattern(u"MMM d – d")
    [u'MMM d – ', u'd']

    :param pattern: Interval pattern string
    :return: list of "subpatterns"
    """
    pass

def match_skeleton(skeleton: str, options: Iterable[str], allow_different_fields: bool=False) -> str | None:
    """
    Find the closest match for the given datetime skeleton among the options given.

    This uses the rules outlined in the TR35 document.

    >>> match_skeleton('yMMd', ('yMd', 'yMMMd'))
    'yMd'

    >>> match_skeleton('yMMd', ('jyMMd',), allow_different_fields=True)
    'jyMMd'

    >>> match_skeleton('yMMd', ('qyMMd',), allow_different_fields=False)

    >>> match_skeleton('hmz', ('hmv',))
    'hmv'

    :param skeleton: The skeleton to match
    :type skeleton: str
    :param options: An iterable of other skeletons to match against
    :type options: Iterable[str]
    :return: The closest skeleton match, or if no match was found, None.
    :rtype: str|None
    """
    pass