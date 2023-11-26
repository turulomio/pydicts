### If a function only can be used by dtaware or naive it will have its prefix dtaware_ or dtnaive_
### If a function can use both of them its prefix will be dt_
from decimal import Decimal
from datetime import timedelta, date, datetime, time
from zoneinfo import ZoneInfo

_=str

def object_or_empty(v):
    """
        Returns and empty string if None, else return value
    """
    return "" if v is None else v

## Converts a string  to a decimal
def str2decimal(s, type):
    if type==1: #2.123,25
        try:
            return Decimal(s.replace(".","").replace(",", "."))
        except:
            return None


def str2bool(value):
    """
        Converts strings True or False to boolean
        @param s String
        @return Boolean
    """
    def exception():
        raise Exception(f"Method str2bool couldn't convert {value} ({value.__class__} to a boolean")
    if not value.__class__ is str:
        exception()
        
    if value=="0" or value.lower()=="false":
        return False
    elif value=="1" or value.lower()=="true":
        return True
    exception()
### Function that converts a None value into a Decimal('0')
### @param dec Should be a Decimal value or None
### @return Decimal
#def none2decimal0(dec):
#    return none2alt(dec,Decimal('0'))
#
### If a value is None, returns an alternative
#def none2alt(value, alternative):
#    if value==None:
#        return alternative
#    return value
#
def bytes2str(b, code='UTF-8'):
    """
        Bytes 2 string
    """ 
    if b is None:
        return None
    return b.decode(code)
    
def str2bytes(s, code='UTF8'):
    """
        String 2 bytes
    """
    if s is None:
        return None
    else:
        return s.encode(code)

### Returns if a datetime is aware
def is_aware(dt):
    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        return False
    return True

## Returns if a datetime is naive
def is_naive(dt):
    return not is_aware(dt)

## Function to create a datetime aware object
## @param date datetime.date object
## @param hour hour object
## @param tz_name String with datetime tz_name name. For example "Europe/Madrid"
## @return datetime aware
def dtaware(date_, time_, tz_name):
    dt_naive=dtnaive(date_, time_)
    return dtnaive2dtaware(dt_naive, tz_name)

def dtnaive2dtaware(dtnaive, tz_name):
    return dtnaive.replace(tzinfo=ZoneInfo(tz_name))


def dtaware_now(tzname=None):
    """
        If tzname is None: returns UTC dtaware
    """
    utc_aware=dtnaive2dtaware(dtnaive_now(), 'UTC')
    if tzname is None:
        return utc_aware
    else:
        return dtaware_changes_tz(utc_aware, tzname)

def dtnaive_now():
    return datetime.now()

## Function to create a datetime aware object
## @param date datetime.date object
## @param hour hour object
## @return datetime naive
def dtnaive(date_, hour):
    return datetime(date_.year,  date_.month,  date_.day,  hour.hour,  hour.minute,  hour.second, hour.microsecond)


## Returns a date with the first date of the month
## @param year Year to search fist day
## @param month Month to search first day
def date_first_of_the_month(year, month):
    return date(year, month, 1)

## Returns a date with the last date of the month
## @param year Year to search last day
## @param month Month to search last day
def date_last_of_the_month(year, month):
    if month==12:
        return date(year, month, 31)
    return date(year, month+1, 1)-timedelta(days=1)

## Returns a date with the first date of the year
## @param year Year to search first day
def date_first_of_the_year(year):
    return date_first_of_the_month(year, 1)

## Returns a date with the last date of the year
## @param year Year to search last day
def date_last_of_the_year(year):
    return date_last_of_the_month(year,12)

## Returns a date with the first date of the month after x months
## @param year Year to search  day
## @param month Month to search day
## @param x Number of months after parameters. Cab be positive to add months or negative to substract months
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
    first=date_first_of_the_next_x_months(year, month, x)
    return date_last_of_the_month(first.year, first.month)

def dtaware_month_end(year, month, tz_name):
    return dtaware_day_end_from_date(date_last_of_the_month(year, month), tz_name)
    
## Returns an aware datetime with the start of year
def dtaware_year_start(year, tz_name):
    return dtaware_day_start_from_date(date(year, 1, 1), tz_name)
    
## Returns an aware datetime with the last of year
def dtaware_year_end(year, tz_name):
    return dtaware_day_end_from_date(date(year, 12, 31), tz_name)
    
def dtaware_day_end(dt, tz_name):
    """
        Returns the last  datetime (microsecond  level) of the  day in tz_name zone
    """
    if is_naive():
        raise Exception(_("Datetime parameter should be aware"))
    dt=dtaware_changes_tz(dt, tz_name)
    return dt.replace(hour=23, minute=59, second=59, microsecond=999999)
    
def dtnaive_day_end(dt):
    """
        Returns the last  datetime (microsecond  level) of the  day in naive format
    """
    if is_aware(dt):
        raise Exception(_("Datetime parameter should be naive"))
    return dt.replace(hour=23, minute=59, second=59, microsecond=999999)

## Returns the end of the day dtnaive from a date
def dtnaive_day_end_from_date(date_):
    dt=datetime(date_.year, date_.month, date_.day)
    return dtnaive_day_end(dt)

## Returns the end of the day dtaware in utc format
def dtaware_day_end_from_date(date, tz_name):
    return dtaware(date, time(23, 59, 59, 999999), tz_name)
    
## Returns a dtnaive or dtawre (as parameter) with the end of the day
def dtnaive_day_start(dt):
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)

## Returns a dtnaive or dtawre (as parameter) with the end of the day in zone tz_name
def dtaware_day_start(dt, tz_name):
    if is_naive():
        raise Exception(_("Datetime parameter should be aware"))
    dt=dtaware_changes_tz(dt, tz_name)
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)

## Returns the end of the day dtnaive from a date
def dtnaive_day_start_from_date(date_):
    dt=datetime(date_.year, date_.month, date_.day)
    return dtnaive_day_start(dt)

## Returns the end of the day dtaware of the tz_name timezone from a date
def dtaware_day_start_from_date(date, tz_name):
    return dtaware(date, time(0, 0, 0, 0), tz_name)

## Returns the start of a month in utc format
def dtaware_month_start(year, month, tz_name):
    return dtaware_day_start_from_date(date(year, month, 1), tz_name)
#    
#def month2int(s):
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

def str2time(s, format="HH:MM"):
    allowed=["HH:MM", "HH:MM:SS","HH:MMxx"]
    if format in allowed:
        if format=="HH:MM":#12:12
            a=s.split(":")
            return time(int(a[0]), int(a[1]))
        elif format=="HH:MM:SS":#12:12:12
            a=s.split(":")
            return time(int(a[0]), int(a[1]), int(a[2]))
        elif format=="HH:MMxx": #5:12am o pm
            s=s.upper()
            s=s.replace("AM", "")
            if s.find("PM"):
                s=s.replace("PM", "")
                points=s.split(":")
                return time(int(points[0])+12, int(points[1]))
            else:#AM
                points=s.split(":")
                return time(int(points[0]), int(points[1]))
    else:
        raise Exception(_("I can't convert this format '{}'. I only support this {}".format(format, allowed)))

## Converts a time to a string
def time2str(ti, format="HH:MM" ):
    allowed=["HH:MM", "HH:MM:SS","Xulpymoney"]
    if format in allowed:
        if ti==None:
            return None
        if format=="Xulpymoney":
            if ti.microsecond in (4, 5):
                return str(ti)[11:-13]
            else:
                return str(ti)[11:-6]
        elif format=="HH:MM":
            return ("{}:{}".format(str(ti.hour).zfill(2), str(ti.minute).zfill(2)))
        elif format=="HH:MM:SS":
            return ("{}:{}:{}".format(str(ti.hour).zfill(2), str(ti.minute).zfill(2), str(ti.second).zfill(2)))


def str2date(iso, format="YYYY-MM-DD"):
    allowed=["YYYY-MM-DD", "DD/MM/YYYY", "DD.MM.YYYY", "DD/MM"]
    if format in allowed:
        try:
            if format=="YYYY-MM-DD": #YYYY-MM-DD
                d=iso.split("-")
                return date(int(d[0]), int(d[1]),  int(d[2]))
            if format=="DD/MM/YYYY": #DD/MM/YYYY
                d=iso.split("/")
                return date(int(d[2]), int(d[1]),  int(d[0]))
            if format=="DD.MM.YYYY": #DD.MM.YYYY
                d=iso.split(".")
                return date(int(d[2]), int(d[1]),  int(d[0]))
            if format=="DD/MM": #DD/MM
                d=iso.split("/")
                return date(date.today().year, int(d[1]),  int(d[0]))
        except:
            return None
    else:
        raise Exception("I can't convert this format '{}'. I only support this {}".format(format, allowed))

def str2dtnaive(s, format):
    allowed=["%Y%m%d%H%M","%Y-%m-%d %H:%M:%S","%d/%m/%Y %H:%M","%d %m %H:%M %Y","%Y-%m-%d %H:%M:%S.","%H:%M:%S", '%b %d %H:%M:%S']
    if format in allowed:
        if format=="%Y%m%d%H%M":
            dat=datetime.strptime( s, format )
            return dat
        if format=="%Y-%m-%d %H:%M:%S":#2017-11-20 23:00:00
            return datetime.strptime( s, format )
        if format=="%d/%m/%Y %H:%M":#20/11/2017 23:00
            return datetime.strptime( s, format )
        if format=="%d %m %H:%M %Y":#27 1 16:54 2017. 1 es el mes convertido con month2int
            return datetime.strptime( s, format)
        if format=="%Y-%m-%d %H:%M:%S.":#2017-11-20 23:00:00.000000  ==>  microsecond. Notice the point in format
            arrPunto=s.split(".")
            s=arrPunto[0]
            micro=int(arrPunto[1]) if len(arrPunto)==2 else 0
            dt=datetime.strptime( s, "%Y-%m-%d %H:%M:%S" )
            dt=dt+timedelta(microseconds=micro)
            return dt
        if format=="%H:%M:%S": 
            tod=date.today()
            a=s.split(":")
            return datetime(tod.year, tod.month, tod.day, int(a[0]), int(a[1]), int(a[2]))
        if format=='%b %d %H:%M:%S': #Apr 26 07:50:44. Year is missing so I set to current
            s=f"{date.today().year} {s}"
            return datetime.strptime(s, '%Y %b %d %H:%M:%S')
    else:
        raise Exception("I can't convert this format '{}'. I only support this {}".format(format, allowed))

def str2dtaware(s, format, tz_name='UTC'):
    allowed=["%Y-%m-%d %H:%M:%S%z","%Y-%m-%d %H:%M:%S.%z", "JsUtcIso"]
    if format in allowed:
        if format=="%Y-%m-%d %H:%M:%S%z":#2017-11-20 23:00:00+00:00
            s=s[:-3]+s[-2:]
            dt=datetime.strptime( s, format )
            return dtaware_changes_tz(dt, tz_name)
        if format=="%Y-%m-%d %H:%M:%S.%z":#2017-11-20 23:00:00.000000+00:00  ==>  microsecond. Notice the point in format
            s=s[:-3]+s[-2:]#quita el :
            arrPunto=s.split(".")
            s=arrPunto[0]+s[-5:]
            micro=int(arrPunto[1][:-5])
            dt=datetime.strptime( s, "%Y-%m-%d %H:%M:%S%z" )
            dt=dt+timedelta(microseconds=micro)
            return dtaware_changes_tz(dt, tz_name)
        if format=="JsUtcIso": #2021-08-21T06:27:38.294Z
            s=s.replace("T"," ").replace("Z","")
            dtnaive=str2dtnaive(s,"%Y-%m-%d %H:%M:%S.")
            dtaware_utc=dtnaive2dtaware(dtnaive, 'UTC')
            return dtaware_changes_tz(dtaware_utc, tz_name)

#    else:
#        return timezone(tz_name).localize(str2dtnaive(s,format))

## epoch is the time from 1,1,1970 in UTC
## return now(timezone(self.name))
def dtaware2epochms(d):
    return d.timestamp()*1000
    
## Return a UTC datetime aware
def epochms2dtaware(n, tz="UTC"):
    utc_unaware=datetime.utcfromtimestamp(n/1000)
    utc_aware=utc_unaware.replace(tzinfo=ZoneInfo('UTC'))#Due to epoch is in UTC
    return dtaware_changes_tz(utc_aware, tz)

## epoch is the time from 1,1,1970 in UTC
## return now(timezone(self.name))
def dtaware2epochmicros(d):
    return int(d.timestamp()*1000000)
## Return a UTC datetime aware
def epochmicros2dtaware(n, tz="UTC"):
    utc_unaware=datetime.utcfromtimestamp(n/1000000)
    utc_aware=utc_unaware.replace(tzinfo=ZoneInfo('UTC'))#Due to epoch is in UTC
    return dtaware_changes_tz(utc_aware, tz)


## Returns a formated string of a dtaware string formatting with a zone name
## @param dt datetime aware object
## @return String
def dtaware2str(dt, format):
    if is_naive(dt)==True:
        raise Exception("A dtaware is needed for {}".format(dt))
    else:
        return dtnaive2str(dt, format)

## Returns a formated string of a dtaware string formatting with a zone name
## @param dt datetime aware object
## @param format String in ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y%m%d %H%M", "%Y%m%d%H%M"]
## @return String
def dtnaive2str(dt, format):
    allowed=["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y%m%d %H%M", "%Y%m%d%H%M", "JsUtcIso"]
    if dt==None:
        return "None"
    elif format in allowed:
        if format=="%Y-%m-%d":
            return dt.strftime("%Y-%m-%d")
        elif format=="%Y-%m-%d %H:%M:%S": 
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        elif format=="%Y%m%d %H%M": 
            return dt.strftime("%Y%m%d %H%M")
        elif format=="%Y%m%d%H%M":
            return dt.strftime("%Y%m%d%H%M")
        elif format=="JsUtcIso":
            return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        raise Exception("I can't convert this format '{}'. I only support this {}".format(format, allowed))

## Changes zoneinfo from a dtaware object
## For example:
## - datetime.datetime(2018, 5, 18, 8, 12, tzinfo=<DstTzInfo 'Europe/Madrid' CEST+2:00:00 DST>)
## - libcaloriestrackerfunctions.dtaware_changes_tz(a,"Europe/London")
## - datetime.datetime(2018, 5, 18, 7, 12, tzinfo=<DstTzInfo 'Europe/London' BST+1:00:00 DST>)
## @param dt datetime aware object
## @param tzname String with datetime zone. For example: "Europe/Madrid"
## @return datetime aware object
def dtaware_changes_tz(dt,  tzname):
    if dt==None:
        return None
    if is_aware(dt):
        return dt.astimezone(ZoneInfo(tzname))
    else:
        raise Exception("Dtaware needed")

## Returns a list of tuples (year, month) from a month to another month, both included
## @param year_from Integer
## @param month_from Integer
## @param year_to Integer If none uses current year
## @param month_to Integer If none uses current month
def months(year_from, month_from, year_to=None, month_to=None):
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
