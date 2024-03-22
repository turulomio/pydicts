from datetime import datetime, date
from decimal import Decimal
from pydicts import dod
from pytest import fixture

empty_lod=[]

@fixture(autouse=True)
def reload_lod_():
    d={"a": datetime.now(), "b": date.today(), "c": Decimal('12.32'), "d": None, "e": int(12), "f":None, "g":True, "h":False,  "nested": {"x":1, "y":2, "z":{"n":4, "m":5, "o":6}}}
    global dod_
    dod_={}
    dod_["first"]=d
    dod_["second"]=d


def test_dod_print():
    dod.dod_print(dod_)
