from datetime import date, time, datetime
from decimal import Decimal
from pydicts import casts, exceptions
from pytest import raises
from zoneinfo import ZoneInfo

zonename_madrid="Europe/Madrid"
zoneinfo_utc=ZoneInfo("UTC")
dtnaive=casts.dtnaive_now()
dtaware_utc=casts.dtaware_now()
dtaware_madrid=casts.dtaware_now(zonename_madrid)

def test_object_or_empty():
    assert casts.object_or_empty(None)==""
    assert casts.object_or_empty(1)==1
    
def test_str2decimal():
    assert casts.str2decimal(None, 1)==None
    assert casts.str2decimal("2.123,25", 1)==Decimal("2123.25")

def test_str2bool():
    with raises(exceptions.CastException):
        casts.str2bool(None)==None
    with raises(exceptions.CastException):
        assert casts.str2bool(1)==True
    with raises(exceptions.CastException):
        assert casts.str2bool(0)==False
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
    
### Function that converts a None value into a Decimal('0')
### @param dec Should be a Decimal value or None
### @return Decimal
#def test_none2decimal0(dec):
#    return none2alt(dec,Decimal('0'))
#
### If a value is None, returns an alternative
#def test_none2alt(value, alternative):
#    if value==None:
#        return alternative
#    return value
#

def test_bytes2str():
    assert casts.bytes2str(None)==None
    assert casts.bytes2str(b"Hello")=="Hello"
    
def test_str2bytes():
    assert casts.str2bytes(None)==None
    assert casts.str2bytes("Hello")==b"Hello"

def test_is_aware():
    assert casts.is_aware(dtnaive)==False
    assert casts.is_aware(dtaware_utc)==True

def test_is_naive():
    assert casts.is_naive(dtnaive)==True
    assert casts.is_naive(dtaware_utc)==False

def test_dtaware():
    assert dtaware_utc==casts.dtaware(dtaware_utc.date(), dtaware_utc.time(), "UTC")

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

def test_dtaware_day_end_from_date():
    assert casts.dtaware_day_end_from_date(date(2023, 12, 29), "UTC")==datetime(2023, 12, 29, 23, 59, 59, 999999, ZoneInfo("UTC"))

### Returns a dtnaive or dtawre (as parameter) with the end of the day
#def test_dt_day_start(dt):
#    return dt.replace(hour=0, minute=0, second=0, microsecond=0)
#
### Returns the end of the day dtnaive from a date
#def test_dtnaive_day_start_from_date(dat):
#    dt=datetime(dat.year, dat.month, dat.day)
#    return dt_day_start(dt)
#
### Returns the end of the day dtaware of the tz_name timezone from a date
#def test_dtaware_day_start_from_date(date, tz_name):
#    dt=dtaware(date, time(0, 0), tz_name)
#    return dt_day_start(dt)
#
### Returns the start of a month
#def test_dtaware_month_start(year, month, tz_name):
#    return dtaware_day_start_from_date(date(year, month, 1), tz_name)
#    
#def test_month2int(s):
#    """
#        Converts a month string to a int
#    """
#    if s in ["Jan", "Ene", "Enero", "January", "enero", "january"]:
#        return 1
#    if s in ["Feb", "Febrero", "February", "febrero", "february"]:
#        return 2
#    if s in ["Mar", "Marzo", "March", "marzo", "march"]:
#        return 3
#    if s in ["Apr", "Abr", "April", "Abril", "abril", "april"]:
#        return 4
#    if s in ["May", "Mayo", "mayo", "may"]:
#        return 5
#    if s in ["Jun", "June", "Junio", "junio", "june"]:
#        return 6
#    if s in ["Jul", "July", "Julio", "julio", "july"]:
#        return 7
#    if s in ["Aug", "Ago", "August", "Agosto", "agosto", "august"]:
#        return 8
#    if s in ["Sep", "Septiembre", "September", "septiembre", "september"]:
#        return 9
#    if s in ["Oct", "October", "Octubre", "octubre", "october"]:
#        return 10
#    if s in ["Nov", "Noviembre", "November", "noviembre", "november"]:
#        return 11
#    if s in ["Dic", "Dec", "Diciembre", "December", "diciembre", "december"]:
#        return 12
#
def test_str2time():
#    allowed=["HH:MM", "HH:MM:SS","HH:MMxx"]
    assert casts.str2time("09:05", "HH:MM")==time(9, 5)
    assert casts.str2time("09:05:54", "HH:MM:SS")==time(9, 5, 54)
    assert casts.str2time("09:05pm", "HH:MMxx")==time(21, 5)

def test_time2str():
#    allowed=["HH:MM", "HH:MM:SS","Xulpymoney"]
    time_=time(9, 5, 54)
    assert casts.time2str(time_, "HH:MM")=="09:05"
    assert casts.time2str(time_, "HH:MM:SS")=="09:05:54"

def test_str2date():
#    allowed=["YYYY-MM-DD", "DD/MM/YYYY", "DD.MM.YYYY", "DD/MM"]

    assert casts.str2date("2023-11-26")==date(2023, 11, 26)
    assert casts.str2date("2023-11-26", "YYYY-MM-DD")==date(2023, 11, 26)
    assert casts.str2date("26/11/2023", "DD/MM/YYYY")==date(2023, 11, 26)
    assert casts.str2date("26.11.2023", "DD.MM.YYYY")==date(2023, 11, 26)
    assert casts.str2date("26/11", "DD/MM")==date(2023, 11, 26)
#
def test_str2dtnaive():
#    allowed=["%Y%m%d%H%M","%Y-%m-%d %H:%M:%S","%d/%m/%Y %H:%M","%d %m %H:%M %Y","%Y-%m-%d %H:%M:%S.","%H:%M:%S", '%b %d %H:%M:%S']

#    assert casts.str2dtnaive("2023-11-26", "%Y-%m-%d")==datetime(2023, 11, 26)
#    assert casts.str2dtnaive("2023-11-26 17:05:05", "%Y-%m-%d %H:%M:%S")==datetime(2023, 11, 26, 17, 5, 5)
#    assert casts.str2dtnaive("20231126 1705", "%Y%m%d %H%M")==datetime(2023, 11, 26, 17, 5, 5)
    assert casts.str2dtnaive("202311261705", "%Y%m%d%H%M")==datetime(2023, 11, 26, 17, 5)
    assert casts.str2dtnaive("2023-11-26T17:05:05.123456", "JsIso")==datetime(2023, 11, 26, 17, 5, 5, 123456)
    assert casts.str2dtnaive("2023-11-26T17:05:05", "JsIso")==datetime(2023, 11, 26, 17, 5, 5)


def test_str2dtaware():
#    allowed=["%Y-%m-%d %H:%M:%S%z","%Y-%m-%d %H:%M:%S.%z", "JsUtcIso"]
    #assert casts.str2dtaware("2023-11-26", "%Y-%m-%d")==datetime(2023, 11, 26, tzinfo=ZoneInfo('UTC'))
    #assert casts.str2dtaware("202311261705", "%Y%m%d%H%M")==datetime(2023, 11, 26, 17, 5)
    assert casts.str2dtaware("2023-11-26T17:05:05Z", "JsUtcIso")==datetime(2023, 11, 26, 17, 5, 5, tzinfo=ZoneInfo('UTC'))

### epoch is the time from 1,1,1970 in UTC
### return now(timezone(self.name))
#def test_dtaware2epochms(d):
#    return d.timestamp()*1000
#    
### Return a UTC datetime aware
#def test_epochms2dtaware(n, tz="UTC"):
#    utc_unaware=datetime.utcfromtimestamp(n/1000)
#    utc_aware=utc_unaware.replace(tzinfo=timezone('UTC'))#Due to epoch is in UTC
#    return dtaware_changes_tz(utc_aware, tz)
#
### epoch is the time from 1,1,1970 in UTC
### return now(timezone(self.name))
#def test_dtaware2epochmicros(d):
#    return int(d.timestamp()*1000000)
### Return a UTC datetime aware
#def test_epochmicros2dtaware(n, tz="UTC"):
#    utc_unaware=datetime.utcfromtimestamp(n/1000000)
#    utc_aware=utc_unaware.replace(tzinfo=timezone('UTC'))#Due to epoch is in UTC
#    return dtaware_changes_tz(utc_aware, tz)
#
#

def test_dtaware2string():    
    dt_aware=datetime(2023, 11, 26, 17, 5, 5, 123456, tzinfo=ZoneInfo("Europe/Madrid"))
    assert casts.dtnaive2str(dt_aware, "%Y-%m-%d")=="2023-11-26"
    assert casts.dtnaive2str(dt_aware, "%Y-%m-%d %H:%M:%S")=="2023-11-26 17:05:05"
    assert casts.dtnaive2str(dt_aware, "%Y%m%d %H%M")=="20231126 1705"
    assert casts.dtnaive2str(dt_aware, "%Y%m%d%H%M")=="202311261705"
    assert casts.dtnaive2str(dt_aware, "JsUtcIso")=="2023-11-26T17:05:05Z"


def test_dtnaive2string():
    dt_naive=datetime(2023, 11, 26, 17, 5, 5, 123456)
    assert casts.dtnaive2str(dt_naive, "%Y-%m-%d")=="2023-11-26"
    assert casts.dtnaive2str(dt_naive, "%Y-%m-%d %H:%M:%S")=="2023-11-26 17:05:05"
    assert casts.dtnaive2str(dt_naive, "%Y%m%d %H%M")=="20231126 1705"
    assert casts.dtnaive2str(dt_naive, "%Y%m%d%H%M")=="202311261705"
    assert casts.dtnaive2str(dt_naive, "JsUtcIso")=="2023-11-26T17:05:05Z"

def test_dtaware_changes_tz():
    #Sacado date en linux
    dt_madrid=datetime(2023, 11, 26, 12, 0,  tzinfo=ZoneInfo("Europe/Madrid"))
    dt_utc=datetime(2023, 11, 26, 11, 0,  tzinfo=ZoneInfo("UTC"))
    
    assert casts.dtaware_changes_tz(dt_madrid, "UTC")==dt_utc
    assert casts.dtaware_changes_tz(dt_utc, "Europe/Madrid")==dt_madrid

def test_months():
    assert casts.months(2023, 11, 2024, 1)== [(2023, 11), (2023, 12), (2024, 1)]
    assert casts.months(2023, 9,  2023, 9)== [(2023, 9)]

