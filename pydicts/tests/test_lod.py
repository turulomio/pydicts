from datetime import datetime, date
from decimal import Decimal
from pydicts import lod, currency, percentage
from pytest import raises, fixture

empty_lod=[]

@fixture(autouse=True)
def reload_lod_():
    global lod_
    lod_=[]
    lod_.append({"a": datetime.now(), "b": date.today(), "c": Decimal('12.32'), "d": None, "e": int(12), "f":None, "g":True, "h":False, "i": currency.Currency(0.12, 'EUR'), "j": 0.12345})
    lod_.append({"a": datetime.now(), "b": date.today(), "c": Decimal('-12.32'), "d": 16, "e": int(12), "f":None, "g":True, "h":False, "i": currency.Currency(0.12345, 'EUR').string(5), "j": 123.12})


def tests_dictkv():
    d=lod.lod2dictkv(lod_, "a","b")
    assert list(d.values())[0]==date.today()
    

def tests_lod_has_key():
    assert lod.lod_has_key(lod_,"c")==True
    assert lod.lod_has_key(lod_,"cc")==False
    assert lod.lod_has_key(empty_lod, "c")==False
    
def test_remove_duplicates():
    lod_=[
        {"a":1,  "b":2}, 
        {"a":1,  "b":2}, 
        {"a":1,  "b":2}, 
    ]
    lod_=lod.lod_remove_duplicates(lod_)
    assert len(lod_)==1
    
def tests_lod_sum():
    assert lod.lod_sum(lod_, "c")==0
    assert lod.lod_sum(lod_, "d")==16
    with raises(TypeError) as excinfo:
        lod.lod_sum(lod_, "d", ignore_nones=False)==16
    assert "NoneType" in str(excinfo.value)
    
def test_lod_average():
    lod.lod_print(lod_)
    assert lod.lod_average(lod_,"c")==0
    assert lod.lod_average(lod_,"d")==8

def test_lod_average_ponderated():
    assert lod.lod_average_ponderated(lod_,"e", "c")==0
    
def test_lod_median():
    assert lod.lod_median(lod_,"c")==0
    
def tests_lod_sum_positives():
    assert lod.lod_sum_positives(lod_, "c")==Decimal("12.32")
    assert lod.lod_sum_positives(lod_, "d")==16
    
def tests_lod_sum_negatives():
    assert lod.lod_sum_negatives(lod_, "c")==Decimal("-12.32")
    assert lod.lod_sum_negatives(lod_, "d")==0
    
def test_lod_remove_key():
    assert lod.lod_has_key(lod_, "d")
    lod.lod_remove_key(lod_, "d")
    assert not lod.lod_has_key(lod_, "d")
    
def test_lod_filter_keys():
    new_lod=lod.lod_filter_keys(lod_,  ["g", "h"])
    assert "a" not in lod.lod_keys(new_lod)
    assert "g" in lod.lod_keys(new_lod)
    assert "h" in lod.lod_keys(new_lod)


def test_lod_filter_dictionaries():
    #Filtering by index
    new_lod=lod.lod_filter_dictionaries(lod_, lambda d,  index: index==1)
    lod.lod_print(new_lod)
    assert len(new_lod)==1
    
    #Filtering by d
    new_lod=lod.lod_filter_dictionaries(lod_, lambda d,  index: d["g"] is None)
    assert len(new_lod)==0

def test_calculate_clone():
    new_lod=lod.lod_calculate(lod_, "NEW C",   lambda d,  index: d['c']*100, clone=True)
    lod.lod_print(new_lod)
    assert "NEW C" in lod.lod_keys(new_lod)
    assert "NEW C" not in lod.lod_keys(lod_)
    
def test_calculate():
    new_lod=lod.lod_calculate(lod_, "NEW C",   lambda d,  index: d['c']*100)
    lod.lod_print(new_lod)
    assert "NEW C" in lod.lod_keys(new_lod)
    assert "NEW C" in lod.lod_keys(lod_)
    
def test_lod2dod():
    dod_=lod.lod2dod(lod_, "c")
    print(dod_)
    assert dod_[Decimal("12.32")]==lod_[0]

def test_dod2lod():
    dod_=lod.lod2dod(lod_, "c")
    assert lod_==lod.dod2lod(dod_)

def test_lod_count():
    assert lod.lod_count(lod_,lambda d, index: d["c"]>0)==1, "Error counting"
    assert lod.lod_count(lod_,lambda d, index: d["f"] is None)==2, "Error counting"
    assert lod.lod_count(lod_,lambda d, index: index>0)==1, "Error counting"

def test_lod_print():
    lod.lod_print(lod_, align=["left","center","right"]*3+["decimal"])