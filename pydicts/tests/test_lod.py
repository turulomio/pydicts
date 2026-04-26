from datetime import datetime, date
from decimal import Decimal
from pydicts import lod, currency, percentage
from collections import OrderedDict # Import OrderedDict
from pytest import raises, fixture

@fixture
def sample_lod():
    lod_ = []
    lod_.append({"a": datetime.now(), "b": date.today(), "c": Decimal('12.32'), "d": None, "e": int(12), "f":None, "g":True, "h":False, "i": currency.Currency(0.12, 'EUR'), "j": 0.12345}) # d is None
    lod_.append({"a": datetime.now(), "b": date.today(), "c": Decimal('-12.32'), "d": 16, "e": int(12), "f":None, "g":True, "h":False, "i": currency.Currency(0.12345, 'EUR'), "j": 123.12}) # d is 16
    return lod_

@fixture
def another_lod():
    return [
        {"id": 1, "name": "Alice", "age": 30, "city": "NY"},
        {"id": 2, "name": "Bob", "age": 25, "city": "LA"},
        {"id": 3, "name": "Charlie", "age": 35, "city": "NY"},
        {"id": 4, "name": "Alice", "age": 30, "city": "NY"}, # Duplicate
        {"id": 5, "name": "David", "age": None, "city": "SF"},
        {"id": 6, "name": "Eve", "age": 28, "city": None},
    ]

@fixture
def empty_lod():
    return []

def tests_dictkv(sample_lod):
    d=lod.lod2dictkv(sample_lod, "a","b")
    assert list(d.values())[0]==date.today()
    
def test_lod_order_by(another_lod):
    # Order by age, ascending, None at top (default)
    ordered_lod = lod.lod_order_by(another_lod, "age")
    assert ordered_lod[0]["name"] == "David" # None age
    assert ordered_lod[1]["name"] == "Bob" # 25
    assert ordered_lod[2]["name"] == "Eve" # 28

    # Order by age, descending, None at bottom
    ordered_lod_desc_none_bottom = lod.lod_order_by(another_lod, "age", reverse=True, none_at_top=False)
    assert ordered_lod_desc_none_bottom[0]["name"] == "Charlie" # 35
    assert ordered_lod_desc_none_bottom[-1]["name"] == "David" # None age

    # Order by name, ascending
    ordered_lod_name = lod.lod_order_by(another_lod, "name")
    assert ordered_lod_name[0]["name"] == "Alice"
    assert ordered_lod_name[1]["name"] == "Alice"
    assert ordered_lod_name[2]["name"] == "Bob"

def tests_lod_has_key(sample_lod, empty_lod):
    assert lod.lod_has_key(sample_lod,"c")==True
    assert lod.lod_has_key(sample_lod,"cc")==False
    assert lod.lod_has_key(empty_lod, "c")==False
    
def test_lod_print(sample_lod):
    # This test primarily checks if the function runs without error
    # Actual output assertion is difficult for print functions
    lod.lod_print(sample_lod)
    lod.lod_print(sample_lod, number=1)
    lod.lod_print(sample_lod, align=["left","center","right"]*3+["decimal"])

def test_lod_print_empty(empty_lod, capsys):
    lod.lod_print(empty_lod)
    captured = capsys.readouterr()
    assert "This list of dictionaries hasn't data to print" in captured.out

def test_lod_print_zero_rows(sample_lod, capsys):
    lod.lod_print(sample_lod, number=0)
    captured = capsys.readouterr()
    # Assert against the English translation, as the _() function is active
    assert "No data was printed due to you selected 0 rows" in captured.out
def test_lod_sum(sample_lod):
    assert lod.lod_sum(sample_lod, "c")==0
    assert lod.lod_sum(sample_lod, "d")==16
    with raises(TypeError) as excinfo:
        lod.lod_sum(sample_lod, "d", ignore_nones=False)
    assert "NoneType" in str(excinfo.value)
    assert lod.lod_sum(sample_lod, "d", ignore_nones=True) == 16
    
def test_lod_average(sample_lod):
    # lod.lod_print(sample_lod) # Remove debug print
    assert lod.lod_average(sample_lod,"c")==0
    assert lod.lod_average(sample_lod,"d")==8

def test_lod_average_ponderated(sample_lod):
    assert lod.lod_average_ponderated(sample_lod,"e", "c")==0
    
def test_lod_median(sample_lod):
    assert lod.lod_median(sample_lod,"c")==0
    
def tests_lod_sum_positives(sample_lod):
    assert lod.lod_sum_positives(sample_lod, "c")==Decimal("12.32")
    assert lod.lod_sum_positives(sample_lod, "d")==16
    
def tests_lod_sum_negatives(sample_lod):
    assert lod.lod_sum_negatives(sample_lod, "c")==Decimal("-12.32")
    assert lod.lod_sum_negatives(sample_lod, "d")==0
    
def test_lod_remove_duplicates(another_lod):
    # Test with a list containing duplicates
    lod_=[
        {"a":1,  "b":2}, 
        {"a":1,  "b":2}, 
        {"a":1,  "b":2}, 
    ]
    lod_=lod.lod_remove_duplicates(lod_)
    assert len(lod_)==1
    # Test with another_lod which has one duplicate
    # Note: The original another_lod has unique 'id's, so all entries are unique. The comment was misleading.
    unique_lod = lod.lod_remove_duplicates(another_lod)
    assert len(unique_lod) == 6 # All entries are unique due to 'id'
    assert unique_lod[0]["id"] == 1
    assert unique_lod[3]["id"] == 4 # This is the 4th item in the original list

def test_lod_rename_key(sample_lod): # Renamed tests_lod_rename_key to test_lod_rename_key for consistency
    cloned_lod = lod.lod_clone(sample_lod) # Clone to avoid modifying original fixture
    lod.lod_rename_key(cloned_lod, "c", "new_c")
    assert not lod.lod_has_key(cloned_lod, "c")
    assert lod.lod_has_key(cloned_lod, "new_c")
    assert cloned_lod[0]["new_c"] == Decimal('12.32')

def test_lod_remove_key(sample_lod):
    cloned_lod = lod.lod_clone(sample_lod) # Clone to avoid modifying original fixture
    assert lod.lod_has_key(cloned_lod, "d")
    lod.lod_remove_key(cloned_lod, "d")
    assert not lod.lod_has_key(cloned_lod, "d")
    # Ensure other keys are still there
    assert lod.lod_has_key(cloned_lod, "a")

def test_lod_keys(sample_lod, empty_lod):
    keys = lod.lod_keys(sample_lod)
    assert isinstance(keys, list)
    assert "a" in keys
    assert "c" in keys
    assert lod.lod_keys(empty_lod) is None

def test_lod_clone(sample_lod):
    cloned_lod = lod.lod_clone(sample_lod)
    assert cloned_lod == sample_lod # Content is the same
    assert cloned_lod is not sample_lod # It's a new list object
    assert cloned_lod[0] is not sample_lod[0] # Inner dictionaries are also new objects
    cloned_lod[0]["c"] = Decimal("999")
    assert sample_lod[0]["c"] != Decimal("999") # Ensure deep copy for dicts

def test_lod_filter_keys(sample_lod):
    new_lod=lod.lod_filter_keys(sample_lod,  ["g", "h"])
    assert "a" not in lod.lod_keys(new_lod)
    assert "g" in lod.lod_keys(new_lod)
    assert "h" in lod.lod_keys(new_lod)
    assert len(new_lod[0]) == 2

def test_lod_filter_dictionaries(sample_lod):
    #Filtering by index
    new_lod=lod.lod_filter_dictionaries(sample_lod, lambda d,  index: index==1)
    # lod.lod_print(new_lod) # Remove debug print
    assert len(new_lod)==1
    assert new_lod[0]["d"] == 16
    
    #Filtering by d
    new_lod=lod.lod_filter_dictionaries(sample_lod, lambda d,  index: d["g"] is None)
    assert len(new_lod)==0

    # Filtering by value
    new_lod = lod.lod_filter_dictionaries(sample_lod, lambda d, index: d["c"] > 0)
    assert len(new_lod) == 1
    assert new_lod[0]["c"] == Decimal('12.32')

def test_calculate_clone(sample_lod):
    new_lod=lod.lod_calculate(sample_lod, "NEW C",   lambda d,  index: d['c']*100, clone=True)
    # lod.lod_print(new_lod) # Remove debug print
    assert "NEW C" in lod.lod_keys(new_lod)
    assert "NEW C" not in lod.lod_keys(sample_lod) # Ensure original lod_ is not modified
    assert new_lod[0]["NEW C"] == Decimal('1232.00')

def test_calculate(sample_lod):
    new_lod=lod.lod_calculate(sample_lod, "NEW C",   lambda d,  index: d['c']*100)
    # lod.lod_print(new_lod) # Remove debug print
    assert "NEW C" in lod.lod_keys(new_lod)
    assert "NEW C" in lod.lod_keys(sample_lod) # Ensure original lod_ is modified
    assert new_lod[0]["NEW C"] == Decimal('1232.00')

def test_lod2dod(sample_lod):
    dod_=lod.lod2dod(sample_lod, "c")
    # print(dod_) # Remove debug print
    assert dod_[Decimal("12.32")]==sample_lod[0]
    assert dod_[Decimal("-12.32")]==sample_lod[1]
    assert len(dod_) == 2

def test_lod2odod(sample_lod):
    odod_ = lod.lod2odod(sample_lod, "c")
    assert isinstance(odod_, OrderedDict) # Now OrderedDict is imported
    assert list(odod_.keys()) == [Decimal("12.32"), Decimal("-12.32")]
    assert odod_[Decimal("12.32")] == sample_lod[0]

def test_lod2dod_tuple(sample_lod):
    dod_tuple = lod.lod2dod_tuple(sample_lod, "g", "h")
    # Both dictionaries in sample_lod have (True, False) for "g", "h". lod2dod_tuple will overwrite entries with the same key, so it will contain the last one.
    # The previous error was due to sample_lod[1]["i"] being a string, causing comparison issues.
    assert dod_tuple[(True, False)] == sample_lod[1]
    assert len(dod_tuple) == 1 # Both sample_lod items have (True, False) for g, h

def test_dod2lod(sample_lod):
    dod_=lod.lod2dod(sample_lod, "c")
    assert sample_lod==lod.dod2lod(dod_)

def test_lod2list(sample_lod):
    # Test basic extraction
    c_list = lod.lod2list(sample_lod, "c")
    assert c_list == [Decimal('12.32'), Decimal('-12.32')]

    # Test sorted
    c_list_sorted = lod.lod2list(sample_lod, "c", sorted=True)
    assert c_list_sorted == [Decimal('-12.32'), Decimal('12.32')]

    # Test cast
    c_list_str = lod.lod2list(sample_lod, "c", cast="str")
    assert c_list_str == ["12.32", "-12.32"]

def test_lod2list_distinct(another_lod):
    names = lod.lod2list_distinct(another_lod, "name", sorted=True)
    assert len(names) == 5

    cities = lod.lod2list_distinct(another_lod, "city", sorted=True)
    assert cities == [None, "LA", "NY", "SF"] # None is now handled by custom sort in lod2list_distinct

def test_lod2lol(sample_lod):
    lol_data = lod.lod2lol(sample_lod, keys=["c", "d"])
    assert lol_data == [[Decimal('12.32'), None], [Decimal('-12.32'), 16]]
    assert len(lol_data) == 2
    assert len(lol_data[0]) == 2

def test_lod2lood(sample_lod):
    lood_data = lod.lod2lood(sample_lod, keys=["c", "d"])
    assert len(lood_data) == 2
    assert isinstance(lood_data[0], OrderedDict) # Now OrderedDict is imported
    assert list(lood_data[0].keys()) == ["c", "d"]
    assert lood_data[0]["c"] == Decimal('12.32')

def test_lod_max_value(another_lod, empty_lod):
    assert lod.lod_max_value(another_lod, "age") == 35 # None values are now ignored
    assert lod.lod_max_value(another_lod, "id") == 6
    assert lod.lod_max_value(empty_lod, "age") is None

def test_lod_min_value(another_lod, empty_lod):
    assert lod.lod_min_value(another_lod, "age") == 25 # None values are now ignored
    assert lod.lod_min_value(another_lod, "id") == 1
    assert lod.lod_min_value(empty_lod, "age") is None

def test_lod_count(sample_lod):
    assert lod.lod_count(sample_lod,lambda d, index: d["c"]>0)==1, "Error counting"
    assert lod.lod_count(sample_lod,lambda d, index: d["f"] is None)==2, "Error counting"
    assert lod.lod_count(sample_lod,lambda d, index: index>0)==1, "Error counting"