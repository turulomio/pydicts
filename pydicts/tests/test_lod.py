from pydicts.lod import lod2dictkv, lod_has_key, lod_sum

from datetime import datetime, date
from decimal import Decimal
from pytest import raises

empty_lod=[]

lod=[]
lod.append({"a": datetime.now(), "b": date.today(), "c": Decimal('12.32'), "d": None, "e": int(12), "f":None, "g":True, "h":False})
lod.append({"a": datetime.now(), "b": date.today(), "c": Decimal('-12.32'), "d": 16, "e": int(12), "f":None, "g":True, "h":False})


def tests_dictkv():
    d=lod2dictkv(lod, "a","b")
    assert list(d.values())[0]==date.today()
    

def tests_lod_has_key():
    assert lod_has_key(lod,"c")==True
    assert lod_has_key(lod,"cc")==False
    assert lod_has_key(empty_lod, "c")==False
    
def tests_lod_sum():
    assert lod_sum(lod, "c")==0
    assert lod_sum(lod, "d")==16
    with raises(TypeError) as excinfo:
        lod_sum(lod, "d", ignore_nones=False)==16
    assert "NoneType" in str(excinfo.value)
