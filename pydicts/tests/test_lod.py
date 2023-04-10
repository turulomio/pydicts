from pydicts.lod import lod2dictkv

from datetime import datetime, date
from decimal import Decimal

def tests_dictkv():
    ld=[]
    ld.append({"a": datetime.now(), "b": date.today(), "c": Decimal(12.32), "d": None, "e": int(12), "f":None, "g":True, "h":False})

    d=lod2dictkv(ld, "a","b")
    
    assert list(d.values())[0]==date.today()
    
