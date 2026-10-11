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
    """
    Tests the MyJSONEncoder and MyJSONEncoder_loads functions for correct serialization and deserialization of various Python types.
    """
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
    """
    Tests the MyJSONEncoderDecimalsAsFloat_dumps and MyJSONEncoderDecimalsAsFloat_loads functions.
    Ensures Decimal objects are serialized as floats and deserialized correctly (though with potential precision loss).
    """
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
    """
    Tests the MyJSONEncoderDecimalsAsString_dumps and MyJSONEncoderDecimalsAsString_loads functions.
    Ensures Decimal objects are serialized as strings and deserialized correctly.
    """
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

def test_myjsonencoder_percentage_and_currency():
    """
    Tests serialization and deserialization of Currency and Percentage objects,
    nested structures, timezone-aware time validation, and unhandled custom classes.
    """
    from pydicts.currency import Currency
    from pydicts.percentage import Percentage
    import pytest

    data = {
        "cur": Currency(50, "EUR"),
        "pct": Percentage(0.25, 1),
        "nested": {
            "inner_cur": Currency(10, "EUR"),
            "items": ["a", "b"]
        },
        "list_of_items": [{"x": 1}, {"y": 2}]
    }
    encoded = myjsonencoder.MyJSONEncoder_dumps(data)
    decoded = myjsonencoder.MyJSONEncoder_loads(encoded)
    assert decoded["nested"]["inner_cur"] == Decimal("10")
    assert decoded["pct"] == Decimal("0.25")

    # Test timezone-aware time raises ValueError
    aware_time = time(12, 0, 0, tzinfo=ZoneInfo("UTC"))
    with pytest.raises(ValueError):
        myjsonencoder.MyJSONEncoder_dumps({"t": aware_time})

    # Test unknown object falls back to super().default()
    class CustomObj:
        pass
    with pytest.raises(TypeError):
        myjsonencoder.MyJSONEncoder_dumps({"c": CustomObj()})

