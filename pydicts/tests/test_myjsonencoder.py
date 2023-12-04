from decimal import Decimal
from datetime import timezone, date, datetime, time, timedelta
from pydicts import myjsonencoder
def test_myjsonencoder():
    d={}
    d["None"]=None
    d["Integer"]=12112
    d["Float"]=12121.1212
    d["Date"]=date.today()
    d["Datetime"]=datetime.now()
    d["Timedelta"]=timedelta(hours=4, days=2, minutes=12,  seconds=12)
    d["Time"]=time(12, 12, 12, 123456)
    d["Datetime aware"]=d["Datetime"].replace(tzinfo=timezone.utc)
    d["Bytes"]=b"Byte array"
    d["Decimal"]=Decimal("12.12123414")
    print ("Dictionary")
    print(d)
    print()
    print ("MyJSONEncoder_dumps")
    print (myjsonencoder.MyJSONEncoder_dumps(d))
    print()
    print ("MyJSONEncoder_loads")
    print(myjsonencoder.MyJSONEncoder_loads(myjsonencoder.MyJSONEncoder_dumps(d)))
    print()
    print ("MyJSONEncoderDecimalsAsFloat_dumps")
    print (myjsonencoder.MyJSONEncoderDecimalsAsFloat_dumps(d))
    print()
    print ("MyJSONEncoderDecimalsAsFloat_loads")
    print(myjsonencoder.MyJSONEncoderDecimalsAsFloat_loads(myjsonencoder.MyJSONEncoderDecimalsAsFloat_dumps(d)))
    print()
    print ("MyJSONEncoderDecimalsAsString_dumps")
    print (myjsonencoder.MyJSONEncoderDecimalsAsString_dumps(d))
    print()
    print ("MyJSONEncoderDecimalsAsString_loads")
    print(myjsonencoder.MyJSONEncoderDecimalsAsString_loads(myjsonencoder.MyJSONEncoderDecimalsAsString_dumps(d)))
    print()
