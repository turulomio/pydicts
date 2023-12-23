from decimal import Decimal
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo
from pydicts import myjsonencoder

d={}
d["None"]=None
d["Boolean"]=True
d["Integer"]=12112
d["Float"]=12121.1212
d["Date"]=date.today()
d["Datetime"]=datetime.now()
d["Timedelta"]=timedelta(days=396, hours=4, minutes=12,  seconds=12, microseconds=121212)
d["Time"]=time(12, 12, 12, 123456)
d["Datetime aware"]=d["Datetime"].replace(tzinfo=ZoneInfo("UTC"))
d["Bytes"]=b"Byte array"
d["Decimal"]=Decimal("12.12123414")


def test_myjsonencoder():
    print("DICCIONARIO", d)
    json_string=myjsonencoder.MyJSONEncoder_dumps(d)
    print("Antes",  json_string)
    json_=myjsonencoder.MyJSONEncoder_loads(json_string)
    print("Despues", json_)
    assert json_["None"]==d["None"]
    assert json_["Integer"]==d["Integer"]
    assert json_["Float"]==d["Float"]
    assert json_["Date"]==d["Date"]
    assert json_["Datetime"]==d["Datetime"]
    assert json_["Datetime aware"]==d["Datetime aware"]
    assert json_["Bytes"]==d["Bytes"]
    assert json_["Decimal"]==d["Decimal"]
    assert json_["Time"]==d["Time"]
    assert json_["Timedelta"]==d["Timedelta"] 

def test_myjsonencoder_decimals_as_float():
    json_string=myjsonencoder.MyJSONEncoderDecimalsAsFloat_dumps(d)
    json_=myjsonencoder.MyJSONEncoderDecimalsAsFloat_loads(json_string)
    assert json_["None"]==d["None"]
    assert json_["Integer"]==d["Integer"]
    assert json_["Float"]==d["Float"]
    assert json_["Date"]==d["Date"]
    assert json_["Datetime"]==d["Datetime"]
    assert json_["Datetime aware"]==d["Datetime aware"]
    assert json_["Bytes"]==d["Bytes"]
    assert json_["Decimal"]==float(d["Decimal"])
    assert json_["Time"]==d["Time"]
    assert json_["Timedelta"]==d["Timedelta"] 


def test_myjsonencoder_decimals_as_string():
    json_string=myjsonencoder.MyJSONEncoderDecimalsAsString_dumps(d)
    json_=myjsonencoder.MyJSONEncoderDecimalsAsString_loads(json_string)
    assert json_["None"]==d["None"]
    assert json_["Integer"]==d["Integer"]
    assert json_["Float"]==d["Float"]
    assert json_["Date"]==d["Date"]
    assert json_["Datetime"]==d["Datetime"]
    assert json_["Datetime aware"]==d["Datetime aware"]
    assert json_["Bytes"]==d["Bytes"]
    assert json_["Decimal"]==str(d["Decimal"])
    assert json_["Time"]==d["Time"]
    assert json_["Timedelta"]==d["Timedelta"] 
