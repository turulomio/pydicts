from decimal import Decimal
from pydicts import lod_ymv
import pytest

# Helper function to create a full year dictionary for tests
def _create_full_year_dict(year, values_by_month=None, total=0):
    d = {"year": year}
    values_by_month = values_by_month or {}
    for i in range(1, 13):
        d[f"m{i}"] = values_by_month.get(i, 0)
    d["total"] = total
    return d
def test_lod_ymv_transposition():
    o=[
        {"year": 2022, "month": 1, "my_sum": 12},
        {"year": 2021, "month": 2, "my_sum": 123},
        {"year": 2019, "month": 5, "my_sum": 1},
        {"year": 2022, "month": 12, "my_sum": 12},
        {"year": 2022, "month": 1, "my_sum": 8}, # Duplicate month/year, should sum
        {"year": 2020, "month": 3, "my_sum": 50},
        {"year": 2020, "month": 4, "my_sum": 20},
    ]
    t=lod_ymv.lod_ymv_transposition(o,key_value="my_sum")

    # Expected structure:
    # 2019: m5=1, total=1
    # 2020: m3=50, m4=20, total=70
    # 2021: m2=123, total=123
    # 2022: m1=12+8=20, m12=12, total=32

    assert len(t) == 4 # Years 2019, 2020, 2021, 2022

    # Year 2019
    y2019 = t[0]
    assert y2019["year"] == 2019
    assert y2019["m5"] == 1
    assert y2019["total"] == 1
    assert all(y2019[f"m{i}"] == 0 for i in range(1, 13) if i != 5)

    # Year 2020
    y2020 = t[1]
    assert y2020["year"] == 2020
    assert y2020["m3"] == 50
    assert y2020["m4"] == 20
    assert y2020["total"] == 70
    assert all(y2020[f"m{i}"] == 0 for i in range(1, 13) if i not in [3, 4])

    # Year 2021
    y2021 = t[2]
    assert y2021["year"] == 2021
    assert y2021["m2"] == 123
    assert y2021["total"] == 123
    assert all(y2021[f"m{i}"] == 0 for i in range(1, 13) if i != 2)

    # Year 2022
    y2022 = t[3]
    assert y2022["year"] == 2022
    assert y2022["m1"] == 20 # 12 + 8
    assert y2022["m12"] == 12
    assert y2022["total"] == 32
    assert all(y2022[f"m{i}"] == 0 for i in range(1, 13) if i not in [1, 12])

    # Test with empty input
    assert lod_ymv.lod_ymv_transposition([], key_value="my_sum") == []

    # Test with missing keys
    o_bad_key = [{"year": 2022, "month": 1, "bad_key": 10}]
    assert lod_ymv.lod_ymv_transposition(o_bad_key, key_value="my_sum") is None

def test_is_noz():
    assert lod_ymv.is_noz(None) is True
    assert lod_ymv.is_noz(0) is True
    assert lod_ymv.is_noz(Decimal('0')) is True
    assert lod_ymv.is_noz(1) is False
    assert lod_ymv.is_noz(Decimal('1')) is False
    assert lod_ymv.is_noz("hello") is False
    assert lod_ymv.is_noz("") is False
    assert lod_ymv.is_noz([]) is False

def test_ymv_transposition_first_value_not_noz():
    # Use the helper to create complete dictionaries
    lod_data = [
        _create_full_year_dict(2020, {3: 10, 4: 20}),
        _create_full_year_dict(2021, {1: 30, 2: 40, 3: 50, 4: 60}),
    ]
    result = lod_ymv.ymv_transposition_first_value_not_noz(lod_data)
    assert result == {"year": 2020, "month": 3, "value": 10}

    lod_data_all_zero = [
        _create_full_year_dict(2020),
        _create_full_year_dict(2021),
    ]
    result_all_zero = lod_ymv.ymv_transposition_first_value_not_noz(lod_data_all_zero)
    assert result_all_zero is None

    lod_data_empty = []
    result_empty = lod_ymv.ymv_transposition_first_value_not_noz(lod_data_empty)
    assert result_empty is None
    lod_data_first_month = [
        _create_full_year_dict(2020, {1: 5}),
    ]
    result_first_month = lod_ymv.ymv_transposition_first_value_not_noz(lod_data_first_month)
    assert result_first_month == {"year": 2020, "month": 1, "value": 5}
def test_d_ymv_transposition_first_key_not_noz():
    d1 = _create_full_year_dict(0, {2: 10, 3: 20, 6: 30}, total=60)
    assert lod_ymv.d_ymv_transposition_first_key_not_noz(d1) == "m2"
    d2 = _create_full_year_dict(0, {1: 5, 2: 10, 3: 20}, total=35)
    assert lod_ymv.d_ymv_transposition_first_key_not_noz(d2) == "m1"
    d3 = _create_full_year_dict(0, {}, total=0)
    assert lod_ymv.d_ymv_transposition_first_key_not_noz(d3) is None
    d4 = _create_full_year_dict(0, {3: 15}, total=15)
    d4["m1"] = None # Explicitly set None
    d4["m2"] = None # Explicitly set None
    assert lod_ymv.d_ymv_transposition_first_key_not_noz(d4) == "m3"
def test_d_ymv_transposition_last_key_not_noz():
    d1 = _create_full_year_dict(0, {2: 10, 3: 20, 6: 30}, total=60)
    assert lod_ymv.d_ymv_transposition_last_key_not_noz(d1) == "m6"
    d2 = _create_full_year_dict(0, {1: 5, 2: 10, 3: 0}, total=15)
    assert lod_ymv.d_ymv_transposition_last_key_not_noz(d2) == "m2"
    d3 = _create_full_year_dict(0, {}, total=0)
    assert lod_ymv.d_ymv_transposition_last_key_not_noz(d3) is None
    d4 = _create_full_year_dict(0, {1: 15}, total=15)
    d4["m2"] = None
    d4["m3"] = None
    assert lod_ymv.d_ymv_transposition_last_key_not_noz(d4) == "m1"
def test_lod_ymv_transposition_with_percentages():
    # Smaller, more controlled dataset for testing percentages
    o = [
        {'year': 2020, 'm1': Decimal('100'), 'm2': Decimal('110'), 'm3': Decimal('100'), 'm4': Decimal('120'), 'm5': Decimal('0'), 'm6': Decimal('0'), 'm7': Decimal('0'), 'm8': Decimal('0'), 'm9': Decimal('0'), 'm10': Decimal('0'), 'm11': Decimal('0'), 'm12': Decimal('130'), 'total': Decimal('460')},
        {'year': 2021, 'm1': Decimal('130'), 'm2': Decimal('140'), 'm3': Decimal('120'), 'm4': Decimal('0'), 'm5': Decimal('0'), 'm6': Decimal('0'), 'm7': Decimal('0'), 'm8': Decimal('0'), 'm9': Decimal('0'), 'm10': Decimal('0'), 'm11': Decimal('0'), 'm12': Decimal('150'), 'total': Decimal('540')},
        {'year': 2022, 'm1': Decimal('0'), 'm2': Decimal('0'), 'm3': Decimal('0'), 'm4': Decimal('0'), 'm5': Decimal('0'), 'm6': Decimal('0'), 'm7': Decimal('0'), 'm8': Decimal('0'), 'm9': Decimal('0'), 'm10': Decimal('0'), 'm11': Decimal('0'), 'm12': Decimal('0'), 'total': Decimal('0')},
        {'year': 2023, 'm1': Decimal('10'), 'm2': Decimal('20'), 'm3': Decimal('30'), 'm4': Decimal('40'), 'm5': Decimal('50'), 'm6': Decimal('60'), 'm7': Decimal('70'), 'm8': Decimal('80'), 'm9': Decimal('90'), 'm10': Decimal('100'), 'm11': Decimal('110'), 'm12': Decimal('120'), 'total': Decimal('780')},
    ]
    r = lod_ymv.lod_ymv_transposition_with_percentages(o)

    assert len(r) == 4

    # Year 2020
    assert r[0]["year"] == 2020
    assert r[0]["m1"] is None # No previous year's m12
    assert r[0]["m2"] == pytest.approx(Decimal('0.1'))
    assert r[0]["m3"] == pytest.approx(Decimal('-0.0909090909090909090909090909')) # (100-110)/110
    assert r[0]["m4"] == pytest.approx(Decimal('0.2'))
    assert r[0]["m5"] is None # 0/120
    assert r[0]["m12"] is None # 130/0
    assert r[0]["total"] == pytest.approx(Decimal('0.3')) # (130-100)/100
    assert r[0]["from_first_quote"] == pytest.approx(Decimal('0.3')) # (130-100)/100

    # Year 2021
    assert r[1]["year"] == 2021
    assert r[1]["m1"] == pytest.approx(Decimal('0.0')) # (130-130)/130
    assert r[1]["m2"] == pytest.approx(Decimal('0.0769230769230769230769230769')) # (140-130)/130
    assert r[1]["m3"] == pytest.approx(Decimal('-0.1428571428571428571428571429')) # (120-140)/140
    assert r[1]["m4"] is None
    assert r[1]["m12"] is None
    assert r[1]["total"] == pytest.approx(Decimal('0.1538461538461538461538461538')) # (150-130)/130
    assert r[1]["from_first_quote"] == pytest.approx(Decimal('0.5')) # (150-100)/100

    # Year 2022 (all zeros)
    assert r[2]["year"] == 2022
    for i in range(1, 13):
        assert r[2][f"m{i}"] is None # All month values are 0, so percentage is None
    assert r[2]["total"] is None
    assert r[2]["from_first_quote"] is None

    # Year 2023
    assert r[3]["year"] == 2023
    assert r[3]["m1"] is None # (10-0)/0
    assert r[3]["m2"] == pytest.approx(Decimal('1.0')) # (20-10)/10
    assert r[3]["m12"] == pytest.approx(Decimal('0.0909090909090909090909090909')) # (120-110)/110
    assert r[3]["total"] is None # (120-0)/0 (total is calculated from first_value_not_noz and last_value_not_noz of the current year, if first is 0, then None)
    assert r[3]["from_first_quote"] == pytest.approx(Decimal('0.2')) # (120-100)/100

    # Test with empty input
    assert lod_ymv.lod_ymv_transposition_with_percentages([]) == []

    # Test with all None/zero values
    o_all_none_zero = [
        {'year': 2020, 'm1': Decimal('0'), 'm2': Decimal('0'), 'm3': Decimal('0'), 'm4': Decimal('0'), 'm5': Decimal('0'), 'm6': Decimal('0'), 'm7': Decimal('0'), 'm8': Decimal('0'), 'm9': Decimal('0'), 'm10': Decimal('0'), 'm11': Decimal('0'), 'm12': Decimal('0'), 'total': Decimal('0')},
        {'year': 2021, 'm1': Decimal('0'), 'm2': Decimal('0'), 'm3': Decimal('0'), 'm4': Decimal('0'), 'm5': Decimal('0'), 'm6': Decimal('0'), 'm7': Decimal('0'), 'm8': Decimal('0'), 'm9': Decimal('0'), 'm10': Decimal('0'), 'm11': Decimal('0'), 'm12': Decimal('0'), 'total': Decimal('0')},
    ]
    r_all_none_zero = lod_ymv.lod_ymv_transposition_with_percentages(o_all_none_zero)
    assert len(r_all_none_zero) == 2
    assert all(v is None for k, v in r_all_none_zero[0].items() if k != 'year')
    assert all(v is None for k, v in r_all_none_zero[1].items() if k != 'year')

def test_lod_ymv_transposition_sum():
    lymv_a = [ # Using helper for consistency
        _create_full_year_dict(2020, {1: 10, 2: 20}, total=30),
        _create_full_year_dict(2021, {1: 100, 2: 200}, total=300),
    ]
    lymv_b = [ # Using helper for consistency
        _create_full_year_dict(2020, {1: 1, 2: 2}, total=3),
        _create_full_year_dict(2022, {1: 1000, 2: 2000}, total=3000),
    ]

    result = lod_ymv.lod_ymv_transposition_sum(lymv_a, lymv_b)

    # Expected:
    # 2020: m1=10+1=11, m2=20+2=22, total=30+3=33
    # 2021: m1=100, m2=200, total=300 (from lymv_a only)
    # 2022: m1=1000, m2=2000, total=3000 (from lymv_b only)

    assert len(result) == 3
    assert result[0]["year"] == 2020
    assert result[0]["m1"] == 11
    assert result[0]["m2"] == 22
    assert result[0]["total"] == 33

    assert result[1]["year"] == 2021
    assert result[1]["m1"] == 100
    assert result[1]["m2"] == 200
    assert result[1]["total"] == 300

    assert result[2]["year"] == 2022
    assert result[2]["m1"] == 1000
    assert result[2]["m2"] == 2000
    assert result[2]["total"] == 3000

    # Test with empty lists
    assert lod_ymv.lod_ymv_transposition_sum([], lymv_b) == lymv_b
    assert lod_ymv.lod_ymv_transposition_sum(lymv_a, []) == lymv_a

    # Test with overlapping years but one list has more years
    lymv_c = [ # Using helper for consistency
        _create_full_year_dict(2019, {1: 5, 2: 5}, total=10),
        _create_full_year_dict(2020, {1: 10, 2: 20}, total=30),
    ]
    lymv_d = [ # Using helper for consistency
        _create_full_year_dict(2020, {1: 1, 2: 2}, total=3),
        _create_full_year_dict(2021, {1: 3, 2: 4}, total=7),
    ]
    result_overlap = lod_ymv.lod_ymv_transposition_sum(lymv_c, lymv_d)
    assert len(result_overlap) == 3
    assert result_overlap[0]["year"] == 2019
    assert result_overlap[0]["m1"] == 5
    assert result_overlap[1]["year"] == 2020
    assert result_overlap[1]["m1"] == 11
    assert result_overlap[2]["year"] == 2021
    assert result_overlap[2]["m1"] == 3

def test_lod_ymv_filling():
    initial_lod = [
        {"year": 2020, "month": 1, "value": 10, "other_data": "A"},
        {"year": 2020, "month": 3, "value": 30, "other_data": "C"},
        {"year": 2021, "month": 2, "value": 20, "other_data": "B"},
    ]

    # Fill from 2020 to 2021
    filled_lod = lod_ymv.lod_ymv_filling(initial_lod, 2020, 2021, fill_value=0, key_value="value")

    # Expected: 2 years * 12 months = 24 entries
    assert len(filled_lod) == 24

    # Check specific filled values and order
    # The filled_lod should be sorted by year, then month
    assert filled_lod[0] == {"year": 2020, "month": 1, "value": 10, "other_data": "A"}
    assert filled_lod[1] == {"year": 2020, "month": 2, "value": 0} # New entry, only specified keys
    assert filled_lod[2] == {"year": 2020, "month": 3, "value": 30, "other_data": "C"}
    assert filled_lod[11] == {"year": 2020, "month": 12, "value": 0}
    assert filled_lod[12] == {"year": 2021, "month": 1, "value": 0}
    assert filled_lod[13] == {"year": 2021, "month": 2, "value": 20, "other_data": "B"}
    assert filled_lod[23] == {"year": 2021, "month": 12, "value": 0}

    # Test with an empty initial lod
    filled_empty_lod = lod_ymv.lod_ymv_filling([], 2022, 2022, fill_value=-1, key_value="value")
    assert len(filled_empty_lod) == 12
    for d in filled_empty_lod:
        assert d["year"] == 2022
        assert d["value"] == -1
        assert "month" in d # Ensure month key is present

    # Test with already full lod (should not change values)
    full_lod = []
    for m in range(1, 13):
        full_lod.append({"year": 2023, "month": m, "value": m * 10, "extra": "X"})
    filled_full_lod = lod_ymv.lod_ymv_filling(full_lod, 2023, 2023, fill_value=0, key_value="value")
    assert len(filled_full_lod) == 12
    for m in range(1, 13):
        # Original dictionaries should be preserved
        assert filled_full_lod[m-1]["year"] == 2023
        assert filled_full_lod[m-1]["month"] == m
        assert filled_full_lod[m-1]["value"] == m * 10
        assert filled_full_lod[m-1]["extra"] == "X"

    # Test with different key names
    initial_lod_custom_keys = [
        {"y": 2020, "m": 1, "val": 10, "other": "data"},
    ]
    filled_custom_keys = lod_ymv.lod_ymv_filling(initial_lod_custom_keys, 2020, 2020, fill_value=0, key_year="y", key_month="m", key_value="val")
    assert len(filled_custom_keys) == 12
    # Check first existing entry
    assert filled_custom_keys[0] == {"y": 2020, "m": 1, "val": 10, "other": "data"}
    assert filled_custom_keys[1] == {"y": 2020, "m": 2, "val": 0}
    assert filled_custom_keys[11] == {"y": 2020, "m": 12, "val": 0}
