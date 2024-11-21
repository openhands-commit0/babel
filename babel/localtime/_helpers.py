try:
    import pytz
except ModuleNotFoundError:
    pytz = None
    import zoneinfo

def _get_tzinfo(tzenv: str):
    """Get the tzinfo from `zoneinfo` or `pytz`

    :param tzenv: timezone in the form of Continent/City
    :return: tzinfo object or None if not found
    """
    if pytz is not None:
        try:
            return pytz.timezone(tzenv)
        except pytz.exceptions.UnknownTimeZoneError:
            return None
    else:
        try:
            return zoneinfo.ZoneInfo(tzenv)
        except zoneinfo.ZoneInfoNotFoundError:
            return None

def _get_tzinfo_from_file(filename: str):
    """Get the tzinfo from a timezone file

    :param filename: path to the timezone file
    :return: tzinfo object or None if not found
    """
    if pytz is not None:
        try:
            with open(filename, 'rb') as f:
                return pytz.tzfile.build_tzinfo('local', f)
        except (IOError, OSError, pytz.exceptions.InvalidTimeError):
            return None
    else:
        try:
            return zoneinfo.ZoneInfo.from_file(filename)
        except (IOError, OSError, ValueError):
            return None

def _get_tzinfo_or_raise(tzenv: str):
    """Get the tzinfo from `zoneinfo` or `pytz` or raise ValueError

    :param tzenv: timezone in the form of Continent/City
    :return: tzinfo object
    :raises ValueError: if timezone not found
    """
    tz = _get_tzinfo(tzenv)
    if tz is None:
        raise ValueError(f'Unknown timezone {tzenv!r}')
    return tz