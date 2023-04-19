from datetime import datetime, date
from decimal import Decimal
from pydicts import lod
from pytest import raises

empty_lod=[]

lod_=[]
lod_.append({"a": datetime.now(), "b": date.today(), "c": Decimal('12.32'), "d": None, "e": int(12), "f":None, "g":True, "h":False})
lod_.append({"a": datetime.now(), "b": date.today(), "c": Decimal('-12.32'), "d": 16, "e": int(12), "f":None, "g":True, "h":False})


def tests_dictkv():
    d=lod.lod2dictkv(lod_, "a","b")
    assert list(d.values())[0]==date.today()
    

def tests_lod_has_key():
    assert lod.lod_has_key(lod_,"c")==True
    assert lod.lod_has_key(lod_,"cc")==False
    assert lod.lod_has_key(empty_lod, "c")==False
    
def tests_lod_sum():
    assert lod.lod_sum(lod_, "c")==0
    assert lod.lod_sum(lod_, "d")==16
    with raises(TypeError) as excinfo:
        lod.lod_sum(lod_, "d", ignore_nones=False)==16
    assert "NoneType" in str(excinfo.value)
    
def test_lod_remove_key():
    assert lod.lod_has_key(lod_, "d")
    lod.lod_remove_key(lod_, "d")
    assert not lod.lod_has_key(lod_, "d")
    
