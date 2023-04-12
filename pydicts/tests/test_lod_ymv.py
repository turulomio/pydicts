from pydicts import lod_ymv

def tests_lod_year_month_value_transposition():
    o=[
        {"year": 2022, "month": 1, "my_sum": 12},
        {"year": 2021, "month": 2, "my_sum": 123},
        {"year": 2019, "month": 5, "my_sum": 1},
        {"year": 2022, "month": 12, "my_sum": 12},
    ]
    t=lod_ymv.lod_ymv_transposition(o,key_value="my_sum")
    assert t[0]["year"]==2019
    assert t[3]["total"]==24
