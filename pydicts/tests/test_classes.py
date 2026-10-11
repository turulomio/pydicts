from decimal import Decimal
import pytest
from pydicts.classes import DOD, LOD, LOL


@pytest.fixture
def sample_data():
    return [
        {"id": 1, "name": "Alice", "age": 30, "salary": Decimal("1000.50")},
        {"id": 2, "name": "Bob", "age": 25, "salary": Decimal("1500.00")},
        {"id": 3, "name": "Charlie", "age": 35, "salary": Decimal("2000.00")},
        {"id": 4, "name": "David", "age": None, "salary": Decimal("500.00")},
        {"id": 5, "name": "Alice", "age": 30, "salary": Decimal("1000.50")},  # duplicate with id 1? different id, same other fields
    ]


def test_init_and_container_protocols(sample_data):
    # Empty init
    lod_empty = LOD()
    assert len(lod_empty) == 0
    assert not bool(lod_empty)
    assert repr(lod_empty) == "LOD(name='LOD', length=0)"

    # Init with data and name
    lod = LOD(sample_data, name="Employees")
    assert len(lod) == 5
    assert lod.length() == 5
    assert bool(lod) is True
    assert repr(lod) == "LOD(name='Employees', length=5)"

    # __iter__
    names = [row["name"] for row in lod]
    assert names == ["Alice", "Bob", "Charlie", "David", "Alice"]

    # __getitem__ index
    assert lod[0]["name"] == "Alice"
    assert lod[-1]["name"] == "Alice"

    # __getitem__ slice
    subset = lod[1:3]
    assert isinstance(subset, LOD)
    assert len(subset) == 2
    assert subset.name == "Employees"
    assert subset[0]["name"] == "Bob"

    # __contains__
    assert sample_data[0] in lod

    # __eq__
    assert lod == sample_data
    assert lod == LOD(sample_data)


def test_first_and_keys(sample_data):
    lod = LOD(sample_data)
    assert lod.first() == sample_data[0]
    assert "name" in lod.first_keys()
    assert set(lod.keys()) == {"id", "name", "age", "salary"}

    empty = LOD()
    assert empty.first() is None
    assert empty.first_keys() == []
    assert empty.keys() is None


def test_set_append_extend(sample_data):
    lod = LOD()
    lod.set(sample_data[:2])
    assert len(lod) == 2
    assert lod.is_set() is True

    lod.append({"id": 6, "name": "Frank", "age": 40, "salary": Decimal("3000")})
    assert len(lod) == 3
    assert lod[-1]["name"] == "Frank"

    lod.extend([{"id": 7, "name": "Grace", "age": 22, "salary": Decimal("1200")}])
    assert len(lod) == 4
    assert lod[-1]["name"] == "Grace"


def test_aggregations(sample_data):
    lod = LOD(sample_data)

    assert lod.sum("salary") == Decimal("6001.00")
    # lod_average calculates lod_sum(key) / len(lod) -> 120 / 5 = 24.0
    assert lod.average("age") == 24.0
    # median on non-None values: sorted salaries [500.00, 1000.50, 1000.50, 1500.00, 2000.00] -> 1000.50
    assert lod.median("salary") == Decimal("1000.50")
    assert lod.min_value("salary") == Decimal("500.00")
    assert lod.max_value("salary") == Decimal("2000.00")

    # count
    assert lod.count(lambda r: r["name"] == "Alice") == 2

    # list and list_distinct
    assert len(lod.list("name", sorted=False)) == 5
    distinct_names = lod.list_distinct("name", sorted=True)
    assert distinct_names == ["Alice", "Bob", "Charlie", "David"]


def test_transformations(sample_data):
    lod = LOD(sample_data)

    # order_by
    lod.order_by("age", none_at_top=True)
    assert lod[0]["name"] == "David"

    # filter
    older = lod.filter(lambda r: r["age"] is not None and r["age"] >= 30)
    assert isinstance(older, LOD)
    assert len(older) == 3

    # filter_keys
    projected = lod.filter_keys(["id", "name"])
    assert isinstance(projected, LOD)
    assert list(projected[0].keys()) == ["id", "name"]

    # calculate
    lod.calculate("double_id", lambda r: r["id"] * 2)
    assert lod[0]["double_id"] == lod[0]["id"] * 2

    # rename_key
    lod.rename_key("double_id", "id_x2")
    assert "id_x2" in lod[0]
    assert "double_id" not in lod[0]

    # remove_key
    lod.remove_key("id_x2")
    assert "id_x2" not in lod[0]

    # clone
    cloned = lod.clone()
    assert cloned == lod
    cloned.append({"id": 99})
    assert len(cloned) == len(lod) + 1


def test_string_and_print(sample_data, capsys):
    lod = LOD(sample_data)
    table_str = str(lod)
    assert "Alice" in table_str
    assert "Bob" in table_str

    lod.print()
    captured = capsys.readouterr()
    assert "Alice" in captured.out


def test_conversions(sample_data):
    lod = LOD(sample_data)

    # to_dod
    dod_obj = lod.to_dod("id")
    assert isinstance(dod_obj, DOD)
    assert len(dod_obj) == 5
    assert dod_obj[1]["name"] == "Alice"

    # to_lod from dod
    roundtrip_lod = dod_obj.to_lod()
    assert isinstance(roundtrip_lod, LOD)
    assert len(roundtrip_lod) == 5

    # to_lol
    lol_obj = lod.to_lol(keys=["id", "name"])
    assert isinstance(lol_obj, LOL)
    assert len(lol_obj) == 5
    assert lol_obj[0] == [1, "Alice"]

    # to_dictkv
    kv = lod.to_dictkv("id", "name")
    assert kv[1] == "Alice"


def test_lol_class():
    data = [
        [1, "Alice", 100],
        [2, "Bob", 200],
        [3, "Charlie", 300],
    ]
    lol_obj = LOL(data, name="Table")
    assert len(lol_obj) == 3
    assert bool(lol_obj) is True
    assert lol_obj[0] == [1, "Alice", 100]
    assert lol_obj[-1][1] == "Charlie"

    # slice
    sub = lol_obj[:2]
    assert isinstance(sub, LOL)
    assert len(sub) == 2

    # row & column access
    assert lol_obj.get_row(1) == [2, "Bob", 200]
    assert lol_obj.get_column(1) == ["Alice", "Bob", "Charlie"]

    # sums
    assert lol_obj.sum_row(0, from_index=2) == 100
    assert lol_obj.sum_column(2) == 600

    # add row & column
    lol_obj.add_row(1, [99, "Temp", 0])
    assert lol_obj.get_row(1) == [99, "Temp", 0]
    assert len(lol_obj) == 4

    lol_obj.remove_rows([1])
    assert len(lol_obj) == 3

    # transposed
    trans = lol_obj.transposed()
    assert isinstance(trans, LOL)
    assert len(trans) == 3
    assert trans[0] == [1, 2, 3]

    # order_by
    lol_obj.order_by(2, reverse=True)
    assert lol_obj[0][1] == "Charlie"

    # string & print
    assert "Alice" in str(lol_obj)


def test_dod_class(capsys):
    data = {
        "user1": {"name": "Alice", "role": "admin"},
        "user2": {"name": "Bob", "role": "user"},
    }
    dod_obj = DOD(data, name="Users")
    assert len(dod_obj) == 2
    assert bool(dod_obj) is True
    assert dod_obj["user1"]["name"] == "Alice"
    assert "user2" in dod_obj
    assert list(dod_obj.keys()) == ["user1", "user2"]

    # mutation
    dod_obj["user3"] = {"name": "Charlie", "role": "editor"}
    assert len(dod_obj) == 3
    assert dod_obj.get("user3")["name"] == "Charlie"
    del dod_obj["user3"]
    assert len(dod_obj) == 2

    # to_lod
    lod_obj = dod_obj.to_lod()
    assert isinstance(lod_obj, LOD)
    assert len(lod_obj) == 2

    # print
    dod_obj.print()
    captured = capsys.readouterr()
    assert "Alice" in captured.out

    # string, string_tables, print_tables
    s = dod_obj.string(indent=2)
    assert "Alice" in s
    tbl = dod_obj.string_tables(key_name="UserID")
    assert "UserID" in tbl
    assert "user1" in tbl
    dod_obj.print_tables(key_name="UserID")
    captured = capsys.readouterr()
    assert "UserID" in captured.out

    # values, items, set, init empty, init DOD, __eq__
    assert len(list(dod_obj.values())) == 2
    assert len(list(dod_obj.items())) == 2
    empty_dod = DOD()
    assert len(empty_dod) == 0
    assert not bool(empty_dod)
    cloned_dod = DOD(dod_obj)
    assert cloned_dod == dod_obj
    assert cloned_dod == dod_obj.dod
    assert dod_obj != [1, 2, 3]

    dod_obj.set({"k1": {"a": 10}})
    assert len(dod_obj) == 1


def test_classes_extended_coverage(sample_data, capsys):
    # LOD conversions and aggregations
    lod = LOD(sample_data, name="Team")
    assert lod.sum_positives("salary") == Decimal("6001.00")
    assert lod.sum_negatives("salary") == 0
    assert lod.has_key("salary") is True
    assert lod.has_key("nonexistent") is False

    # LOD print_first
    lod.print_first()
    captured = capsys.readouterr()
    assert "Alice" in captured.out

    # LOD aggregations / join / reorder
    reordered = lod.clone().reorder_keys(["name", "id", "age", "salary"])
    assert list(reordered[0].keys())[:2] == ["name", "id"]

    # remove_duplicates
    lod_dup = LOD([{"id": 1, "val": 10}, {"id": 1, "val": 10}, {"id": 2, "val": 20}])
    lod_dup.remove_duplicates()
    assert len(lod_dup) == 2

    # aggregate_sum
    lod_agg = LOD([{"grp": "A", "val": 10}, {"grp": "A", "val": 20}, {"grp": "B", "val": 5}])
    aggregated = lod_agg.aggregate_sum("val")
    assert len(aggregated) == 2

    # join
    l1 = LOD([{"id": 1, "score": 10}, {"id": 2, "score": 20}])
    l2 = LOD([{"id": 1, "score": 5}, {"id": 2, "score": 15}])
    joined = l1.join(l2, calc_key="score", operation="+")
    assert joined[0]["score"] == 15

    # to_odod, to_dod_tuple, to_lood
    odod = lod.to_odod("id")
    assert isinstance(odod, DOD)
    dod_tup = lod.to_dod_tuple("id", "name")
    assert isinstance(dod_tup, DOD)
    lood = lod.to_lood(["id", "name"])
    assert isinstance(lood, list)
    assert len(lood) == len(lod)

    # is_set check
    lod_empty = LOD()
    assert lod_empty.is_set() is True
    del lod_empty.ld
    assert lod_empty.is_set() is False

    # Init from iterable / another LOD
    lod_copy = LOD(lod)
    assert lod_copy == lod
    lod_from_iter = LOD((d for d in sample_data[:2]))
    assert len(lod_from_iter) == 2
    assert lod != "not_a_lod"

    # LOL extended methods
    lol = LOL([[1, 2], [3, 4]], name="Matrix")
    assert 1 not in lol
    assert [1, 2] in lol
    assert lol == [[1, 2], [3, 4]]
    assert lol == LOL([[1, 2], [3, 4]])
    assert lol != "invalid"

    lol.set([[10, 20], [30, 40]])
    assert lol[0][0] == 10
    lol.append([50, 60])
    lol.extend(LOL([[70, 80]]))
    lol.extend([[90, 100]])
    assert len(lol) == 5

    # add_column / remove_columns
    lol.add_column(1, [1, 2, 3, 4, 5])
    assert lol.get_column(1) == [1, 2, 3, 4, 5]
    lol.remove_columns([1])
    assert len(lol[0]) == 2

    # lol print
    lol.print()
    captured = capsys.readouterr()
    assert "10" in captured.out

    # lol __iter__ and repr
    rows = [r for r in lol]
    assert len(rows) == 5
    assert "rows=5" in repr(lol)

    # LOD extend with another LOD
    lod1 = LOD([{"a": 1}])
    lod2 = LOD([{"b": 2}])
    lod1.extend(lod2)
    assert len(lod1) == 2

    # LOD average_ponderated
    weights_data = LOD([{"weight": 2, "grade": 10}, {"weight": 3, "grade": 15}])
    # (2*10 + 3*15) / (2+3) = (20 + 45) / 5 = 13.0
    assert weights_data.average_ponderated("weight", "grade") == 13.0

    # DOD __iter__, __repr__, __str__
    d_obj = DOD({"x": {"n": 1}}, name="Single")
    keys_iter = [k for k in d_obj]
    assert keys_iter == ["x"]
    assert "entries=1" in repr(d_obj)
    assert "Single" in repr(d_obj)
    assert "x" in str(d_obj)


