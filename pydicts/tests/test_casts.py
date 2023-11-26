from datetime import date, time, datetime
from decimal import Decimal
from pydicts import casts
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
    with raises(Exception):
        casts.str2bool(None)==None
    with raises(Exception):
        assert casts.str2bool(1)==True
    with raises(Exception):
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
    
### Returns an aware datetime with the start of year
#def test_dtaware_year_start(year, tz_name):
#    return dtaware_day_start_from_date(date(year, 1, 1), tz_name)
#    
### Returns an aware datetime with the last of year
#def test_dtaware_year_end(year, tz_name):
#    return dtaware_day_end_from_date(date(year, 12, 31), tz_name)
#    

def test_dtnaive_day_end():
    assert casts.dtnaive_day_end(casts.dtnaive_now()).time()==time(23, 59, 59, 999999)

### Returns the end of the day dtnaive from a date
#def test_dtnaive_day_end_from_date(dat):
#    dt=datetime(dat.year, dat.month, dat.day)
#    return dt_day_end(dt)
#
### Returns the end of the day dtaware of the tz_name timezone from a date
#def test_dtaware_day_end_from_date(date, tz_name):
#    dt=dtaware(date, time(0, 0), tz_name)
#    return dt_day_end(dt)    
#    
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
#def test_string2time(s, format="HH:MM"):
#    allowed=["HH:MM", "HH:MM:SS","HH:MMxx"]
#    if format in allowed:
#        if format=="HH:MM":#12:12
#            a=s.split(":")
#            return time(int(a[0]), int(a[1]))
#        elif format=="HH:MM:SS":#12:12:12
#            a=s.split(":")
#            return time(int(a[0]), int(a[1]), int(a[2]))
#        elif format=="HH:MMxx": #5:12am o pm
#            s=s.upper()
#            s=s.replace("AM", "")
#            if s.find("PM"):
#                s=s.replace("PM", "")
#                points=s.split(":")
#                return time(int(points[0])+12, int(points[1]))
#            else:#AM
#                points=s.split(":")
#                return time(int(points[0]), int(points[1]))
#    else:
#        error("I can't convert this format '{}'. I only support this {}".format(format, allowed))
#
### Converts a time to a string
#def test_time2string(ti, format="HH:MM" ):
#    allowed=["HH:MM", "HH:MM:SS","Xulpymoney"]
#    if format in allowed:
#        if ti==None:
#            return None
#        if format=="Xulpymoney":
#            if ti.microsecond in (4, 5):
#                return str(ti)[11:-13]
#            else:
#                return str(ti)[11:-6]
#        elif format=="HH:MM":
#            return ("{}:{}".format(str(ti.hour).zfill(2), str(ti.minute).zfill(2)))
#        elif format=="HH:MM:SS":
#            return ("{}:{}:{}".format(str(ti.hour).zfill(2), str(ti.minute).zfill(2), str(ti.second).zfill(2)))
#
#
#def test_string2date(iso, format="YYYY-MM-DD"):
#    allowed=["YYYY-MM-DD", "DD/MM/YYYY", "DD.MM.YYYY", "DD/MM"]
#    if format in allowed:
#        try:
#            if format=="YYYY-MM-DD": #YYYY-MM-DD
#                d=iso.split("-")
#                return date(int(d[0]), int(d[1]),  int(d[2]))
#            if format=="DD/MM/YYYY": #DD/MM/YYYY
#                d=iso.split("/")
#                return date(int(d[2]), int(d[1]),  int(d[0]))
#            if format=="DD.MM.YYYY": #DD.MM.YYYY
#                d=iso.split(".")
#                return date(int(d[2]), int(d[1]),  int(d[0]))
#            if format=="DD/MM": #DD/MM
#                d=iso.split("/")
#                return date(date.today().year, int(d[1]),  int(d[0]))
#        except:
#            return None
#    else:
#        error("I can't convert this format '{}'. I only support this {}".format(format, allowed))
#
#def test_string2dtnaive(s, format):
#    allowed=["%Y%m%d%H%M","%Y-%m-%d %H:%M:%S","%d/%m/%Y %H:%M","%d %m %H:%M %Y","%Y-%m-%d %H:%M:%S.","%H:%M:%S", '%b %d %H:%M:%S']
#    if format in allowed:
#        if format=="%Y%m%d%H%M":
#            dat=datetime.strptime( s, format )
#            return dat
#        if format=="%Y-%m-%d %H:%M:%S":#2017-11-20 23:00:00
#            return datetime.strptime( s, format )
#        if format=="%d/%m/%Y %H:%M":#20/11/2017 23:00
#            return datetime.strptime( s, format )
#        if format=="%d %m %H:%M %Y":#27 1 16:54 2017. 1 es el mes convertido con month2int
#            return datetime.strptime( s, format)
#        if format=="%Y-%m-%d %H:%M:%S.":#2017-11-20 23:00:00.000000  ==>  microsecond. Notice the point in format
#            arrPunto=s.split(".")
#            s=arrPunto[0]
#            micro=int(arrPunto[1]) if len(arrPunto)==2 else 0
#            dt=datetime.strptime( s, "%Y-%m-%d %H:%M:%S" )
#            dt=dt+timedelta(microseconds=micro)
#            return dt
#        if format=="%H:%M:%S": 
#            tod=date.today()
#            a=s.split(":")
#            return datetime(tod.year, tod.month, tod.day, int(a[0]), int(a[1]), int(a[2]))
#        if format=='%b %d %H:%M:%S': #Apr 26 07:50:44. Year is missing so I set to current
#            s=f"{date.today().year} {s}"
#            return datetime.strptime(s, '%Y %b %d %H:%M:%S')
#    else:
#        error("I can't convert this format '{}'. I only support this {}".format(format, allowed))
#
#def test_string2dtaware(s, format, tz_name='UTC'):
#    allowed=["%Y-%m-%d %H:%M:%S%z","%Y-%m-%d %H:%M:%S.%z", "JsUtcIso"]
#    if format in allowed:
#        if format=="%Y-%m-%d %H:%M:%S%z":#2017-11-20 23:00:00+00:00
#            s=s[:-3]+s[-2:]
#            dt=datetime.strptime( s, format )
#            return dtaware_changes_tz(dt, tz_name)
#        if format=="%Y-%m-%d %H:%M:%S.%z":#2017-11-20 23:00:00.000000+00:00  ==>  microsecond. Notice the point in format
#            s=s[:-3]+s[-2:]#quita el :
#            arrPunto=s.split(".")
#            s=arrPunto[0]+s[-5:]
#            micro=int(arrPunto[1][:-5])
#            dt=datetime.strptime( s, "%Y-%m-%d %H:%M:%S%z" )
#            dt=dt+timedelta(microseconds=micro)
#            return dtaware_changes_tz(dt, tz_name)
#        if format=="JsUtcIso": #2021-08-21T06:27:38.294Z
#            s=s.replace("T"," ").replace("Z","")
#            dtnaive=string2dtnaive(s,"%Y-%m-%d %H:%M:%S.")
#            dtaware_utc=dtnaive2dtaware(dtnaive, 'UTC')
#            return dtaware_changes_tz(dtaware_utc, tz_name)
#
#    else:
#        return timezone(tz_name).localize(string2dtnaive(s,format))
#
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
### Returns a formated string of a dtaware string formatting with a zone name
### @param dt datetime aware object
### @return String
#def test_dtaware2string(dt, format):
#    if is_naive(dt)==True:
#        error("A dtaware is needed for {}".format(dt))
#    else:
#        return dtnaive2string(dt, format)
#
### Returns a formated string of a dtaware string formatting with a zone name
### @param dt datetime aware object
### @param format String in ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y%m%d %H%M", "%Y%m%d%H%M"]
### @return String
#def test_dtnaive2string(dt, format):
#    allowed=["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y%m%d %H%M", "%Y%m%d%H%M", "JsUtcIso"]
#    if dt==None:
#        return "None"
#    elif format in allowed:
#        if format=="%Y-%m-%d":
#            return dt.strftime("%Y-%m-%d")
#        elif format=="%Y-%m-%d %H:%M:%S": 
#            return dt.strftime("%Y-%m-%d %H:%M:%S")
#        elif format=="%Y%m%d %H%M": 
#            return dt.strftime("%Y%m%d %H%M")
#        elif format=="%Y%m%d%H%M":
#            return dt.strftime("%Y%m%d%H%M")
#        elif format=="JsUtcIso":
#            return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
#    else:
#        error("I can't convert this format '{}'. I only support this {}".format(format, allowed))
#
### Changes zoneinfo from a dtaware object
### For example:
### - datetime.datetime(2018, 5, 18, 8, 12, tzinfo=<DstTzInfo 'Europe/Madrid' CEST+2:00:00 DST>)
### - libcaloriestrackerfunctions.dtaware_changes_tz(a,"Europe/London")
### - datetime.datetime(2018, 5, 18, 7, 12, tzinfo=<DstTzInfo 'Europe/London' BST+1:00:00 DST>)
### @param dt datetime aware object
### @param tzname String with datetime zone. For example: "Europe/Madrid"
### @return datetime aware object
#def test_dtaware_changes_tz(dt,  tzname):
#    if dt==None:
#        return None
#    tzt=timezone(tzname)
#    tarjet=tzt.normalize(dt.astimezone(tzt))
#    return tarjet
#
### Returns a list of tuples (year, month) from a month to another month, both included
### @param year_from Integer
### @param month_from Integer
### @param year_to Integer If none uses current year
### @param month_to Integer If none uses current month
#def test_months(year_from, month_from, year_to=None, month_to=None):
#    if year_to is None or month_to is None:
#        year_to=date.today().year
#        month_to=date.today().month
#    r=[]
#    end=date_first_of_the_month(year_to, month_to)
#    current=date_first_of_the_month(year_from, month_from)
#    while True:
#        if current>end:
#            break
#        r.append((current.year,current.month))
#        current=date_first_of_the_next_x_months(current.year, current.month, 1)
#    return r
#
#if __name__ == "__main__":
#    tz="Europe/Madrid"
#    now=dtnaive_now()
#    print("Current localzone is", tz)
#    print ("DtNaive:",  now)
#    now_aware=dtaware(now.date(), now.time(), tz)
#    print("DtAware:", now_aware, "With dtaware_now", dtaware_now(tz))
#    epochms=dtaware2epochms(now_aware)
#    print("Epoch in miliseconds:", epochms)
#    print("Dtaware reconverting epoch {}".format(epochms2dtaware(epochms, tz)) )
#    epochmicros=dtaware2epochmicros(now_aware)
#    print("Epoch in microseconds:", epochmicros)
#    print("Dtaware reconverting epoch in microseconds {}".format(epochmicros2dtaware(epochmicros, tz)) )
#    now_aware_in_utc=dtaware_changes_tz(now_aware, 'UTC')
#    print("Datetime '{}' changes to UTC '{}'".format(now_aware, now_aware_in_utc))
#    print()
#    print("dtaware2string")
#    print("  - {}".format(dtaware2string(now_aware, "%Y-%m-%d %H:%M:%S")))
#    print("  - {}".format(dtaware2string(now_aware, "%Y%m%d %H%M")))
#    print("  - {}".format(dtaware2string(now_aware, "%Y%m%d%H%M")))
#    print()
#    print("dt_day_end")
#    print("  - Today will end at '{}' as naive".format(dt_day_end(now)))
#    print("  - Today will end at '{}' as aware in this timezone '{}'".format( dt_day_end(now_aware), tz))
#    print()    
#    print("time2string")
#    print("  - This is the current hour '{}' with format HH:MM".format(time2string(now.time(), "HH:MM")))
#    print("  - This is the current hour '{}' with format HH:MM:SS".format(time2string(now.time(), "HH:MM:SS")))
#    print()    
#    print("string2dtnaive and string2dtaware")
#    a="201910022209"
#    format="%Y%m%d%H%M"
#    print("  - {}: {} and {}".format(a,string2dtnaive(a,format),string2dtaware(a,format)))
#    a="2019-10-03 2:22:09"
#    format="%Y-%m-%d %H:%M:%S"
#    print("  - {}: {} and {}".format(a,string2dtnaive(a,format),string2dtaware(a,format)))
#    a="2019-10-03 2:22:09+05:00"
#    format="%Y-%m-%d %H:%M:%S%z"
#    print("  - {}: UTC: {}. Madrid: {}".format(a,string2dtaware(a,format),string2dtaware(a,format,"Europe/Madrid")))
#    a="2019-10-03 2:22:09.267+05:00"
#    format="%Y-%m-%d %H:%M:%S.%z"
#    print("  - {}: UTC: {}. Madrid: {}".format(a,string2dtaware(a,format),string2dtaware(a,format,"Europe/Madrid")))
#    a="2019-10-03 2:22:09"
#    format="%Y-%m-%d %H:%M:%S"
#    print("  - {}: {} and {}".format(a,string2dtnaive(a,format),string2dtaware(a,format)))
#    a="2019-10-03 2:22:09.267"
#    format="%Y-%m-%d %H:%M:%S."
#    print("  - {}: {} and {}".format(a,string2dtnaive(a,format),string2dtaware(a,format)))
#    
#    print("Js UTC ISO 2 DTAWARE")
#    a="2021-08-21T06:27:38.294Z"
#    print(f"  - {a}: {string2dtaware(a,'JsUtcIso','Europe/Madrid')}")
#
#
