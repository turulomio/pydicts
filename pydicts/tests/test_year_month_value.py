from pydicts.year_month_value import lod_year_month_value_transposition

def tests_dictkv():
  
    
    print ("-- List dict transposition")
    o=[
        {"year": 2022, "month": 1, "my_sum": 12},
        {"year": 2021, "month": 2, "my_sum": 123},
        {"year": 2019, "month": 5, "my_sum": 1},
        {"year": 2022, "month": 12, "my_sum": 12},
    ]
    print(lod_year_month_value_transposition(o,key_value="my_sum"))
