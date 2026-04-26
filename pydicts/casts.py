"""
    All cast will raise a CastException(message) if cast fails
    All cast will have a parameter ignore_exception=False, to ignore exceptions and return ignore_exception_value
    All cast hava a method ignore_exception_value=None
"""

from decimal import Decimal
import locale
from datetime import timedelta, date, datetime, time
from gettext import translation
from importlib.resources import files
from pydicts import exceptions
from re import match
from zoneinfo import ZoneInfo
from base64 import b64encode, b64decode
from isodate import parse_duration, duration_isoformat


try:
    t=translation('pydicts', files("pydicts") / 'locale')
    _=t.gettext
except:
    _=str

dict_month_names={
    "es":{1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"},
    "en":{1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June", 7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"},
}


def get_locale():
    current_locale = locale.getlocale(locale.LC_TIME)[0] 
    if current_locale is None:
        current_locale = locale.getlocale()[0]
    return current_locale

    
def object_or_empty(v):
    """Returns an empty string if the input value is None, otherwise returns the value itself.

    Args:
        v (any): The input value.

    Returns:
        str or any: An empty string if `v` is None, otherwise `v`.

    Example:
        >>> object_or_empty(None)
        ''
        >>> object_or_empty("hello")
        'hello'
    """
    return "" if v is None else v

def str2decimal(value, ignore_exception=False, ignore_exception_value=None):
    """
        Converts a string  to a decimal
        Parameters:
    Converts a string representation to a Decimal object.

    Args:
        value (str): The string to convert.
        ignore_exception (bool, optional): If True, returns `ignore_exception_value` on error instead of raising an exception. Defaults to False.
        ignore_exception_value (any, optional): The value to return if an exception is ignored. Defaults to None.

    Returns:
        Decimal: The converted Decimal object.
    """
    original=value
    error=f"Error in Pydicts.cast.str2decimal method. Value: {original} Value class: {value.__class__.__name__}"

    if is_noe(value) or not value.__class__ ==str:
        if ignore_exception is False:
            raise exceptions.CastException(error)
        else:
            return ignore_exception_value

    try:
        return Decimal(value)
    except:

        if ignore_exception is False:
            raise exceptions.CastException(error)
        else:
            return ignore_exception_value

def str2bool(value, ignore_exception=False, ignore_exception_value=None):
    """
    Converts a string representation ("true", "false", "1", "0") to a boolean.
    Case-insensitive for "true" and "false".

    Args:
        value (str): The string to convert.
        ignore_exception (bool, optional): If True, returns `ignore_exception_value` on error instead of raising an exception. Defaults to False.
        ignore_exception_value (any, optional): The value to return if an exception is ignored. Defaults to None.

    Returns:
        bool: The converted boolean value.
    """
    original=value
    error=f"Error in Pydicts.cast.str2bool method. Value: {original} Value class: {value.__class__.__name__}"

    if is_noe(value) or not value.__class__ ==str:
        if ignore_exception is False:
            raise exceptions.CastException(error)
        else:
            return ignore_exception_value
        
    if value=="0" or value.lower()=="false":
        return False
    elif value=="1" or value.lower()=="true":
        return True
    else:
        if ignore_exception is False:
            raise exceptions.CastException(error)
        else:
            return ignore_exception_value

def none2alternative(value, alternative):
    """If a value is None, returns an alternative value; otherwise, returns the original value.

    Args:
        value (any): The input value to check.
        alternative (any): The value to return if `value` is None.

    Returns:
        any: `alternative` if `value` is None, otherwise `value`.

    Example:
        >>> none2alternative(None, 0)
        0
        >>> none2alternative(5, 0)
        5
    """
    if value is None:
        return alternative
    return value

def bytes2str(value, code='UTF-8', ignore_exception=False, ignore_exception_value=None):
    """Converts a bytes object to a string using the specified encoding.
    """ 
    
    original=value
    error=f"Error in Pydicts.cast.bytes2str method. Value: {original} Value class: {value.__class__.__name__}"

    if value is None or not value.__class__==bytes:

        if ignore_exception is False:
            raise exceptions.CastException(error)
        else:
            return ignore_exception_value

    try:
        return value.decode(code)
    except:

        if ignore_exception is False:
            raise exceptions.CastException(error)
        else:
            return ignore_exception_value

    
def str2bytes(value, code='UTF8', ignore_exception=False, ignore_exception_value=None):
    """Converts a string to a bytes object using the specified encoding.

    Args:
        value (str): The string to convert.
        code (str, optional): The encoding to use. Defaults to 'UTF8'.
        ignore_exception (bool, optional): If True, returns `ignore_exception_value` on error instead of raising an exception. Defaults to False.
        ignore_exception_value (any, optional): The value to return if an exception is ignored. Defaults to None.

    Returns:
        bytes: The converted bytes object.
    """       
    original=value
    error=f"Error in Pydicts.cast.str2bytes method. Value: {original} Value class: {value.__class__.__name__}"

    if value is None or not value.__class__==str:
        if ignore_exception is False:
            raise exceptions.CastException(error)
        else:
            return ignore_exception_value

    try:
        return value.encode(code)
    except:
        if ignore_exception is False:
            raise exceptions.CastException(error)
        else:
            return ignore_exception_value
            
        
def base64bytes2bytes(value, ignore_exception=False, ignore_exception_value=None): # Renamed from base642bytes to base64bytes2bytes for clarity
    """Decodes a base64-encoded bytes object back into its original bytes.

    Args:
        value (bytes): The base64-encoded bytes object.
        ignore_exception (bool, optional): If True, returns `ignore_exception_value` on error instead of raising an exception. Defaults to False.
        ignore_exception_value (any, optional): The value to return if an exception is ignored. Defaults to None.

    Returns:
        bytes: The decoded bytes object.
    """ 
    
    original=value
    error=f"Error in Pydicts.cast.base642bytes method. Value: {original} Value class: {value.__class__.__name__}"

    if value is None or not value.__class__==bytes:
        if ignore_exception is False:
            raise exceptions.CastException(error)
        else:
            return ignore_exception_value

    try:
        return b64decode(value)
    except:
        if ignore_exception is False:
            raise exceptions.CastException(error)
        else:
            return ignore_exception_value

    
def bytes2base64bytes(value, ignore_exception=False, ignore_exception_value=None): # Renamed from bytes2base64 to bytes2base64bytes for clarity
    """Encodes a bytes object into a base64-encoded bytes object.

    Args:
        value (bytes): The bytes object to encode.
        ignore_exception (bool, optional): If True, returns `ignore_exception_value` on error instead of raising an exception. Defaults to False.
        ignore_exception_value (any, optional): The value to return if an exception is ignored. Defaults to None.

    Returns:
        bytes: The base64-encoded bytes object.
    """       
    original=value
    error=f"Error in Pydicts.cast.bytes2base64 method. Value: {original} Value class: {value.__class__.__name__}"

    if value is None or not value.__class__==bytes:
        if ignore_exception is False:
            raise exceptions.CastException(error)
        else:
            return ignore_exception_value

    try:
        return b64encode(value)
    except:
        if ignore_exception is False:
            raise exceptions.CastException(error)
        else:
            return ignore_exception_value    

### Returns if a datetime is aware
def is_aware(dt):
    """Checks if a datetime object is timezone-aware.

    Args:
        dt (datetime): The datetime object to check.

    Returns:
        bool: True if the datetime object is timezone-aware, False otherwise.
    """
    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        return False
    return True

    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        return False
    return True

## Returns if a datetime is naive
def is_naive(dt):
    """Checks if a datetime object is timezone-naive.

    Args:
        dt (datetime): The datetime object to check.

    Returns:
        bool: True if the datetime object is timezone-naive, False otherwise.
    """
    return not is_aware(dt)

def is_noe(value):
    """Checks if a value is None or an empty string.

    Args:
        value (any): The value to check.

    Returns:
        bool: True if the value is None or an empty string, False otherwise.
    """
    if value is None:
        return True
    if value =="":
        return True
    return False
    
def dtaware(date_, time_, tz_name):
    """Creates a timezone-aware datetime object from a date, time, and timezone name.

    Args:
        date_ (date): A `datetime.date` object.
        time_ (time): A `datetime.time` object.
        tz_name (str): A string representing the timezone name (e.g., "Europe/Madrid").

    Returns:
        datetime: A timezone-aware datetime object.
    """
    dt_naive=dtnaive(date_, time_)
    return dtnaive2dtaware(dt_naive, tz_name)

def dtnaive2dtaware(dtnaive, tz_name):
    return dtnaive.replace(tzinfo=ZoneInfo(tz_name))

def dtaware2dtnaive(dtaware):
    """Converts a timezone-aware datetime object to a timezone-naive datetime object.

    Args:
        dtaware (datetime): A timezone-aware datetime object.

    Returns:
        datetime: A timezone-naive datetime object.

    Raises:
        exceptions.CastException: If the input datetime object is not timezone-aware.
    """
    if not is_aware(dtaware): 
        raise exceptions.CastException(f"{dtaware} should be a dtaware")
    return dtaware.replace(tzinfo=None)

def dtaware_now(tzname=None):
    """Returns the current datetime as a timezone-aware object.

    Args:
        tzname (str, optional): The name of the timezone. If None, returns UTC aware datetime. Defaults to None.

    Returns:
        datetime: A timezone-aware datetime object representing the current time.

        If tzname is None: returns UTC dtaware
    """
    utc_aware = datetime.now(ZoneInfo('UTC'))
    if tzname is None:
        return utc_aware
    else:
        return dtaware_changes_tz(utc_aware, tzname)

def dtnaive_now():
    """Returns the current datetime as a timezone-naive object.

    Returns:
        datetime: A timezone-naive datetime object representing the current time.
    """
    return datetime.now()

def dtnaive(date_, hour):
    """Creates a timezone-naive datetime object from a date and time object.

    Args:
        date_ (date): A `datetime.date` object.
        hour (time): A `datetime.time` object.

    Returns:
        datetime: A timezone-naive datetime object.
    """
    return datetime(date_.year,  date_.month,  date_.day,  hour.hour,  hour.minute,  hour.second, hour.microsecond)


## Returns a date with the first date of the month
## @param year Year to search fist day
## @param month Month to search first day
def date_first_of_the_month(year, month):
    """Returns a date object representing the first day of the specified month and year.

    Args:
        year (int): The year.
        month (int): The month (1-12).

    Returns:
        date: A `datetime.date` object for the first day of the month.
    """
    return date(year, month, 1)

## Returns a date with the last date of the month
## @param year Year to search last day
## @param month Month to search last day
def date_last_of_the_month(year, month):
    """Returns a date object representing the last day of the specified month and year.

    Args:
        year (int): The year.
        month (int): The month (1-12).

    Returns:
        date: A `datetime.date` object for the last day of the month.
    """
    if month==12:
        return date(year, month, 31)
    return date(year, month+1, 1)-timedelta(days=1)

## Returns a date with the first date of the year
## @param year Year to search first day
def date_first_of_the_year(year):
    """Returns a date object representing the first day of the specified year.

    Args:
        year (int): The year.

    Returns:
        date: A `datetime.date` object for January 1st of the year.
    """
    return date_first_of_the_month(year, 1)

## Returns a date with the last date of the year
## @param year Year to search last day
def date_last_of_the_year(year):
    """Returns a date object representing the last day of the specified year.

    Args:
        year (int): The year.

    Returns:
        date: A `datetime.date` object for December 31st of the year.
    """
    return date_last_of_the_month(year,12)

## Returns a date with the first date of the month after x months
## @param year Year to search  day
## @param month Month to search day
## @param x Number of months after parameters. Cab be positive to add months or negative to substract months
def date_first_of_the_next_x_months(year, month, x):
    """Calculates the date of the first day of the month `x` months from the given year and month.

    Args:
        year (int): The starting year.
        month (int): The starting month (1-12).
        x (int): The number of months to add (positive) or subtract (negative).

    Returns:
        date: A `datetime.date` object for the first day of the target month.
    """
def date_first_of_the_next_x_months(year, month, x):
    if x>=0:
        first=date(year, month, 1)
        for i in range(x):
            last=date_last_of_the_month(first.year, first.month)
            first=last+timedelta(days=1)
        return first
    else:#<0
        first=date(year, month, 1)
        for i in range(abs(x)):
            last_before=first-timedelta(days=1)
            first=date_first_of_the_month(last_before.year, last_before.month)
        return first    

## Returns a date with the last date of the month after x months
## @param year Year to search  day
## @param month Month to search day
## @param x Number of months after parameters. Cab be positive to add months or negative to substract months
def date_last_of_the_next_x_months(year, month, x):
    """Calculates the date of the last day of the month `x` months from the given year and month.

    Args:
        year (int): The starting year.
        month (int): The starting month (1-12).
        x (int): The number of months to add (positive) or subtract (negative).

    Returns:
        date: A `datetime.date` object for the last day of the target month.
    """
def date_last_of_the_next_x_months(year, month, x):
    first=date_first_of_the_next_x_months(year, month, x)
    return date_last_of_the_month(first.year, first.month)

def dtaware_month_end(year, month, tz_name):
    return dtaware_day_end_from_date(date_last_of_the_month(year, month), tz_name)
    
def dtaware_year_start(year, tz_name):
    """Returns a timezone-aware datetime object representing the start of the specified year.

    Args:
        year (int): The year.
        tz_name (str): The name of the timezone.

    Returns:
        datetime: A timezone-aware datetime object for January 1st, 00:00:00.000000.
    """
    return dtaware_day_start_from_date(date(year, 1, 1), tz_name)
    
def dtaware_year_end(year, tz_name):
    """Returns a timezone-aware datetime object representing the end of the specified year.

    Args:
        year (int): The year.
        tz_name (str): The name of the timezone.

    Returns:
        datetime: A timezone-aware datetime object for December 31st, 23:59:59.999999.
    """
    return dtaware_day_end_from_date(date(year, 12, 31), tz_name)
    
def dtaware_day_end(dt, tz_name):
    """
        Returns the last  datetime (microsecond  level) of the  day in tz_name zone
    """
    if is_naive(dt):
        raise exceptions.CastException(_("A datetime with timezone is needed"))
    dt = dtaware_changes_tz(dt, tz_name)
    return dt.replace(hour=23, minute=59, second=59, microsecond=999999)
    
def dtnaive_day_end(dt):
    """Returns a timezone-naive datetime object representing the end of the day for the given datetime.

    Args:
        dt (datetime): A timezone-naive datetime object.

    Returns:
        datetime: A timezone-naive datetime object set to 23:59:59.999999 of the same day.

    Raises:
        exceptions.CastException: If the input datetime object is timezone-aware."""
    """
        Returns the last  datetime (microsecond  level) of the  day in naive format
    """
    if is_aware(dt):
        raise exceptions.CastException(_("A datetime without timezone is needed"))
    return dt.replace(hour=23, minute=59, second=59, microsecond=999999)

## Returns the end of the day dtnaive from a date
def dtnaive_day_end_from_date(date_):
    """Returns a timezone-naive datetime object representing the end of the day for a given date.

    Args:
        date_ (date): A `datetime.date` object.

    Returns:
        datetime: A timezone-naive datetime object set to 23:59:59.999999 of the given date.
    """
    dt=datetime(date_.year, date_.month, date_.day)
    return dtnaive_day_end(dt)

## Returns the end of the day dtaware in utc format
def dtaware_day_end_from_date(date, tz_name):
    """Returns a timezone-aware datetime object representing the end of the day for a given date and timezone.

    Args:
        date (date): A `datetime.date` object.
        tz_name (str): The name of the timezone.

    Returns:
        datetime: A timezone-aware datetime object set to 23:59:59.999999 of the given date in the specified timezone.
    """
    return dtaware(date, time(23, 59, 59, 999999), tz_name)
    
## Returns a dtnaive or dtawre (as parameter) with the end of the day
def dtnaive_day_start(dt):
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)

## Returns a dtnaive or dtawre (as parameter) with the end of the day in zone tz_name
def dtaware_day_start(dt, tz_name):
    """Returns a timezone-aware datetime object representing the start of the day for the given datetime in the specified timezone.

    Args:
        dt (datetime): A timezone-aware datetime object.
        tz_name (str): The name of the timezone.

    Returns:
        datetime: A timezone-aware datetime object set to 00:00:00.000000 of the same day in the specified timezone."""
def dtaware_day_start(dt, tz_name):
    if is_naive(dt):
        raise exceptions.CastException(_("A datetime with timezone is needed"))
    dt=dtaware_changes_tz(dt, tz_name)
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)

## Returns the end of the day dtnaive from a date
def dtnaive_day_start_from_date(date_):
    """Returns a timezone-naive datetime object representing the start of the day for a given date.

    Args:
        date_ (date): A `datetime.date` object.

    Returns:
        datetime: A timezone-naive datetime object set to 00:00:00.000000 of the given date.
    """
    dt=datetime(date_.year, date_.month, date_.day)
    return dtnaive_day_start(dt)

## Returns the end of the day dtaware of the tz_name timezone from a date
def dtaware_day_start_from_date(date, tz_name):
    """Returns a timezone-aware datetime object representing the start of the day for a given date and timezone.

    Args:
        date (date): A `datetime.date` object.
        tz_name (str): The name of the timezone.

    Returns:
        datetime: A timezone-aware datetime object set to 00:00:00.000000 of the given date in the specified timezone.
    """
    return dtaware(date, time(0, 0, 0, 0), tz_name)

## Returns the start of a month in utc format
def dtaware_month_start(year, month, tz_name):
    """Returns a timezone-aware datetime object representing the start of the specified month and year.

    Args:
        year (int): The year.
        month (int): The month (1-12).
        tz_name (str): The name of the timezone.

    Returns:
        datetime: A timezone-aware datetime object for the first day of the month, 00:00:00.000000.
    """
    return dtaware_day_start_from_date(date(year, month, 1), tz_name)


def str2time(value, format="JsIso", ignore_exception=False, ignore_exception_value=None):
    """Converts a string representation of time to a `datetime.time` object.

    Args:
        value (str): The string to convert.
        format (str, optional): The format of the input string. Allowed values:
                                "HH:MM", "HH:MM:SS", "HH:MMxx" (e.g., "5:12am"), "JsIso". Defaults to "JsIso".
        ignore_exception (bool, optional): If True, returns `ignore_exception_value` on error instead of raising an exception. Defaults to False.
        ignore_exception_value (any, optional): The value to return if an exception is ignored. Defaults to None.

    Returns:
        time: The converted `datetime.time` object.
    """
    original=value
    allowed=["HH:MM", "HH:MM:SS","JsIso","HH:MMxx"]
    error=f"Error in Pydicts.cast.str2time method. Value: {original} Value class: {value.__class__.__name__} Format: {format} Allowed: {allowed}"
    if format not in  allowed or value.__class__!=str:
        if ignore_exception is False:
            raise exceptions.CastException(error)
        else:
            return ignore_exception_value

    try:
        if format=="HH:MM":#12:12
            a=value.split(":")
            return time(int(a[0]), int(a[1]))
        elif format=="HH:MM:SS":#12:12:12
            a=value.split(":")
            return time(int(a[0]), int(a[1]), int(a[2]))
        elif format == "HH:MMxx":  # 5:12am or 5:12PM
            value_lower = value.lower()
            is_pm = False
            clean_value = value_lower

            if "pm" in value_lower:
                is_pm = True
                clean_value = value_lower.replace("pm", "")
            elif "am" in value_lower:
                is_pm = False
                clean_value = value_lower.replace("am", "")
            else:
                raise exceptions.CastException(f"Missing AM/PM indicator for HH:MMxx format: {value}")

            points = clean_value.split(":")
            h = int(points[0])
            m = int(points[1])

            if is_pm and h != 12:  # If PM and not 12 PM, add 12 hours
                h += 12
            elif not is_pm and h == 12:  # If AM and 12 AM, set hour to 0 (midnight)
                h = 0
            return time(h, m)
        elif format=="JsIso":#23:00:00.000000  
            if not ":" in value:
                raise exceptions.CastException(error)
            return time.fromisoformat(value)
    except:
        if ignore_exception is False:
            raise exceptions.CastException(error)
        else:
            return ignore_exception_value

## Converts a time to a string
def time2str(value, format="JsIso" , ignore_exception=False, ignore_exception_value=None):
    """Converts a `datetime.time` object to its string representation.

    Args:
        value (time): The `datetime.time` object to convert.
        format (str, optional): The desired output format. Allowed values:
                                "HH:MM", "HH:MM:SS", "Xulpymoney", "JsIso". Defaults to "JsIso".
        ignore_exception (bool, optional): If True, returns `ignore_exception_value` on error instead of raising an exception. Defaults to False.
        ignore_exception_value (any, optional): The value to return if an exception is ignored. Defaults to None.

    Returns:
        str: The string representation of the time.
    """
    original=value
    allowed=["HH:MM", "HH:MM:SS","Xulpymoney", "JsIso"]
    error=f"Error in Pydicts.cast.str2time method. Value: {original} Value class: {value.__class__.__name__} Format: {format} Allowed: {allowed}"
    if format not in  allowed or value.__class__!=time:
        if ignore_exception is False:
            raise exceptions.CastException(error)
        else:
            return ignore_exception_value

    try:
        if format=="Xulpymoney":
            return value.strftime("%H:%M:%S")
        elif format=="HH:MM":
            return ("{}:{}".format(str(value.hour).zfill(2), str(value.minute).zfill(2)))
        elif format=="HH:MM:SS":
            return ("{}:{}:{}".format(str(value.hour).zfill(2), str(value.minute).zfill(2), str(value.second).zfill(2)))
        elif format=="JsIso":
            return(str(value))
    except:
        if ignore_exception is False:
            raise exceptions.CastException(error)
        else:
            return ignore_exception_value


def str2date(value, format="YYYY-MM-DD", ignore_exception=False, ignore_exception_value=None):
    """Converts a string representation of a date to a `datetime.date` object.

    Args:
        value (str): The string to convert.
        format (str, optional): The format of the input string. Allowed values:
                                "YYYY-MM-DD", "DD/MM/YYYY", "DD.MM.YYYY", "DD/MM", "JsIso". Defaults to "YYYY-MM-DD".
        ignore_exception (bool, optional): If True, returns `ignore_exception_value` on error instead of raising an exception. Defaults to False.
        ignore_exception_value (any, optional): The value to return if an exception is ignored. Defaults to None.

    Returns:
        date: The converted `datetime.date` object.
    """
    original=value
    allowed=["YYYY-MM-DD", "DD/MM/YYYY", "DD.MM.YYYY", "DD/MM", "JsIso"]
    error=f"Error in Pydicts.cast.str2date method. Value: {original} Value class: {value.__class__.__name__} Format: {format} Allowed: {allowed}"
    if format not in  allowed or value.__class__!=str:
        if ignore_exception is False:
            raise exceptions.CastException(error)
        else:
            return ignore_exception_value

    try:
        if format in ["YYYY-MM-DD", "JsIso"]:
            d=value.split("-")
            return date(int(d[0]), int(d[1]),  int(d[2]))
        if format=="DD/MM/YYYY": #DD/MM/YYYY
            d=value.split("/")
            return date(int(d[2]), int(d[1]),  int(d[0]))
        if format=="DD.MM.YYYY": #DD.MM.YYYY
            d=value.split(".")
            return date(int(d[2]), int(d[1]),  int(d[0]))
        if format=="DD/MM": #DD/MM
            d=value.split("/")
            return date(date.today().year, int(d[1]),  int(d[0]))
    except:
        if ignore_exception is False:
            raise exceptions.CastException(error)
        else:
            return ignore_exception_value

def date2str(value, format="JsIso", ignore_exception=False, ignore_exception_value=None):
    """Converts a datetime.date object to its string representation.

    Args:
        value (date): The datetime.date object to convert.
        format (str, optional): The desired output format. Allowed values:
                                "JsIso" (YYYY-MM-DD), "DD/MM/YYYY", "DD.MM.YYYY",
                                "long string" (e.g., "January 15, 2023" or "15 de enero de 2023" based on locale).
                                Defaults to "JsIso".
        ignore_exception (bool, optional): If True, returns `ignore_exception_value` on error instead of raising an exception. Defaults to False.
        ignore_exception_value (any, optional): The value to return if an exception is ignored. Defaults to None.

    Returns:
        str: The string representation of the date.

    Note:
        The "long string" format is locale-dependent. It attempts to format the date
        in a human-readable way based on the system's current locale (e.g., English, Spanish).
        If the locale is not explicitly handled, it defaults to an English-like format.
    """
    original = value
    allowed = ["JsIso", "DD/MM/YYYY", "DD.MM.YYYY", "long string"]
    error = f"Error in Pydicts.cast.date2str method. Value: {original} Value class: {value.__class__.__name__} Format: {format} Allowed: {allowed}"

    if not isinstance(value, date) or format not in allowed:
        if ignore_exception:
            return ignore_exception_value
        raise exceptions.CastException(error)

    try:
        if format == "JsIso":
            return value.strftime("%Y-%m-%d")
        elif format == "DD/MM/YYYY":
            return value.strftime("%d/%m/%Y")
        elif format == "DD.MM.YYYY":
            return value.strftime("%d.%m.%Y")
        elif format == "long string":
            current_locale = get_locale()
            if current_locale and current_locale.startswith("es"):# Spanish format
                return f"{value.day} de {dict_month_names["es"][value.month].lower()} de {value.year}"
            else:
                # Default to English-like format
                return value.strftime("%B %d, %Y")
    except Exception: # Catch any potential strftime errors
        if ignore_exception:
            return ignore_exception_value
        raise exceptions.CastException(error)


def str2dtnaive(value, format="JsIso", ignore_exception=False, ignore_exception_value=None):
    """Converts a string representation of a datetime to a timezone-naive `datetime.datetime` object.

    Args:
        value (str): The string to convert.
        format (str, optional): The format of the input string. Allowed values:
                                "%Y%m%d%H%M", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M", "%d %m %H:%M %Y",
                                "%Y-%m-%d %H:%M:%S.", "%H:%M:%S",
                                '%b %d %H:%M:%S' (e.g., "Jan 15 10:30:00", locale-dependent month abbreviation),
                                "JsIso" (e.g., "2021-08-21T06:27:38.294").
                                Defaults to "JsIso".
        ignore_exception (bool, optional): If True, returns `ignore_exception_value` on error instead of raising an exception. Defaults to False.
        ignore_exception_value (any, optional): The value to return if an exception is ignored. Defaults to None.

    Returns:
        datetime: The converted timezone-naive `datetime.datetime` object.
    """
    original = value
    allowed = ["%Y%m%d%H%M", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M", "%d %m %H:%M %Y", "%Y-%m-%d %H:%M:%S.", "%H:%M:%S", '%b %d %H:%M:%S', "JsIso"]
    error=f"Error in Pydicts.cast.str2dtnaive method. Value: {original} Value class: {value.__class__.__name__} Format: {format} Allowed: {allowed}"
    if format not in  allowed or value.__class__!=str:
        if ignore_exception is False:
            raise exceptions.CastException(error)
        else:
            return ignore_exception_value

    try:
        if format=="%Y%m%d%H%M":
            dat=datetime.strptime( value, format )
            return dat
        if format=="%Y-%m-%d %H:%M:%S":#2017-11-20 23:00:00
            return datetime.strptime( value, format )
        if format=="%d/%m/%Y %H:%M":#20/11/2017 23:00
            return datetime.strptime( value, format )
        if format=="%d %m %H:%M %Y":#27 1 16:54 2017. 1 es el mes convertido con month2int
            return datetime.strptime( value, format)
        if format=="%Y-%m-%d %H:%M:%S.":#2017-11-20 23:00:00.000000  ==>  microsecond. Notice the point in format
            arrPunto=value.split(".")
            micro=int(arrPunto[1]) if len(arrPunto)==2 and arrPunto[1] else 0
            dt=datetime.strptime( arrPunto[0],  "%Y-%m-%d %H:%M:%S" )
            dt=dt+timedelta(microseconds=micro)
            return dt
        if format=="%H:%M:%S": 
            tod=date.today()
            a=value.split(":")
            return datetime(tod.year, tod.month, tod.day, int(a[0]), int(a[1]), int(a[2]))
        if format=='%b %d %H:%M:%S': #Apr 26 07:50:44. Year is missing so I set to current
            s=f"{date.today().year} {value}"
            return datetime.strptime(s, '%Y %b %d %H:%M:%S')
        if format=="JsIso": #2021-08-21T06:27:38.294
            # JsIso for naive datetime should not contain 'Z'
            if "Z" in value:
                raise exceptions.CastException(error)
            value=value.replace("T"," ")
            dtnaive=str2dtnaive(value,"%Y-%m-%d %H:%M:%S.")

            return dtnaive
    except:
        if ignore_exception is False:
            raise exceptions.CastException(error)
        else:
            return ignore_exception_value

def str2dtaware(value, format="JsUtcIso", tz_name='UTC', ignore_exception=False, ignore_exception_value=None):
    """Converts a string representation of a datetime to a timezone-aware `datetime.datetime` object.

    Args:
        value (str): The string to convert.
        format (str, optional): The format of the input string. Allowed values:
                                "%Y-%m-%d %H:%M:%S%z", "%Y-%m-%d %H:%M:%S.%z", "JsUtcIso". Defaults to "JsUtcIso".
        tz_name (str, optional): The target timezone name for the aware datetime. Defaults to 'UTC'.
        ignore_exception (bool, optional): If True, returns `ignore_exception_value` on error instead of raising an exception. Defaults to False.
        ignore_exception_value (any, optional): The value to return if an exception is ignored. Defaults to None.

    Returns:
        datetime: The converted timezone-aware `datetime.datetime` object.
    """
    original=value
    allowed=["%Y-%m-%d %H:%M:%S%z","%Y-%m-%d %H:%M:%S.%z", "JsUtcIso"]
    error=f"Error in Pydicts.cast.str2dtaware method. Value: {original} Value class: {value.__class__.__name__} Format: {format} Allowed: {allowed}"
    if format not in  allowed or value.__class__!=str:
        if ignore_exception is False:
            raise exceptions.CastException(error)
        else:
            return ignore_exception_value
    try:
        if format=="%Y-%m-%d %H:%M:%S%z":#2017-11-20 23:00:00+00:00
            dt=datetime.strptime( value, format )
            return dtaware_changes_tz(dt, tz_name)
        if format=="%Y-%m-%d %H:%M:%S.%z":#2017-11-20 23:00:00.000000+00:00  ==>  microsecond. Notice the point in format
            # datetime.strptime can handle %f for microseconds and %z for timezone offset directly
            # The input string "2023-01-15 10:30:00.123456+01:00" matches "%Y-%m-%d %H:%M:%S.%f%z"
            # No need for manual splitting and rejoining
            dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f%z")
            # dt = dt.replace(tzinfo=ZoneInfo(tz_name)) # This is handled by dtaware_changes_tz
            return dtaware_changes_tz(dt, tz_name)
        if format=="JsUtcIso": #2021-08-21T06:27:38.294Z
            if not "Z" in value:
                raise exceptions.CastException(error)
            # datetime.fromisoformat handles 'Z' and fractional seconds correctly
            dt_utc_aware = datetime.fromisoformat(value.replace('Z', '+00:00'))
            return dtaware_changes_tz(dt_utc_aware, tz_name)

    except:
        if ignore_exception is False:
            raise exceptions.CastException(error)
        else:
            return ignore_exception_value

## epoch is the time from 1,1,1970 in UTC
def dtaware2epochms(d: datetime):
    """Converts a timezone-aware datetime object to milliseconds since the Unix epoch (1970-01-01 UTC).

    Args:
        d (datetime): A timezone-aware datetime object.

    Returns:
        int: The number of milliseconds since epoch.
    """
    return int(d.timestamp() * 1000)
    
## Return a UTC datetime aware
def epochms2dtaware(n: int | float, tz="UTC"):
    """Converts milliseconds since the Unix epoch to a timezone-aware datetime object.

    Args:
        n (int | float): The number of milliseconds since epoch.
        tz (str, optional): The target timezone name. Defaults to "UTC".

    Returns:
        datetime: A timezone-aware datetime object.
    """
    utc_aware = datetime.fromtimestamp(n / 1000, ZoneInfo('UTC')) # Use timezone-aware fromtimestamp
    return dtaware_changes_tz(utc_aware, tz)

## epoch is the time from 1,1,1970 in UTC
def dtaware2epochmicros(d):
    """Converts a timezone-aware datetime object to microseconds since the Unix epoch (1970-01-01 UTC).

    Args:
        d (datetime): A timezone-aware datetime object.

    Returns:
        int: The number of microseconds since epoch.
    """
    return int(d.timestamp()*1000000)

## Return a UTC datetime aware
def epochmicros2dtaware(n, tz="UTC"):
    utc_aware = datetime.fromtimestamp(n / 1000000, ZoneInfo('UTC')) # Use timezone-aware fromtimestamp
    return dtaware_changes_tz(utc_aware, tz)

## Returns a formated string of a dtaware string formatting with a zone name
## @param dt datetime aware object
def dtaware2str(value, format="JsUtcIso", ignore_exception=False, ignore_exception_value=None):
    """Converts a timezone-aware datetime object to its string representation in a specified format.

    Args:
        value (datetime): A timezone-aware datetime object.
        format (str, optional): The desired output format. Allowed values:
                                "%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y%m%d %H%M", "%Y%m%d%H%M", "JsUtcIso",
                                "long string" (e.g., "January 15, 2023 at 10:30 UTC" or "15 de enero de 2023 a las 10:30 (UTC)" based on locale).
                                Defaults to "JsUtcIso".
        ignore_exception (bool, optional): If True, returns `ignore_exception_value` on error instead of raising an exception. Defaults to False.
        ignore_exception_value (any, optional): The value to return if an exception is ignored. Defaults to None.

    Returns:
        str: The string representation of the datetime.

    Note:
        The "long string" format is locale-dependent. It attempts to format the datetime
        in a human-readable way including the timezone name, based on the system's current locale.
        If the locale is not explicitly handled, it defaults to an English-like format.
    """
    original=value
    allowed=["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y%m%d %H%M", "%Y%m%d%H%M", "JsUtcIso", "long string"]
    error=f"Error in Pydicts.cast.dtaware2str method. Value: {original} Value class: {value.__class__.__name__} Format: {format} Allowed: {allowed}"
    
    if format not in  allowed or value.__class__!=datetime or is_naive(value):
        if ignore_exception is False:
            raise exceptions.CastException(error)
        else:
            return ignore_exception_value
    try:
        if format=="%Y-%m-%d":
            return value.strftime("%Y-%m-%d")
        elif format=="%Y-%m-%d %H:%M:%S": 
            return value.strftime("%Y-%m-%d %H:%M:%S")
        elif format=="%Y%m%d %H%M": 
            return value.strftime("%Y%m%d %H%M")
        elif format=="%Y%m%d%H%M":
            return value.strftime("%Y%m%d%H%M")
        elif format=="JsUtcIso":
            value=dtaware_changes_tz(value, "UTC")
            return value.isoformat().replace("+00:00","Z")
        elif format == "long string":
            current_locale = get_locale()
            if current_locale and current_locale.startswith("es"):
                return date2str(value.date(), format="long string", ignore_exception=ignore_exception, ignore_exception_value=ignore_exception_value) + " a las " + time2str(value.time(), "HH:MM", ignore_exception=ignore_exception, ignore_exception_value=ignore_exception_value) + " (" + value.tzinfo.tzname(value) +")"
            else:
                # Default to English-like format including timezone name
                return value.strftime("%B %d, %Y at %H:%M %Z")
    except:
        if ignore_exception is False:
            raise exceptions.CastException(error)
        else:
            return ignore_exception_value

## Returns a formated string of a dtaware string formatting with a zone name
def dtnaive2str(value, format="JsIso", ignore_exception=False, ignore_exception_value=None):
    """Converts a timezone-naive datetime object to its string representation in a specified format.

    Args:
        value (datetime): A timezone-naive datetime object.
        format (str, optional): The desired output format. Allowed values:
                                "%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y%m%d %H%M", "%Y%m%d%H%M", "JsIso",
                                "long string" (e.g., "January 15, 2023 at 10:30" or "15 de enero de 2023 a las 10:30" based on locale).
                                Defaults to "JsIso".
        ignore_exception (bool, optional): If True, returns `ignore_exception_value` on error instead of raising an exception. Defaults to False.
        ignore_exception_value (any, optional): The value to return if an exception is ignored. Defaults to None.

    Returns:
        str: The string representation of the datetime.

    Note:
        The "long string" format is locale-dependent. It attempts to format the datetime
        in a human-readable way based on the system's current locale.
        If the locale is not explicitly handled, it defaults to an English-like format.
    """
    original=value
    allowed=["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y%m%d %H%M", "%Y%m%d%H%M", "JsIso", "long string"]
    error=f"Error in Pydicts.cast.dtnaive2str method. Value: {original} Value class: {value.__class__.__name__} Format: {format} Allowed: {allowed}"
    if format not in  allowed or value.__class__!=datetime or is_aware(value):
        if ignore_exception is False:
            raise exceptions.CastException(error)
        else:
            return ignore_exception_value

    try:
        if format=="%Y-%m-%d":
            return value.strftime("%Y-%m-%d")
        elif format=="%Y-%m-%d %H:%M:%S": 
            return value.strftime("%Y-%m-%d %H:%M:%S")
        elif format=="%Y%m%d %H%M": 
            return value.strftime("%Y%m%d %H%M")
        elif format=="%Y%m%d%H%M":
            return value.strftime("%Y%m%d%H%M")
        elif format=="JsIso":
            return value.strftime("%Y-%m-%dT%H:%M:%S")+"."+str(value.microsecond).zfill(6)
        elif format == "long string":
            current_locale = get_locale()
            if current_locale and current_locale.startswith("es"):
                return date2str(value.date(), format="long string", ignore_exception=ignore_exception, ignore_exception_value=ignore_exception_value) + " a las " + time2str(value.time(), "HH:MM", ignore_exception=ignore_exception, ignore_exception_value=ignore_exception_value)
            else:
                return value.strftime("%B %d, %Y at %H:%M")
    except:
        if ignore_exception is False:
            raise exceptions.CastException(error)
        else:
            return ignore_exception_value

def dtaware_changes_tz(dt,  tzname):
    """Changes the timezone of a timezone-aware datetime object.

    Args:
        dt (datetime): A timezone-aware datetime object.
        tzname (str): The name of the target timezone (e.g., "Europe/Madrid").

    Returns:
        datetime: A new timezone-aware datetime object converted to the target timezone.

    Raises:
        exceptions.CastException: If the input datetime object is timezone-naive.

    Example:
        >>> dt_madrid = datetime(2018, 5, 18, 8, 12, tzinfo=ZoneInfo('Europe/Madrid'))
        >>> dtaware_changes_tz(dt_madrid, "Europe/London")
        datetime.datetime(2018, 5, 18, 7, 12, tzinfo=<DstTzInfo 'Europe/London' BST+1:00:00 DST>)
    """
    if dt==None:
        return None
    if is_aware(dt):
        return dt.astimezone(ZoneInfo(tzname))
    else:
        raise exceptions.CastException(_("A datetime with timezone is needed"))

def months(year_from, month_from, year_to=None, month_to=None):
    """Generates a list of (year, month) tuples for a range of months.

    Args:
        year_from (int): The starting year.
        month_from (int): The starting month (1-12).
        year_to (int, optional): The ending year. If None, uses the current year. Defaults to None.
        month_to (int, optional): The ending month (1-12). If None, uses the current month. Defaults to None.

    Returns:
        list: A list of (year, month) tuples, inclusive of the start and end months.
    """
    if year_to is None or month_to is None:
        year_to=date.today().year
        month_to=date.today().month
    r=[]
    end=date_first_of_the_month(year_to, month_to)
    current=date_first_of_the_month(year_from, month_from)
    while True:
        if current>end:
            break
        r.append((current.year,current.month))
        current=date_first_of_the_next_x_months(current.year, current.month, 1)
    return r
    
def timedelta2str(value, ignore_exception=False, ignore_exception_value=None):
    """Converts a `datetime.timedelta` object into an ISO 8601 duration string.

    Args:
        value (timedelta): The `datetime.timedelta` object to convert.
        ignore_exception (bool, optional): If True, returns `ignore_exception_value` on error instead of raising an exception. Defaults to False.
        ignore_exception_value (any, optional): The value to return if an exception is ignored. Defaults to None.

    Returns:
        str: The ISO 8601 duration string.

    Raises:
        exceptions.CastException: If `value` is not a `timedelta` object and `ignore_exception` is False.
    """
    original=value
    error=f"Error in Pydicts.cast.timedelta2str method. Value: {original} Value class: {value.__class__.__name__}"
    # Check ignore_exception first for type mismatches
    if not isinstance(value, timedelta):
        if ignore_exception: return ignore_exception_value
        raise exceptions.CastException(error)
    # is_noe is not appropriate for timedelta objects, as timedelta(0) is a valid value
    # and None is already handled by the isinstance check.
    try:
        return duration_isoformat(value)
    except:
        if ignore_exception is False:
            raise exceptions.CastException(error)
        else:
            return ignore_exception_value
    
def str2timedelta(value, ignore_exception=False, ignore_exception_value=None):
    """Converts an ISO 8601 duration string into a `datetime.timedelta` object.

    Args:
        value (str): The ISO 8601 duration string to convert.
        ignore_exception (bool, optional): If True, returns `ignore_exception_value` on error instead of raising an exception. Defaults to False.
        ignore_exception_value (any, optional): The value to return if an exception is ignored. Defaults to None.

    Returns:
        timedelta: The converted `datetime.timedelta` object.

    Raises:
        exceptions.CastException: If `value` is not a string, is empty, or is not a valid ISO 8601 duration string, and `ignore_exception` is False.
    """
    original=value
    error=f"Error in Pydicts.cast.str2timedelta method. Value: {original} Value class: {value.__class__.__name__}"
    # Check ignore_exception first for type mismatches
    if not isinstance(value, str):
        if ignore_exception: return ignore_exception_value
        raise exceptions.CastException(error)
    if is_noe(value): # Check for empty string after type check
        if ignore_exception: return ignore_exception_value
        raise exceptions.CastException(error)
    try:
        return parse_duration(value)
    except:
        if ignore_exception is False:
            raise exceptions.CastException(error)
        else:
            return ignore_exception_value

def is_email(value):
    """Checks if a string is a valid email address using a regular expression.

    Args:
        value (str): The string to validate.

    Returns:
        bool: True if the string is a valid email address, False otherwise.

    Note: This validation is based on a common regex pattern and might not cover all edge cases defined by RFCs.
    """
    if not value.__class__==str:
        return False

    if match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
        return True
    else:
        return False
    
