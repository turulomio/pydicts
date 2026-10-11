from datetime import datetime, date
from decimal import Decimal
from pydicts import dod
from pytest import fixture

empty_lod = []

@fixture(autouse=True)
def reload_lod_():
    d = {
        "a": datetime.now(),
        "b": date.today(),
        "c": Decimal("12.32"),
        "d": None,
        "e": int(12),
        "f": None,
        "g": True,
        "h": False,
        "nested": {"x": 1, "y": 2, "z": {"n": 4, "m": 5, "o": 6}},
    }
    global dod_
    dod_ = {}
    dod_["first"] = d
    dod_["second"] = d


def test_dod_string():
    """
    Tests the dod_string function to verify formatted output and parameter handling.
    """
    s = dod.dod_string(dod_, indent=2)
    assert isinstance(s, str)
    assert "first" in s
    assert "second" in s


def test_dod_print(capsys):
    """
    Tests the dod_print function to ensure it outputs to stdout properly.
    """
    dod.dod_print(dod_, indent=4)
    captured = capsys.readouterr()
    assert "first" in captured.out
    assert "second" in captured.out


def test_dod_tables(capsys):
    """
    Tests dod_string_tables and dod_print_tables.
    """
    tbl = dod.dod_string_tables(dod_, key_name="ID")
    assert "ID" in tbl
    assert "first" in tbl
    assert "second" in tbl

    dod.dod_print_tables(dod_, key_name="ID")
    captured = capsys.readouterr()
    assert "ID" in captured.out
    assert "first" in captured.out


