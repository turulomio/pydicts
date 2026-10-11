from pydicts.lod_xyv import lod_xyv_transformation


def test_lod_xyv_transformation():
    """
    Tests lod_xyv_transformation for pivoting 2D sparse/coordinate records (X, Y, Value)
    into structured tabular rows with column headers, handling empty lists and invalid keys.
    """
    raw_data = [
        {"x": "Row1", "y": "ColA", "val": 10},
        {"x": "Row1", "y": "ColB", "val": 20},
        {"x": "Row2", "y": "ColA", "val": 30},
        {"x": "Row2", "y": "ColB", "val": 40},
    ]

    # Valid transformation
    res = lod_xyv_transformation(raw_data, "x", "y", "val")
    assert isinstance(res, list)
    assert len(res) == 2
    row1 = next(r for r in res if r["title"] == "Row1")
    assert row1["ColA"] == 10
    assert row1["ColB"] == 20

    # Empty list
    assert lod_xyv_transformation([], "x", "y", "val") == []

    # Invalid keys
    assert lod_xyv_transformation(raw_data, "wrong_x", "y", "val") is None
