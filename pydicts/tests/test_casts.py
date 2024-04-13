from datetime import date, time, datetime, timedelta
from decimal import Decimal
from pydicts import casts, exceptions
from pytest import raises
from zoneinfo import ZoneInfo

def test_is_noe():
    assert casts.is_noe(None)==True
    assert casts.is_noe(1)==False
    assert casts.is_noe("")==True
    assert casts.is_noe("HELLO")==False    
    
def test_none2alternative():
    assert casts.none2alternative(1, 1)==1
    assert casts.none2alternative(None, Decimal(0))==Decimal(0)
    assert casts.none2alternative(None, None)==None
    
def test_object_or_empty():
    assert casts.object_or_empty(None)==""
    assert casts.object_or_empty(1)==1
    assert casts.object_or_empty("")==""

def test_str2decimal():
    with raises(exceptions.CastException):
        assert casts.str2decimal(None)
    assert casts.str2decimal("", ignore_exception=True)==None
    
    with raises(exceptions.CastException):
        assert casts.str2decimal("")
    assert casts.str2decimal("", ignore_exception=True)==None
    
    with raises(exceptions.CastException):
        assert casts.str2decimal("2.123,25")
    assert casts.str2decimal("2.123,25", ignore_exception=True)==None
    
    with raises(exceptions.CastException):
        assert casts.str2decimal("2.123,25")
    assert casts.str2decimal("2.123,25", ignore_exception=True)==None
    
    with raises(exceptions.CastException):
        assert casts.str2decimal("2,123.25")
    assert casts.str2decimal("2,123.25", ignore_exception=True)==None
    
    assert casts.str2decimal("121212.123")==Decimal("121212.123")

def test_str2bool():
    with raises(exceptions.CastException):
        assert casts.str2bool(None)
    casts.str2bool(None, ignore_exception=True)==None
    
    with raises(exceptions.CastException):
        assert casts.str2bool(1)
    assert casts.str2bool(1, ignore_exception=True)==None
    
    with raises(exceptions.CastException):
        assert casts.str2bool(0)
    assert casts.str2bool(0, ignore_exception=True)==None
    assert casts.str2bool("1")==True
    assert casts.str2bool("0")==False
    with raises(exceptions.CastException):
        assert casts.str2bool(True)
    with raises(exceptions.CastException):
        assert casts.str2bool(False)
    assert casts.str2bool("true")==True
    assert casts.str2bool("True")==True
    assert casts.str2bool("false")==False
    assert casts.str2bool("False")==False
    

def test_date_first_of_the_next_x_months():
    date_plus_3_months=casts.date_first_of_the_next_x_months(2023, 11, 3)
    assert date_plus_3_months.year==2024
    assert date_plus_3_months.month==2
    assert date_plus_3_months.day==1
    date_minus_12_months=casts.date_first_of_the_next_x_months(2023, 11, -12)
    assert date_minus_12_months.year==2022
    assert date_minus_12_months.month==11
    assert date_minus_12_months.day==1
    
def test_date_last_of_the_next_x_months():
    date_plus_3_months=casts.date_last_of_the_next_x_months(2023, 11, 3)
    assert date_plus_3_months.year==2024
    assert date_plus_3_months.month==2
    assert date_plus_3_months.day==29
    date_minus_12_months=casts.date_last_of_the_next_x_months(2023, 11, -12)
    assert date_minus_12_months.year==2022
    assert date_minus_12_months.month==11
    assert date_minus_12_months.day==30

def test_date_first_of_the_year():
    assert casts.date_first_of_the_year(2022)==date(2022, 1, 1)
    
def test_date_last_of_the_year():
    assert casts.date_last_of_the_year(2023)==date(2023, 12, 31)

def test_bytes2str():
    with raises(exceptions.CastException):
        assert casts.bytes2str(None)==None
    assert casts.bytes2str(None, ignore_exception=True)==None
    assert casts.bytes2str(b"Hello")=="Hello"
    
def test_str2bytes():
    with raises(exceptions.CastException):
        assert casts.str2bytes(None)==None
    assert casts.str2bytes(None, ignore_exception=True)==None
    assert casts.str2bytes("Hello")==b"Hello"

def test_is_aware():
    assert casts.is_aware(casts.dtnaive_now())==False
    assert casts.is_aware(casts.dtaware_now())==True

def test_is_naive():
    assert casts.is_naive(casts.dtnaive_now())==True
    assert casts.is_naive(casts.dtaware_now())==False

def test_dtaware():
    dtaware_utc=casts.dtaware_now()
    assert dtaware_utc==casts.dtaware(dtaware_utc.date(), dtaware_utc.time(), "UTC")
    
def test_dtaware2dtnaive():
    dt_naive=  datetime(2023, 11, 26, 17, 5, 5, 123456)
    dt_aware=casts.dtnaive2dtaware(dt_naive, "UTC")
    with raises(exceptions.CastException):
        casts.dtaware2dtnaive(dt_naive)
    assert dt_naive==casts.dtaware2dtnaive(dt_aware)

def test_dtnaive():
    assert casts.dtnaive(date(2020,1 , 1), time(1, 1, 1, 1))==datetime(2020, 1, 1, 1, 1, 1, 1)
    with raises(ValueError):
        casts.dtnaive(date(2020,1 , 61), time(1, 1, 1, 1))

def test_dtnaive2dtaware():
    naive=datetime(2023, 1, 1, 0, 0, 0, 0)
    assert casts.dtnaive2dtaware(naive, "Europe/Madrid")==naive.replace(tzinfo=ZoneInfo("Europe/Madrid"))

def test_date_first_of_the_month():
    assert casts.date_first_of_the_month(2023, 11)==date(2023, 11, 1)
    with raises(ValueError):
        casts.date_first_of_the_month(2023, 13)

def test_date_last_of_the_month():
    assert casts.date_last_of_the_month(2023, 11)==date(2023, 11, 30)
    with raises(ValueError):
        casts.date_first_of_the_month(2023, 13)

def test_dtaware_now():
    pass
    
def test_dtnaive_now():
    pass
    
def test_dtaware_month_start():
    pass

def test_dtaware_month_end():
    assert casts.dtaware_month_end(2023, 11, "UTC")==datetime(2023, 11, 30, 23, 59, 59, 999999, ZoneInfo("UTC"))
    
def test_dtaware_year_start():
    assert casts.dtaware_year_start(2023, "UTC")==datetime(2023, 1, 1,0, 0, 0, 0, ZoneInfo("UTC"))

def test_dtaware_year_end():
    assert casts.dtaware_year_end(2023, "UTC")==datetime(2023, 12, 31, 23, 59, 59, 999999, ZoneInfo("UTC"))

def test_dtnaive_day_end():
    assert casts.dtnaive_day_end(casts.dtnaive_now()).time()==time(23, 59, 59, 999999)

def test_dtnaive_day_end_from_date():
    assert casts.dtnaive_day_end_from_date(date(2023, 12, 29))==datetime(2023, 12, 29, 23, 59, 59, 999999)

def test_dtaware_day_end():
    pass

def test_dtaware_day_end_from_date():
    assert casts.dtaware_day_end_from_date(date(2023, 12, 29), "UTC")==datetime(2023, 12, 29, 23, 59, 59, 999999, ZoneInfo("UTC"))

def test_dtaware_day_start():
    pass

def test_dtaware_day_start_from_date():
    pass

def test_str2time():
#    allowed=["HH:MM", "HH:MM:SS","HH:MMxx"]
    with raises(exceptions.CastException):
        assert casts.str2time(None)
    assert casts.str2time("09:05", "HH:MM")==time(9, 5)
    assert casts.str2time("09:05:54", "HH:MM:SS")==time(9, 5, 54)
    assert casts.str2time("09:05:54.123")==time(9, 5, 54, 123000)
    assert casts.str2time("09:05:54.000123")==time(9, 5, 54, 123)
    assert casts.str2time("09:05pm", "HH:MMxx")==time(21, 5)
    
    
def test_str2timedelta():
    assert casts.str2timedelta("P396DT01H01M01.000001S")==timedelta(days=396,  hours=1,  minutes=1, seconds=1, microseconds=1)
    assert casts.str2timedelta("PT0S")==timedelta( seconds=0)
    
    
    with raises(exceptions.CastException):
        casts.str2timedelta(None)
    with raises(exceptions.CastException):
        casts.str2timedelta("")
    
    assert casts.str2timedelta(None, ignore_exception=True)==None
    assert casts.str2timedelta("", ignore_exception=True)==None
    
def test_timedelta2str():
    assert casts.timedelta2str(timedelta(days=396,  hours=1,  minutes=1, seconds=1, microseconds=1))=="P396DT1H1M1.000001S"
    assert casts.timedelta2str(timedelta(days=0))=="P0D"
    
    with raises(exceptions.CastException):
        casts.timedelta2str(None)
    with raises(exceptions.CastException):
        casts.timedelta2str("")
        
        
    assert casts.timedelta2str(None, ignore_exception=True)==None
    assert casts.timedelta2str("", ignore_exception=True)==None

def test_time2str():
    with raises(exceptions.CastException):
        assert casts.time2str(None)
        
    assert casts.time2str(None, ignore_exception=True)==None
    time_=time(9, 5, 54, 123456)
    assert casts.time2str(time_, "HH:MM")=="09:05"
    assert casts.time2str(time_, "HH:MM:SS")=="09:05:54"
    assert casts.time2str(time_)=="09:05:54.123456"

def test_str2date():
    with raises(exceptions.CastException):
        assert casts.str2date(None)
    assert casts.str2date(None, ignore_exception=True)==None
    
    with raises(exceptions.CastException):
        assert casts.str2date("2023")
        
    with raises(exceptions.CastException):
        assert casts.str2date(2023)
    
    assert casts.str2date("2023-11-26")==date(2023, 11, 26)
    assert casts.str2date("2023-11-26", "YYYY-MM-DD")==date(2023, 11, 26)
    assert casts.str2date("26/11/2023", "DD/MM/YYYY")==date(2023, 11, 26)
    assert casts.str2date("26.11.2023", "DD.MM.YYYY")==date(2023, 11, 26)
    assert casts.str2date("26/11", "DD/MM")==date(date.today().year, 11, 26)

def test_str2dtnaive():
    assert casts.str2dtnaive("202311261705", "%Y%m%d%H%M")==datetime(2023, 11, 26, 17, 5)
    assert casts.str2dtnaive("2023-11-26T17:05:05")==datetime(2023, 11, 26, 17, 5, 5)
    assert casts.str2dtnaive("2023-11-26T17:05:05.123456", "JsIso")==datetime(2023, 11, 26, 17, 5, 5, 123456)

    with raises(exceptions.CastException):
        casts.str2dtnaive("2023-11-26T17:05:05.123456Z")
    
    assert casts.str2dtnaive("2023-11-26T17:05:05.123456Z", ignore_exception=True)==None


def test_str2dtaware():   
    with raises(exceptions.CastException):
        casts.str2dtaware("2023-11-26T17:05:05Z", "YYYY-mm-dd")
    
    assert casts.str2dtaware("2023-11-26T17:05:05Z", "YYYY-mm-dd", ignore_exception=True)==None
    assert casts.str2dtaware("2023-11-26T17:05:05Z")==datetime(2023, 11, 26, 17, 5, 5, tzinfo=ZoneInfo('UTC'))
    assert casts.str2dtaware("2023-11-26T17:05:05", "JsUtcIso", ignore_exception=True)==None

def test_dtaware2str():    
    dt_naive=  datetime(2023, 11, 26, 17, 5, 5, 123456)
    dt_aware=casts.dtnaive2dtaware(dt_naive, "UTC")
    with raises(exceptions.CastException):
        casts.dtaware2str(dt_naive)
    assert casts.dtaware2str(dt_aware, "%Y-%m-%d")=="2023-11-26"
    assert casts.dtaware2str(dt_aware, "%Y-%m-%d %H:%M:%S")=="2023-11-26 17:05:05"
    assert casts.dtaware2str(dt_aware, "%Y%m%d %H%M")=="20231126 1705"
    assert casts.dtaware2str(dt_aware, "%Y%m%d%H%M")=="202311261705"
    assert casts.dtaware2str(dt_aware, "JsUtcIso")=="2023-11-26T17:05:05.123456Z"


def test_dtnaive2str():
    dt_naive=  datetime(2023, 11, 26, 17, 5, 5, 123456)
    dt_aware=casts.dtnaive2dtaware(dt_naive, "UTC")
    with raises(exceptions.CastException):
        casts.dtnaive2str(dt_aware)
    
    assert casts.dtnaive2str(dt_naive, "%Y-%m-%d")=="2023-11-26"
    assert casts.dtnaive2str(dt_naive, "%Y-%m-%d %H:%M:%S")=="2023-11-26 17:05:05"
    assert casts.dtnaive2str(dt_naive, "%Y%m%d %H%M")=="20231126 1705"
    assert casts.dtnaive2str(dt_naive, "%Y%m%d%H%M")=="202311261705"
    assert casts.dtnaive2str(dt_naive, "JsIso")=="2023-11-26T17:05:05.123456"

def test_dtaware_changes_tz():
    #Sacado date en linux
    dt_madrid=datetime(2023, 11, 26, 12, 0,  tzinfo=ZoneInfo("Europe/Madrid"))
    dt_utc=datetime(2023, 11, 26, 11, 0,  tzinfo=ZoneInfo("UTC"))
    
    assert casts.dtaware_changes_tz(dt_madrid, "UTC")==dt_utc
    assert casts.dtaware_changes_tz(dt_utc, "Europe/Madrid")==dt_madrid

def test_months():
    assert casts.months(2023, 11, 2024, 1)== [(2023, 11), (2023, 12), (2024, 1)]
    assert casts.months(2023, 9,  2023, 9)== [(2023, 9)]

def test_bytes2base64bytes():
    s="Elvis Presley"
    bytes=casts.str2bytes(s)
    base64bytes=casts.bytes2base64bytes(bytes)
    bytes2=casts.base64bytes2bytes(base64bytes)
    assert s==casts.bytes2str(bytes2)
    
def test_base64bytes2bytes():
    pass

def test_dtaware2epochmicros():
    pass
    
def test_epochmicros2dtaware():
    pass

def test_epochms2dtaware():
    pass

def test_email():
    assert casts.is_email(None)==False
    assert casts.is_email("")==False
    assert casts.is_email(12)==False
    assert casts.is_email("hi.hi.com")==False
    assert casts.is_email("hi@hi@.com")==False
    assert casts.is_email("hi@hi.com.")==False
    assert casts.is_email("hi@hi.comm")
    
    
    
    
