import pytest
import locale # Added for locale-dependent date formatting tests
from datetime import datetime, date, time, timedelta
from decimal import Decimal
from zoneinfo import ZoneInfo
from pydicts import exceptions, casts

def mock_get_locale_en():
    return "en_US.UTF-8"

def mock_get_locale_es():
    return "es_ES.UTF-8"

# Fixture to automatically mock get_locale for all tests in this module
@pytest.fixture(autouse=True)
def mock_get_locale_fixture(monkeypatch):
    # Default to English for most tests unless explicitly overridden
    monkeypatch.setattr(casts, 'get_locale', mock_get_locale_en)

# Test dtaware_now
def test_dtaware_now_utc():
    """Tests dtaware_now function for UTC timezone."""
    now_utc = casts.dtaware_now()
    assert casts.is_aware(now_utc)
    assert now_utc.tzinfo == ZoneInfo('UTC')
    # Check if it's close to the actual UTC time
    assert abs((datetime.now(ZoneInfo('UTC')) - now_utc).total_seconds()) < 1

def test_dtaware_now_specific_tz():
    """Tests dtaware_now function for a specific timezone."""
    tz_name = 'Europe/Madrid'
    now_madrid = casts.dtaware_now(tz_name)
    assert casts.is_aware(now_madrid)
    assert now_madrid.tzinfo == ZoneInfo(tz_name)
    # Check if it's close to the actual time in Madrid
    assert abs((datetime.now(ZoneInfo(tz_name)) - now_madrid).total_seconds()) < 1

# Test str2decimal
def test_str2decimal_success():
    """Tests successful string to Decimal conversion."""
    assert casts.str2decimal("123.45") == Decimal("123.45")
    assert casts.str2decimal("100") == Decimal("100")

def test_str2decimal_failure():
    """Tests failed string to Decimal conversion and exception handling."""

    with pytest.raises(exceptions.CastException):
        casts.str2decimal("abc")
    with pytest.raises(exceptions.CastException):
        casts.str2decimal(123)
    with pytest.raises(exceptions.CastException):
        casts.str2decimal(None)

def test_str2decimal_ignore_exception():
    """Tests string to Decimal conversion with exception ignoring."""
    assert casts.str2decimal("abc", ignore_exception=True, ignore_exception_value=0) == 0
    assert casts.str2decimal(123, ignore_exception=True, ignore_exception_value=None) is None

# Test str2bool
def test_str2bool_success():
    assert casts.str2bool("true") is True
    assert casts.str2bool("TRUE") is True
    assert casts.str2bool("1") is True
    assert casts.str2bool("false") is False
    assert casts.str2bool("FALSE") is False
    assert casts.str2bool("0") is False

def test_str2bool_failure():
    """Tests failed string to boolean conversion and exception handling."""
    with pytest.raises(exceptions.CastException):
        casts.str2bool("yes")
    with pytest.raises(exceptions.CastException):
        casts.str2bool(1)
    with pytest.raises(exceptions.CastException):
        casts.str2bool(None)

def test_str2bool_ignore_exception():
    assert casts.str2bool("yes", ignore_exception=True, ignore_exception_value=False) is False
    assert casts.str2bool(1, ignore_exception=True, ignore_exception_value=None) is None

# Test is_aware and is_naive
def test_is_aware_naive():
    naive_dt = datetime.now()
    aware_dt_utc = datetime.now(ZoneInfo('UTC'))
    aware_dt_madrid = datetime.now(ZoneInfo('Europe/Madrid'))

    assert casts.is_naive(naive_dt)
    assert not casts.is_aware(naive_dt)

    assert casts.is_aware(aware_dt_utc)
    assert not casts.is_naive(aware_dt_utc)

    assert casts.is_aware(aware_dt_madrid)
    assert not casts.is_naive(aware_dt_madrid)

# Test is_noe
def test_is_noe():
    assert casts.is_noe(None) is True
    assert casts.is_noe("") is True
    assert casts.is_noe(" ") is False
    assert casts.is_noe("hello") is False
    assert casts.is_noe(0) is False
    assert casts.is_noe([]) is False

# Test object_or_empty
def test_object_or_empty():
    assert casts.object_or_empty(None) == ""
    assert casts.object_or_empty("hello") == "hello"
    assert casts.object_or_empty(123) == 123
    assert casts.object_or_empty("") == ""

# Test none2alternative
def test_none2alternative():
    assert casts.none2alternative(None, "default") == "default"
    assert casts.none2alternative("value", "default") == "value"
    assert casts.none2alternative(0, "default") == 0

# Test bytes2str
def test_bytes2str_success():
    assert casts.bytes2str(b"hello") == "hello"
    assert casts.bytes2str(b"\xc3\xa1", code='utf-8') == "á"

def test_bytes2str_failure():
    with pytest.raises(exceptions.CastException):
        casts.bytes2str("hello") # Not bytes
    with pytest.raises(exceptions.CastException):
        casts.bytes2str(None)
    with pytest.raises(exceptions.CastException):
        casts.bytes2str(b"\xc3\xa1", code='ascii') # Decoding error

def test_bytes2str_ignore_exception():
    """Tests successful bytes to string conversion."""
    assert casts.bytes2str("hello", ignore_exception=True, ignore_exception_value="fail") == "fail"
    assert casts.bytes2str(b"\xc3\xa1", code='ascii', ignore_exception=True, ignore_exception_value="fail") == "fail"

# Test str2bytes
def test_str2bytes_success():
    assert casts.str2bytes("hello") == b"hello"
    assert casts.str2bytes("á", code='utf-8') == b"\xc3\xa1"

def test_str2bytes_failure():
    """Tests successful string to bytes conversion."""
    with pytest.raises(exceptions.CastException):
        casts.str2bytes(b"hello") # Not str
    with pytest.raises(exceptions.CastException):
        casts.str2bytes(None)
    with pytest.raises(exceptions.CastException):
        casts.str2bytes("á", code='ascii') # Encoding error

def test_str2bytes_ignore_exception():
    """Tests successful string to bytes conversion."""
    assert casts.str2bytes(b"hello", ignore_exception=True, ignore_exception_value=b"fail") == b"fail"
    assert casts.str2bytes("á", code='ascii', ignore_exception=True, ignore_exception_value=b"fail") == b"fail"

# Test base64bytes2bytes
def test_base64bytes2bytes_success():
    assert casts.base64bytes2bytes(b"aGVsbG8=") == b"hello"

def test_base64bytes2bytes_failure():
    """Tests successful base64 bytes to bytes decoding."""
    with pytest.raises(exceptions.CastException):
        casts.base64bytes2bytes(b"not-base64")
    with pytest.raises(exceptions.CastException):
        casts.base64bytes2bytes("aGVsbG8=") # Not bytes
    with pytest.raises(exceptions.CastException):
        casts.base64bytes2bytes(None)

def test_base64bytes2bytes_ignore_exception():
    """Tests failed base64 bytes to bytes decoding and exception handling."""
    assert casts.base64bytes2bytes(b"not-base64", ignore_exception=True, ignore_exception_value=b"fail") == b"fail"

# Test bytes2base64bytes
def test_bytes2base64bytes_success():
    assert casts.bytes2base64bytes(b"hello") == b"aGVsbG8="

def test_bytes2base64bytes_failure():
    """Tests successful bytes to base64 bytes encoding."""
    with pytest.raises(exceptions.CastException):
        casts.bytes2base64bytes("hello") # Not bytes
    with pytest.raises(exceptions.CastException):
        casts.bytes2base64bytes(None)

def test_bytes2base64bytes_ignore_exception():
    """Tests failed bytes to base64 bytes encoding and exception handling."""
    assert casts.bytes2base64bytes("hello", ignore_exception=True, ignore_exception_value=b"fail") == b"fail"


def test_dtnaive_now():
    """Tests the dtnaive_now function."""
    naive_dt = casts.dtnaive_now()
    assert casts.is_naive(naive_dt)
    assert abs((datetime.now() - naive_dt).total_seconds()) < 1

def test_dtnaive2dtaware():
    """Tests the dtnaive2dtaware function."""

    naive_dt = datetime(2023, 1, 1, 12, 0, 0)
    aware_dt = casts.dtnaive2dtaware(naive_dt, 'Europe/Madrid')
    assert casts.is_aware(aware_dt)
    assert aware_dt.tzinfo == ZoneInfo('Europe/Madrid')
    assert aware_dt.hour == 12
# Test dtaware2dtnaive
def test_dtaware2dtnaive():
    aware_dt = datetime(2023, 1, 1, 12, 0, 0, tzinfo=ZoneInfo('Europe/Madrid'))
    naive_dt = casts.dtaware2dtnaive(aware_dt)
    assert casts.is_naive(naive_dt)
    assert naive_dt.hour == 12
    assert naive_dt.tzinfo is None

    with pytest.raises(exceptions.CastException):
        casts.dtaware2dtnaive(datetime.now()) # Naive datetime

# Test dtaware
def test_dtaware():
    d = date(2023, 1, 1)
    t = time(10, 30, 0)
    aware_dt = casts.dtaware(d, t, 'Europe/Madrid')
    assert casts.is_aware(aware_dt)
    assert aware_dt.year == 2023
    assert aware_dt.month == 1
    assert aware_dt.day == 1
    assert aware_dt.hour == 10
    assert aware_dt.minute == 30
    assert aware_dt.second == 0
    assert aware_dt.tzinfo == ZoneInfo('Europe/Madrid')

# Test dtnaive
def test_dtnaive():
    d = date(2023, 1, 1)
    t = time(10, 30, 0, 123456) # type: ignore
    naive_dt = casts.dtnaive(d, t)
    assert casts.is_naive(naive_dt)
    assert naive_dt.year == 2023
    assert naive_dt.month == 1
    assert naive_dt.day == 1
    assert naive_dt.hour == 10
    assert naive_dt.minute == 30
    assert naive_dt.second == 0
    assert naive_dt.microsecond == 123456
    assert naive_dt.tzinfo is None

def test_date_first_of_the_month():
    """Tests the date_first_of_the_month function."""
    assert casts.date_first_of_the_month(2023, 5) == date(2023, 5, 1)


# Test date_last_of_the_month
def test_date_last_of_the_month():
    assert casts.date_last_of_the_month(2023, 1) == date(2023, 1, 31)
    assert casts.date_last_of_the_month(2023, 2) == date(2023, 2, 28)
    assert casts.date_last_of_the_month(2024, 2) == date(2024, 2, 29) # Leap year
    assert casts.date_last_of_the_month(2023, 12) == date(2023, 12, 31)

def test_date_first_of_the_year():
    """Tests the date_first_of_the_year function."""
    assert casts.date_first_of_the_year(2023) == date(2023, 1, 1)

# Test date_last_of_the_year
def test_date_last_of_the_year():
    assert casts.date_last_of_the_year(2023) == date(2023, 12, 31)

# Test date_first_of_the_next_x_months
def test_date_first_of_the_next_x_months():
    assert casts.date_first_of_the_next_x_months(2023, 1, 0) == date(2023, 1, 1)
    assert casts.date_first_of_the_next_x_months(2023, 1, 1) == date(2023, 2, 1)
    assert casts.date_first_of_the_next_x_months(2023, 1, 12) == date(2024, 1, 1)
    assert casts.date_first_of_the_next_x_months(2023, 3, -1) == date(2023, 2, 1)
    assert casts.date_first_of_the_next_x_months(2023, 1, -1) == date(2022, 12, 1)
    assert casts.date_first_of_the_next_x_months(2023, 1, -12) == date(2022, 1, 1)

# Test date_last_of_the_next_x_months
def test_date_last_of_the_next_x_months():
    assert casts.date_last_of_the_next_x_months(2023, 1, 0) == date(2023, 1, 31)
    assert casts.date_last_of_the_next_x_months(2023, 1, 1) == date(2023, 2, 28)
    assert casts.date_last_of_the_next_x_months(2023, 1, 12) == date(2024, 1, 31)
    assert casts.date_last_of_the_next_x_months(2023, 3, -1) == date(2023, 2, 28)
    assert casts.date_last_of_the_next_x_months(2023, 1, -1) == date(2022, 12, 31)

# Test dtaware_month_end
def test_dtaware_month_end():
    dt = casts.dtaware_month_end(2023, 1, 'UTC')
    assert dt.year == 2023
    assert dt.month == 1
    assert dt.day == 31
    assert dt.hour == 23
    assert dt.minute == 59
    assert dt.second == 59
    assert dt.microsecond == 999999
    assert dt.tzinfo == ZoneInfo('UTC')

# Test dtaware_year_start
def test_dtaware_year_start():
    dt = casts.dtaware_year_start(2023, 'UTC')
    assert dt.year == 2023
    assert dt.month == 1
    assert dt.day == 1
    assert dt.hour == 0
    assert dt.minute == 0
    assert dt.second == 0
    assert dt.microsecond == 0
    assert dt.tzinfo == ZoneInfo('UTC')

# Test dtaware_year_end
def test_dtaware_year_end():
    dt = casts.dtaware_year_end(2023, 'UTC')
    assert dt.year == 2023
    assert dt.month == 12
    assert dt.day == 31
    assert dt.hour == 23
    assert dt.minute == 59
    assert dt.second == 59
    assert dt.microsecond == 999999
    assert dt.tzinfo == ZoneInfo('UTC')

# Test dtaware_day_end
def test_dtaware_day_end():
    dt_utc = datetime(2023, 1, 1, 10, 0, 0, tzinfo=ZoneInfo('UTC'))
    end_of_day_utc = casts.dtaware_day_end(dt_utc, 'UTC')
    assert end_of_day_utc.hour == 23
    assert end_of_day_utc.minute == 59
    assert end_of_day_utc.second == 59
    assert end_of_day_utc.microsecond == 999999
    assert end_of_day_utc.tzinfo == ZoneInfo('UTC')

    dt_madrid = datetime(2023, 1, 1, 10, 0, 0, tzinfo=ZoneInfo('Europe/Madrid'))
    end_of_day_madrid = casts.dtaware_day_end(dt_madrid, 'Europe/Madrid')
    assert end_of_day_madrid.hour == 23
    assert end_of_day_madrid.minute == 59
    assert end_of_day_madrid.second == 59
    assert end_of_day_madrid.microsecond == 999999
    assert end_of_day_madrid.tzinfo == ZoneInfo('Europe/Madrid')

    with pytest.raises(exceptions.CastException):
        casts.dtaware_day_end(datetime.now(), 'UTC') # Naive datetime

# Test dtnaive_day_end
def test_dtnaive_day_end():
    naive_dt = datetime(2023, 1, 1, 10, 0, 0)
    end_of_day_naive = casts.dtnaive_day_end(naive_dt)
    assert end_of_day_naive.hour == 23
    assert end_of_day_naive.minute == 59
    assert end_of_day_naive.second == 59
    assert end_of_day_naive.microsecond == 999999
    assert casts.is_naive(end_of_day_naive)

    with pytest.raises(exceptions.CastException):
        casts.dtnaive_day_end(datetime.now(ZoneInfo('UTC'))) # Aware datetime

# Test dtnaive_day_end_from_date
def test_dtnaive_day_end_from_date():
    d = date(2023, 1, 1) # type: ignore
    end_of_day_naive = casts.dtnaive_day_end_from_date(d)
    assert end_of_day_naive.year == 2023
    assert end_of_day_naive.month == 1
    assert end_of_day_naive.day == 1
    assert end_of_day_naive.hour == 23
    assert end_of_day_naive.minute == 59
    assert end_of_day_naive.second == 59
    assert end_of_day_naive.microsecond == 999999
    assert casts.is_naive(end_of_day_naive)

# Test dtaware_day_end_from_date
def test_dtaware_day_end_from_date():
    d = date(2023, 1, 1) # type: ignore
    end_of_day_aware = casts.dtaware_day_end_from_date(d, 'Europe/Madrid')
    assert end_of_day_aware.year == 2023
    assert end_of_day_aware.month == 1
    assert end_of_day_aware.day == 1
    assert end_of_day_aware.hour == 23
    assert end_of_day_aware.minute == 59
    assert end_of_day_aware.second == 59
    assert end_of_day_aware.microsecond == 999999
    assert end_of_day_aware.tzinfo == ZoneInfo('Europe/Madrid')

# Test dtnaive_day_start
def test_dtnaive_day_start():
    naive_dt = datetime(2023, 1, 1, 10, 30, 45, 123456)
    start_of_day_naive = casts.dtnaive_day_start(naive_dt)
    assert start_of_day_naive.hour == 0
    assert start_of_day_naive.minute == 0
    assert start_of_day_naive.second == 0
    assert start_of_day_naive.microsecond == 0
    assert casts.is_naive(start_of_day_naive)

# Test dtaware_day_start
def test_dtaware_day_start():
    aware_dt = datetime(2023, 1, 1, 10, 30, 45, 123456, tzinfo=ZoneInfo('Europe/Madrid'))
    start_of_day_aware = casts.dtaware_day_start(aware_dt, 'Europe/Madrid')
    assert start_of_day_aware.hour == 0
    assert start_of_day_aware.minute == 0
    assert start_of_day_aware.second == 0
    assert start_of_day_aware.microsecond == 0
    assert start_of_day_aware.tzinfo == ZoneInfo('Europe/Madrid')

    with pytest.raises(exceptions.CastException):
        casts.dtaware_day_start(datetime.now(), 'UTC') # Naive datetime

# Test dtnaive_day_start_from_date
def test_dtnaive_day_start_from_date():
    d = date(2023, 1, 1) # type: ignore
    start_of_day_naive = casts.dtnaive_day_start_from_date(d)
    assert start_of_day_naive.year == 2023
    assert start_of_day_naive.month == 1
    assert start_of_day_naive.day == 1
    assert start_of_day_naive.hour == 0
    assert start_of_day_naive.minute == 0
    assert start_of_day_naive.second == 0
    assert start_of_day_naive.microsecond == 0
    assert casts.is_naive(start_of_day_naive)

# Test dtaware_day_start_from_date
def test_dtaware_day_start_from_date():
    d = date(2023, 1, 1) # type: ignore
    start_of_day_aware = casts.dtaware_day_start_from_date(d, 'Europe/Madrid')
    assert start_of_day_aware.year == 2023
    assert start_of_day_aware.month == 1
    assert start_of_day_aware.day == 1
    assert start_of_day_aware.hour == 0
    assert start_of_day_aware.minute == 0
    assert start_of_day_aware.second == 0
    assert start_of_day_aware.microsecond == 0
    assert start_of_day_aware.tzinfo == ZoneInfo('Europe/Madrid')

# Test dtaware_month_start
def test_dtaware_month_start():
    dt = casts.dtaware_month_start(2023, 5, 'UTC')
    assert dt.year == 2023
    assert dt.month == 5
    assert dt.day == 1
    assert dt.hour == 0
    assert dt.minute == 0
    assert dt.second == 0
    assert dt.microsecond == 0
    assert dt.tzinfo == ZoneInfo('UTC')

# Test str2time
def test_str2time_success():
    assert casts.str2time("12:34", format="HH:MM") == time(12, 34)
    assert casts.str2time("12:34:56", format="HH:MM:SS") == time(12, 34, 56)
    assert casts.str2time("5:12am", format="HH:MMxx") == time(5, 12)
    assert casts.str2time("5:12PM", format="HH:MMxx") == time(17, 12)
    assert casts.str2time("23:00:00.123456", format="JsIso") == time(23, 0, 0, 123456)
    assert casts.str2time("23:00:00", format="JsIso") == time(23, 0, 0)

def test_str2time_failure():
    """Tests failed string to time conversion and exception handling."""
    with pytest.raises(exceptions.CastException):
        casts.str2time("invalid", format="HH:MM")
    with pytest.raises(exceptions.CastException):
        casts.str2time("12:34", format="invalid_format")
    with pytest.raises(exceptions.CastException):
        casts.str2time(123, format="HH:MM")
    # The previous assertion for "23:00" was removed because time.fromisoformat accepts it.

def test_str2time_ignore_exception():
    """Tests failed string to time conversion and exception handling."""
    assert casts.str2time("invalid", format="HH:MM", ignore_exception=True, ignore_exception_value=None) is None
    assert casts.str2time(123, format="HH:MM", ignore_exception=True, ignore_exception_value=time(0,0)) == time(0,0)

# Test time2str
def test_time2str_success():
    t = time(12, 34, 56, 123456)
    assert casts.time2str(t, format="Xulpymoney") == "12:34:56" # Assuming microsecond not 4 or 5
    t_ms_4 = time(12, 34, 56, 4)
    assert casts.time2str(t_ms_4, format="Xulpymoney") == "12:34:56"
    t_ms_5 = time(12, 34, 56, 5)
    assert casts.time2str(t_ms_5, format="Xulpymoney") == "12:34:56"
    assert casts.time2str(time(12, 34), format="HH:MM") == "12:34"
    assert casts.time2str(time(1, 2, 3), format="HH:MM:SS") == "01:02:03"
    assert casts.time2str(time(12, 34, 56, 123456), format="JsIso") == "12:34:56.123456"

def test_time2str_failure():
    """Tests successful time to string conversion."""
    with pytest.raises(exceptions.CastException):
        casts.time2str(datetime.now(), format="HH:MM") # Not time
    with pytest.raises(exceptions.CastException):
        casts.time2str(time(12, 0), format="invalid_format")
    with pytest.raises(exceptions.CastException):
        casts.time2str(None, format="HH:MM")

def test_time2str_ignore_exception():
    """Tests failed time to string conversion and exception handling."""
    assert casts.time2str(datetime.now(), format="HH:MM", ignore_exception=True, ignore_exception_value="fail") == "fail"

# Test str2date
def test_str2date_success():
    assert casts.str2date("2023-01-15", format="YYYY-MM-DD") == date(2023, 1, 15)
    assert casts.str2date("2023-01-15", format="JsIso") == date(2023, 1, 15)
    assert casts.str2date("15/01/2023", format="DD/MM/YYYY") == date(2023, 1, 15)
    assert casts.str2date("15.01.2023", format="DD.MM.YYYY") == date(2023, 1, 15)
    today_year = date.today().year
    assert casts.str2date("15/01", format="DD/MM") == date(today_year, 1, 15)

def test_str2date_failure():
    """Tests successful string to date conversion."""
    with pytest.raises(exceptions.CastException):
        casts.str2date("invalid", format="YYYY-MM-DD")
    with pytest.raises(exceptions.CastException):
        casts.str2date("2023-01-15", format="invalid_format")
    with pytest.raises(exceptions.CastException):
        casts.str2date(123, format="YYYY-MM-DD")

def test_str2date_ignore_exception():
    """Tests failed string to date conversion and exception handling."""
    assert casts.str2date("invalid", format="YYYY-MM-DD", ignore_exception=True, ignore_exception_value=None) is None

# Test str2dtnaive

def test_date2str_localization_with_system_locale(monkeypatch):
    """
    Tests date2str with 'long date str' format by explicitly setting a system locale.
    WARNING: Changing the global locale can have side effects and is generally
    not recommended within library functions. This test demonstrates how strftime
    behaves when the system locale is set.
    """
    monkeypatch.setattr(casts, 'get_locale', mock_get_locale_es)
    test_date = date(2023, 1, 15) # type: ignore
    original_locale = locale.getlocale(locale.LC_TIME) # Save current locale

    try:
        # Try to set a Spanish locale. This might fail on some systems.
        try:
            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        except locale.Error: # type: ignore
            pytest.skip("Spanish locale not available on this system for testing strftime localization.")

        assert casts.date2str(test_date, format="long string") == "15 de enero de 2023"
    finally:
        locale.setlocale(locale.LC_TIME, original_locale) # Always restore the original locale

# Test date2str
def test_date2str_success():
    """Tests successful date to string conversion."""
    test_date = date(2023, 1, 15) # type: ignore
    assert casts.date2str(test_date, format="JsIso") == "2023-01-15"
    assert casts.date2str(test_date, format="DD/MM/YYYY") == "15/01/2023"
    assert casts.date2str(test_date, format="DD.MM.YYYY") == "15.01.2023"

    # Test 'long string' with explicit English locale for robustness
    original_locale = locale.getlocale()
    try:
        # Try to set an English locale. This might fail on some systems.
        try:
            locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
        except locale.Error: # type: ignore
            pytest.skip("English locale not available on this system for testing strftime localization.")
        assert casts.date2str(test_date, format="long string") == "January 15, 2023"
    finally:
        locale.setlocale(locale.LC_TIME, original_locale) # Always restore the original locale

def test_date2str_failure():
    """Tests failed date to string conversion and exception handling."""
    test_date = date(2023, 1, 15) # type: ignore
    with pytest.raises(exceptions.CastException):
        casts.date2str("not a date", format="JsIso") # Not a date object
    with pytest.raises(exceptions.CastException):
        casts.date2str(test_date, format="invalid_format") # Invalid format
    with pytest.raises(exceptions.CastException):
        casts.date2str(None, format="JsIso") # None value

def test_date2str_ignore_exception():
    """Tests date to string conversion with exception ignoring."""
    test_date = date(2023, 1, 15) # type: ignore
    assert casts.date2str("not a date", ignore_exception=True, ignore_exception_value="fail") == "fail"
    assert casts.date2str(test_date, format="invalid_format", ignore_exception=True, ignore_exception_value=None) is None
    assert casts.date2str(None, ignore_exception=True, ignore_exception_value="") == ""

def test_str2dtnaive_success():
    assert casts.str2dtnaive("202301151030", format="%Y%m%d%H%M") == datetime(2023, 1, 15, 10, 30)
    assert casts.str2dtnaive("2023-01-15 10:30:00", format="%Y-%m-%d %H:%M:%S") == datetime(2023, 1, 15, 10, 30, 0)
    assert casts.str2dtnaive("15/01/2023 10:30", format="%d/%m/%Y %H:%M") == datetime(2023, 1, 15, 10, 30)
    assert casts.str2dtnaive("15 01 10:30 2023", format="%d %m %H:%M %Y") == datetime(2023, 1, 15, 10, 30)
    assert casts.str2dtnaive("2023-01-15 10:30:00.123456", format="%Y-%m-%d %H:%M:%S.") == datetime(2023, 1, 15, 10, 30, 0, 123456)
    assert casts.str2dtnaive("2023-01-15 10:30:00.", format="%Y-%m-%d %H:%M:%S.") == datetime(2023, 1, 15, 10, 30, 0, 0)
    today = date.today()
    assert casts.str2dtnaive("10:30:00", format="%H:%M:%S") == datetime(today.year, today.month, today.day, 10, 30, 0)
    assert casts.str2dtnaive("2023-01-15T10:30:00.123456", format="JsIso") == datetime(2023, 1, 15, 10, 30, 0, 123456)
    assert casts.str2dtnaive("2023-01-15T10:30:00", format="JsIso") == datetime(2023, 1, 15, 10, 30, 0, 0) # This assertion was moved outside the locale block

    # Test locale-dependent month abbreviation parsing for str2dtnaive
    original_locale = locale.getlocale(locale.LC_TIME)
    try:
        try:
            locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
        except locale.Error: # type: ignore
            pytest.skip("English locale not available on this system for testing strptime localization.")
        assert casts.str2dtnaive("Jan 15 10:30:00", format="%b %d %H:%M:%S") == datetime(date.today().year, 1, 15, 10, 30, 0)
    finally:
        locale.setlocale(locale.LC_TIME, original_locale)

def test_str2dtnaive_failure():
    """Tests successful string to naive datetime conversion."""
    with pytest.raises(exceptions.CastException):
        casts.str2dtnaive("invalid", format="%Y%m%d%H%M")
    with pytest.raises(exceptions.CastException):
        casts.str2dtnaive("202301151030", format="invalid_format")
    with pytest.raises(exceptions.CastException):
        casts.str2dtnaive(123, format="%Y%m%d%H%M")
    with pytest.raises(exceptions.CastException):
        casts.str2dtnaive("2023-01-15T10:30:00.123Z", format="JsIso") # Contains Z

def test_str2dtnaive_ignore_exception():
    """Tests failed string to naive datetime conversion and exception handling."""
    assert casts.str2dtnaive("invalid", format="%Y%m%d%H%M", ignore_exception=True, ignore_exception_value=None) is None

# Test str2dtaware
def test_str2dtaware_success():
    dt_str_with_tz = "2023-01-15 10:30:00+01:00"
    dt_aware = casts.str2dtaware(dt_str_with_tz, format="%Y-%m-%d %H:%M:%S%z", tz_name='Europe/Madrid')
    assert dt_aware.year == 2023
    assert dt_aware.month == 1
    assert dt_aware.day == 15
    assert dt_aware.hour == 10 # Local time in Madrid
    assert dt_aware.tzinfo == ZoneInfo('Europe/Madrid')

    dt_str_with_tz_ms = "2023-01-15 10:30:00.123456+01:00"
    dt_aware_ms = casts.str2dtaware(dt_str_with_tz_ms, format="%Y-%m-%d %H:%M:%S.%z", tz_name='Europe/Madrid')
    assert dt_aware_ms.microsecond == 123456
    assert dt_aware_ms.tzinfo == ZoneInfo('Europe/Madrid')

    dt_js_utc_iso = "2023-01-15T10:30:00.123Z"
    dt_aware_js_utc = casts.str2dtaware(dt_js_utc_iso, format="JsUtcIso", tz_name='UTC')
    assert dt_aware_js_utc.year == 2023
    assert dt_aware_js_utc.month == 1
    assert dt_aware_js_utc.day == 15
    assert dt_aware_js_utc.hour == 10 # UTC hour
    assert dt_aware_js_utc.microsecond == 123000 # JsUtcIso format has 3 digits for ms, so it's 123 milliseconds = 123000 microseconds
    assert dt_aware_js_utc.tzinfo == ZoneInfo('UTC')

    dt_aware_js_madrid = casts.str2dtaware(dt_js_utc_iso, format="JsUtcIso", tz_name='Europe/Madrid')
    assert dt_aware_js_madrid.tzinfo == ZoneInfo('Europe/Madrid')
    # Check conversion from UTC 10:30 to Madrid time (UTC+1)
    assert dt_aware_js_madrid.hour == 11 # 10:30 UTC is 11:30 in Madrid (if no DST, but for Jan 15, it's UTC+1)
    assert dt_aware_js_madrid.minute == 30

def test_str2dtaware_failure():
    """Tests successful string to aware datetime conversion."""
    with pytest.raises(exceptions.CastException):
        casts.str2dtaware("invalid", format="%Y-%m-%d %H:%M:%S%z")
    with pytest.raises(exceptions.CastException):
        casts.str2dtaware("2023-01-15 10:30:00+01:00", format="invalid_format")
    with pytest.raises(exceptions.CastException):
        casts.str2dtaware(123, format="%Y-%m-%d %H:%M:%S%z")
    with pytest.raises(exceptions.CastException):
        casts.str2dtaware("2023-01-15T10:30:00.123", format="JsUtcIso") # Missing Z

def test_str2dtaware_ignore_exception():
    """Tests failed string to aware datetime conversion and exception handling."""
    assert casts.str2dtaware("invalid", format="%Y-%m-%d %H:%M:%S%z", ignore_exception=True, ignore_exception_value=None) is None

# Test dtaware2epochms
def test_dtaware2epochms():
    dt_utc = datetime(1970, 1, 1, 0, 0, 1, 500000, tzinfo=ZoneInfo('UTC')) # 1.5 seconds after epoch
    assert casts.dtaware2epochms(dt_utc) == 1500

# Test epochms2dtaware
def test_epochms2dtaware():
    epoch_ms = 1500
    dt_aware = casts.epochms2dtaware(epoch_ms, tz="UTC")
    assert dt_aware == datetime(1970, 1, 1, 0, 0, 1, 500000, tzinfo=ZoneInfo('UTC'))

    dt_aware_madrid = casts.epochms2dtaware(epoch_ms, tz="Europe/Madrid")
    # 1.5s UTC is 1.5s UTC+1 in Madrid, so 01:00:01.500000
    assert dt_aware_madrid == datetime(1970, 1, 1, 1, 0, 1, 500000, tzinfo=ZoneInfo('Europe/Madrid'))

# Test epochmicros2dtaware
def test_epochmicros2dtaware():
    epoch_micros = 1500000
    dt_aware = casts.epochmicros2dtaware(epoch_micros, tz="UTC")
    assert dt_aware == datetime(1970, 1, 1, 0, 0, 1, 500000, tzinfo=ZoneInfo('UTC'))

def test_dtaware2epochmicros():
    """Tests dtaware2epochmicros function."""   
    dt_utc = datetime(1970, 1, 1, 0, 0, 1, 500000, tzinfo=ZoneInfo('UTC')) # 1.5 seconds after epoch
    assert casts.dtaware2epochmicros(dt_utc) == 1500000


# Test dtaware2str
def test_dtaware2str_success():
    dt_utc = datetime(2023, 1, 15, 10, 30, 0, tzinfo=ZoneInfo('UTC'))
    dt_madrid = datetime(2023, 1, 15, 10, 30, 0, tzinfo=ZoneInfo('Europe/Madrid')) # 10:30 local Madrid time

    assert casts.dtaware2str(dt_utc, format="%Y-%m-%d") == "2023-01-15"
    assert casts.dtaware2str(dt_utc, format="%Y-%m-%d %H:%M:%S") == "2023-01-15 10:30:00"
    assert casts.dtaware2str(dt_utc, format="%Y%m%d %H%M") == "20230115 1030"
    assert casts.dtaware2str(dt_utc, format="%Y%m%d%H%M") == "202301151030"
    assert casts.dtaware2str(dt_utc, format="JsUtcIso") == "2023-01-15T10:30:00Z"

    # Test with a different timezone, JsUtcIso should convert to UTC
    assert casts.dtaware2str(dt_madrid, format="JsUtcIso") == "2023-01-15T09:30:00Z" # Madrid 10:30 is UTC 09:30

def test_dtaware2str_failure():
    """Tests epochmicros2dtaware function."""
    with pytest.raises(exceptions.CastException):
        casts.dtaware2str(datetime.now(), format="%Y-%m-%d") # Naive
    with pytest.raises(exceptions.CastException):
        casts.dtaware2str(datetime.now(ZoneInfo('UTC')), format="invalid_format")
    with pytest.raises(exceptions.CastException):
        casts.dtaware2str(None, format="%Y-%m-%d")

def test_dtaware2str_ignore_exception():
    """Tests successful aware datetime to string conversion."""
    assert casts.dtaware2str(datetime.now(), format="%Y-%m-%d", ignore_exception=True, ignore_exception_value="fail") == "fail"

# Test dtnaive2str
def test_dtnaive2str_success():
    dt_naive = datetime(2023, 1, 15, 10, 30, 0, 123456)

    assert casts.dtnaive2str(dt_naive, format="%Y-%m-%d") == "2023-01-15"
    assert casts.dtnaive2str(dt_naive, format="%Y-%m-%d %H:%M:%S") == "2023-01-15 10:30:00"
    assert casts.dtnaive2str(dt_naive, format="%Y%m%d %H%M") == "20230115 1030"
    assert casts.dtnaive2str(dt_naive, format="%Y%m%d%H%M") == "202301151030"
    assert casts.dtnaive2str(dt_naive, format="JsIso") == "2023-01-15T10:30:00.123456"

def test_dtnaive2str_failure():
    """Tests failed aware datetime to string conversion and exception handling."""
    with pytest.raises(exceptions.CastException):
        casts.dtnaive2str(datetime.now(ZoneInfo('UTC')), format="%Y-%m-%d") # Aware
    with pytest.raises(exceptions.CastException):
        casts.dtnaive2str(datetime.now(), format="invalid_format")
    with pytest.raises(exceptions.CastException):
        casts.dtnaive2str(None, format="%Y-%m-%d")

def test_dtnaive2str_ignore_exception():
    """Tests aware datetime to string conversion with exception ignoring."""
    assert casts.dtnaive2str(datetime.now(ZoneInfo('UTC')), format="%Y-%m-%d", ignore_exception=True, ignore_exception_value="fail") == "fail"

# Test dtnaive2str with "long string" format
def test_dtnaive2str_long_string_success(monkeypatch):
    test_dt_naive = datetime(2023, 1, 15, 10, 30, 0)
    original_locale = locale.getlocale()
    try:
        # Test English locale
        try:
            locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
        except locale.Error: # type: ignore
            pytest.skip("English locale not available on this system for testing strftime localization.")
        assert casts.dtnaive2str(test_dt_naive, format="long string") == "January 15, 2023 at 10:30"
    
        # Test Spanish locale
        try:
            monkeypatch.setattr(casts, 'get_locale', mock_get_locale_es)
            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        except locale.Error: # type: ignore
            pytest.skip("Spanish locale not available on this system for testing strftime localization.")
        assert casts.dtnaive2str(test_dt_naive, format="long string") == "15 de enero de 2023 a las 10:30"
    finally:
        locale.setlocale(locale.LC_TIME, original_locale)

# Test dtaware2str with "long string" format
def test_dtaware2str_long_string_success(monkeypatch):
    test_dt_aware = datetime(2023, 1, 15, 10, 30, 0, tzinfo=ZoneInfo('UTC'))
    test_dt_aware_madrid = datetime(2023, 1, 15, 10, 30, 0, tzinfo=ZoneInfo('Europe/Madrid')) # type: ignore
    original_locale = locale.getlocale()
    try:
        # Test English locale
        try:
            locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
        except locale.Error: # type: ignore
            pytest.skip("English locale not available on this system for testing strftime localization.")
        assert casts.dtaware2str(test_dt_aware, format="long string") == "January 15, 2023 at 10:30 UTC"
    
        # Test Spanish locale
        try:
            monkeypatch.setattr(casts, 'get_locale', mock_get_locale_es)
            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        except locale.Error: # type: ignore
            pytest.skip("Spanish locale not available on this system for testing strftime localization.")
        assert casts.dtaware2str(test_dt_aware, format="long string") == "15 de enero de 2023 a las 10:30 (UTC)"
        assert casts.dtaware2str(test_dt_aware_madrid, format="long string") == "15 de enero de 2023 a las 10:30 (CET)"
    finally:
        locale.setlocale(locale.LC_TIME, original_locale)

# Test dtaware_changes_tz
def test_dtaware_changes_tz():
    dt_utc = datetime(2023, 1, 15, 10, 0, 0, tzinfo=ZoneInfo('UTC'))
    dt_madrid = casts.dtaware_changes_tz(dt_utc, 'Europe/Madrid')
    assert dt_madrid.tzinfo == ZoneInfo('Europe/Madrid')
    assert dt_madrid.hour == 11 # UTC 10:00 is Madrid 11:00 (Jan 15)

    dt_madrid_to_london = casts.dtaware_changes_tz(dt_madrid, 'Europe/London')
    assert dt_madrid_to_london.tzinfo == ZoneInfo('Europe/London')
    assert dt_madrid_to_london.hour == 10 # Madrid 11:00 is London 10:00 (Jan 15)

    assert casts.dtaware_changes_tz(None, 'UTC') is None

    with pytest.raises(exceptions.CastException):
        casts.dtaware_changes_tz(datetime.now(), 'UTC') # Naive datetime

# Test months
def test_months():
    # Test current year/month
    today = date.today()
    expected_months = []
    current = casts.date_first_of_the_month(2023, 1)
    end = casts.date_first_of_the_month(today.year, today.month)
    while current <= end:
        expected_months.append((current.year, current.month))
        if current.month == 12:
            current = date(current.year + 1, 1, 1)
        else:
            current = date(current.year, current.month + 1, 1) # type: ignore

    # Test with explicit to_year and to_month
    assert casts.months(2023, 1, 2023, 3) == [(2023, 1), (2023, 2), (2023, 3)]
    assert casts.months(2023, 11, 2024, 1) == [(2023, 11), (2023, 12), (2024, 1)]
    assert casts.months(2023, 5, 2023, 5) == [(2023, 5)]
    assert casts.months(2023, 5, 2023, 4) == [] # From after to

# Test timedelta2str
def test_timedelta2str_success():
    td = timedelta(days=1, hours=2, minutes=3, seconds=4, microseconds=500000)
    assert casts.timedelta2str(td) == "P1DT2H3M4.5S"

def test_timedelta2str_failure():
    with pytest.raises(exceptions.CastException): # Not a timedelta object
        casts.timedelta2str("not a timedelta")
    with pytest.raises(exceptions.CastException): # None is not a timedelta
        casts.timedelta2str(None) 
def test_timedelta2str_ignore_exception():
    """Tests naive datetime to string conversion with exception ignoring."""
    assert casts.timedelta2str("not a timedelta", ignore_exception=True, ignore_exception_value=None) is None

def test_timedelta2str_zero():
    td = timedelta(0)
    assert casts.timedelta2str(td) == "P0D"


def test_timedelta2str_only_days():
    td = timedelta(days=5)
    assert casts.timedelta2str(td) == "P5D"


def test_timedelta2str_only_hours():
    td = timedelta(hours=10)
    assert casts.timedelta2str(td) == "PT10H"

def test_timedelta2str_only_seconds():
    td = timedelta(seconds=30)
    assert casts.timedelta2str(td) == "PT30S"


def test_str2timedelta_success():
    assert casts.str2timedelta("P1DT2H3M4.5S") == timedelta(days=1, hours=2, minutes=3, seconds=4, microseconds=500000)
    assert casts.str2timedelta("PT1H") == timedelta(hours=1)

def test_str2timedelta_failure():
    with pytest.raises(exceptions.CastException):
        casts.str2timedelta("invalid iso duration")
    with pytest.raises(exceptions.CastException):
        casts.str2timedelta(123)
    with pytest.raises(exceptions.CastException):
        casts.str2timedelta(None)

def test_str2timedelta_ignore_exception():
    """Tests the dtaware_changes_tz function."""
    assert casts.str2timedelta("invalid iso duration", ignore_exception=True, ignore_exception_value=None) is None

# Test is_email
def test_is_email():
    assert casts.is_email("test@example.com") is True
    assert casts.is_email("first.last@sub.domain.co.uk") is True
    assert casts.is_email("user123@domain-name.com") is True
    assert casts.is_email("user+tag@example.com") is True
    assert casts.is_email("invalid-email") is False
    assert casts.is_email("invalid@.com") is False
    assert casts.is_email("@example.com") is False
    assert casts.is_email("test@example") is False
    assert casts.is_email(None) is False
    assert casts.is_email(123) is False


def test_timedelta2str_fractional_seconds():
    td = timedelta(seconds=1, microseconds=123456)
    assert casts.timedelta2str(td) == "PT1.123456S"

def test_timedelta2str_negative_timedelta():
    td = timedelta(days=-1, hours=-5)
    assert casts.timedelta2str(td) == "-P1DT5H"

def test_timedelta2str_invalid_input():
    with pytest.raises(exceptions.CastException):
        casts.timedelta2str("not a timedelta")

def test_timedelta2str_ignore_exception():
    assert casts.timedelta2str("not a timedelta", ignore_exception=True, ignore_exception_value="ERROR") == "ERROR"

def test_str2timedelta_basic():
    s = "P1DT2H3M4.5S"
    td = timedelta(days=1, hours=2, minutes=3, seconds=4, microseconds=500000)
    assert casts.str2timedelta(s) == td

def test_str2timedelta_zero():
    s = "PT0S"
    td = timedelta(0)
    assert casts.str2timedelta(s) == td

def test_str2timedelta_only_days():
    s = "P5D"
    td = timedelta(days=5)
    assert casts.str2timedelta(s) == td

def test_str2timedelta_only_hours():
    s = "PT10H"
    td = timedelta(hours=10)
    assert casts.str2timedelta(s) == td

def test_str2timedelta_only_seconds():
    s = "PT30S"
    td = timedelta(seconds=30)
    assert casts.str2timedelta(s) == td

def test_str2timedelta_fractional_seconds():
    s = "PT1.123456S"
    td = timedelta(seconds=1, microseconds=123456)
    assert casts.str2timedelta(s) == td

def test_str2timedelta_negative_duration():
    s = "-P1DT5H"
    td = timedelta(days=-1, hours=-5)
    assert casts.str2timedelta(s) == td

def test_str2timedelta_invalid_string():
    with pytest.raises(exceptions.CastException):
        casts.str2timedelta("not a duration string")

def test_str2timedelta_empty_string():
    with pytest.raises(exceptions.CastException):
        casts.str2timedelta("")

def test_str2timedelta_invalid_input_type():
    with pytest.raises(exceptions.CastException):
        casts.str2timedelta(123)

def test_str2timedelta_ignore_exception():
    assert casts.str2timedelta("invalid", ignore_exception=True, ignore_exception_value=None) is None
    assert casts.str2timedelta(123, ignore_exception=True, ignore_exception_value="ERROR") == "ERROR"

# --- Tests for 'long string' format in date2str, dtaware2str, dtnaive2str ---

def test_date2str_long_string_en():
    d = date(2023, 1, 15)
    assert casts.date2str(d, format="long string") == "January 15, 2023"

def test_date2str_long_string_es(monkeypatch):
    monkeypatch.setattr(casts, 'get_locale', mock_get_locale_es)
    d = date(2023, 1, 15)
    assert casts.date2str(d, format="long string") == "15 de enero de 2023"

def test_dtnaive2str_long_string_en(monkeypatch):
    monkeypatch.setattr(casts, 'get_locale', mock_get_locale_en)
    dt = datetime(2023, 1, 15, 10, 30, 0)
    assert casts.dtnaive2str(dt, format="long string") == "January 15, 2023 at 10:30"

def test_dtnaive2str_long_string_es(monkeypatch):
    monkeypatch.setattr(casts, 'get_locale', mock_get_locale_es)
    dt = datetime(2023, 1, 15, 10, 30, 0)
    assert casts.dtnaive2str(dt, format="long string") == "15 de enero de 2023 a las 10:30"

def test_dtaware2str_long_string_en(monkeypatch):
    monkeypatch.setattr(casts, 'get_locale', mock_get_locale_en)
    dt = datetime(2023, 1, 15, 10, 30, 0, tzinfo=ZoneInfo('UTC'))
    assert casts.dtaware2str(dt, format="long string") == "January 15, 2023 at 10:30 UTC"

def test_dtaware2str_long_string_es(monkeypatch):
    monkeypatch.setattr(casts, 'get_locale', mock_get_locale_es)
    dt = datetime(2023, 1, 15, 10, 30, 0, tzinfo=ZoneInfo('Europe/Madrid'))
    # Note: The actual tzname can vary (e.g., CET/CEST). For consistent testing,
    # a more robust mock for tzname might be needed if the exact string is critical.
    # Here, we assume 'CET' for simplicity in the test assertion.
    # In a real scenario, you might mock ZoneInfo('Europe/Madrid').tzname as well.
    assert casts.dtaware2str(dt, format="long string") == "15 de enero de 2023 a las 10:30 (CET)"

def test_dtaware2str_long_string_naive_datetime():
    dt_naive = datetime(2023, 1, 15, 10, 30, 0)
    with pytest.raises(exceptions.CastException):
        casts.dtaware2str(dt_naive, format="long string")

def test_dtaware2str_long_string_ignore_exception_naive():
    dt_naive = datetime(2023, 1, 15, 10, 30, 0)
    assert casts.dtaware2str(dt_naive, format="long string", ignore_exception=True, ignore_exception_value="N/A") == "N/A"
