from datetime import date
from pydicts import lod
"""
    lod_ymv example:
    +------------------+-------------------+---------+
|   datetime__year |   datetime__month |   quote |
|------------------+-------------------+---------|
|             2020 |                 1 |   82.92 |
|             2020 |                 2 |   67.41 |
|             2020 |                 3 |   51.24 |
|             2020 |                 4 |   61.98 |
|             2020 |                 5 |   65.21 |
|             2020 |                 6 |   66.69 |
|             2020 |                 7 |   70.55 |
|             2020 |                 8 |   81.31 |
|             2020 |                 9 |   76.6  |
|             2020 |                10 |   74.33 |
|             2020 |                11 |   85.59 |
|             2020 |                12 |   89.84 |
|             2021 |                 1 |   90.52 |
|             2021 |                 2 |   96.19 |
|             2021 |                 3 |  106.42 |
|             2021 |                 4 |  114.54 |
|             2021 |                 5 |  113.42 |
|             2021 |                 6 |  122.66 |
|             2021 |                 7 |  128.38 |
|             2021 |                 8 |  137.18 |
|             2021 |                 9 |  128.82 |
|             2021 |                10 |  143.94 |
|             2021 |                11 |  147.06 |
|             2021 |                12 |  159.98 |
|             2022 |                 1 |  139.62 |
|             2022 |                 2 |  134    |
|             2022 |                 3 |  148.32 |
|             2022 |                 4 |  131.9  |
|             2022 |                 5 |  122.38 |
|             2022 |                 6 |  104.96 |
|             2022 |                 7 |  125.88 |
|             2022 |                 8 |  120.36 |
|             2022 |                 9 |  103.98 |
|             2022 |                10 |  114.4  |
|             2022 |                11 |  113.64 |
|             2022 |                12 |  102.12 |
|             2023 |                 1 |  111.62 |
|             2023 |                 2 |  110.42 |
|             2023 |                 3 |  112.76 |
|             2023 |                 4 |  113.96 |
+------------------+-------------------+---------+

"""


## Converts a tipical groyp by lor with year, month, value into an other lor with year, 1, 2, 3 .... 12, total 
def lod_ymv_transposition(ld, key_year="year", key_month="month", key_value="value"):
    """
        Covert lod_ymv into a trasposition form 
        +--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+---------+
        |   year |     m1 |     m2 |     m3 |     m4 |     m5 |     m6 |     m7 |     m8 |     m9 |    m10 |    m11 |    m12 |   total |
        |--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+---------|
        |   2020 |  82.92 |  67.41 |  51.24 |  61.98 |  65.21 |  66.69 |  70.55 |  81.31 |  76.6  |  74.33 |  85.59 |  89.84 |  873.67 |
        |   2021 |  90.52 |  96.19 | 106.42 | 114.54 | 113.42 | 122.66 | 128.38 | 137.18 | 128.82 | 143.94 | 147.06 | 159.98 | 1489.11 |
        |   2022 | 139.62 | 134    | 148.32 | 131.9  | 122.38 | 104.96 | 125.88 | 120.36 | 103.98 | 114.4  | 113.64 | 102.12 | 1461.56 |
        |   2023 | 111.62 | 110.42 | 112.76 | 113.96 |   0    |   0    |   0    |   0    |   0    |   0    |   0    |   0    |  448.76 |
        +--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+---------+
    """
    if len(ld)==0:
       return []

    if not key_year in ld[0] or not key_month in ld[0] or not key_value in ld[0]:
        print("Keys names are not correct in dictionary in lod_ymv_transposition function")
        return None

    min_year=lod.lod_min_value(ld, key_year)
    max_year=lod.lod_max_value(ld, key_year)
    #Initialize result
    r=[]
    for year in range(min_year,max_year+1):
        r.append({"year": year, "m1":0, "m2":0,  "m3":0, "m4":0, "m5":0, "m6":0, "m7":0, "m8":0, "m9":0, "m10":0, "m11":0, "m12":0, "total":0})

    #Assign values
    for d in ld:
        r[d[key_year]-min_year]["m"+str(d[key_month])]=r[d[key_year]-min_year]["m"+str(d[key_month])]+d[key_value]

    #Calculate totals
    for year in range(min_year,max_year+1):
        d=r[year-min_year]
        d["total"]=d["m1"]+d["m2"]+d["m3"]+d["m4"]+d["m5"]+d["m6"]+d["m7"]+d["m8"]+d["m9"]+d["m10"]+d["m11"]+d["m12"]

    return r
    
def d_ymv_transposition_first_value(d):
    """
        REturns the first key mX not null in dictionary
    """
    r=None
    for i in range(1, 13):
        if d[f"m{i}"]!=0:
            r= f"m{i}"
            break
    return r

def d_ymv_transposition_last_value(d):
    """
        REturns the last key mX not null in dictionary
    """
    r=None
    for i in reversed(range(1, 13)):
        if d[f"m{i}"]!=0:
            r= f"m{i}"
            break
    return r

    
def lod_ymv_transposition_with_percentages(lod_ymv_transposition):
    """
        Replace a lod_ymv_transposition values to Percentages
    """
    def percentage(from_,  to_):
        if from_ is None or from_==0:
            return None
        if to_ is None or to_==0:
            return None
        return (to_-from_)/from_
    ###########################
    r=[]
    if len(lod_ymv_transposition)==0:
        return r
    for i, d in enumerate(lod_ymv_transposition):
        new_d={"year":d["year"]}
        new_d["m1"]=None if i==0 else percentage(lod_ymv_transposition[i-1]["m12"], d["m1"])
        new_d["m2"]=percentage(d["m1"], d["m2"])
        new_d["m3"]=percentage(d["m2"], d["m3"])
        new_d["m4"]=percentage(d["m3"], d["m4"])
        new_d["m5"]=percentage(d["m4"], d["m5"])
        new_d["m6"]=percentage(d["m5"], d["m6"])
        new_d["m7"]=percentage(d["m6"], d["m7"])
        new_d["m8"]=percentage(d["m7"], d["m8"])
        new_d["m9"]=percentage(d["m8"], d["m9"])
        new_d["m10"]=percentage(d["m9"], d["m10"])
        new_d["m11"]=percentage(d["m10"], d["m11"])
        new_d["m12"]=percentage(d["m11"], d["m12"])
        if i==0:
            new_d["total"]=percentage(d[d_ymv_transposition_first_value(d)], d[d_ymv_transposition_last_value(d)])
            new_d["from_first_quote"]=percentage
        else:
            new_d["total"]=percentage(lod_ymv_transposition[i-1]["m12"], d[d_ymv_transposition_last_value(d)])
        new_d["from_first_quote"]=percentage(lod_ymv_transposition[0][d_ymv_transposition_first_value(lod_ymv_transposition[0])], d[d_ymv_transposition_last_value(d)])
            
        r.append(new_d)
    return r

def lod_ymv_transposition_sum(lymv_a, lymv_b):
    """
        Sums to lod_ymv_transpositions
    """
    def get_younger(year, field):
        if year in d_younger:
            return d_younger[year][field]
        else:
            return 0
    
    if len(lymv_a)==0:
        return lymv_b
    if len(lymv_b)==0:
        return lymv_a
    year_lymv_a=lymv_a[0]["year"]
    year_lymv_b=lymv_b[0]["year"]
    print(year_lymv_a, year_lymv_b)
    older=lymv_a if year_lymv_a<year_lymv_b else lymv_b
    younger=lymv_a if year_lymv_a>year_lymv_b else lymv_b
    d_younger=lod.lod2dod(younger, "year")
    r=[]
    for d in older:
        new={}
        new["year"]=d["year"]
        new["m1"]=d["m1"]+get_younger(d["year"],"m1")
        new["m2"]=d["m2"]+get_younger(d["year"],"m2")
        new["m3"]=d["m3"]+get_younger(d["year"],"m3")
        new["m4"]=d["m4"]+get_younger(d["year"],"m4")
        new["m5"]=d["m5"]+get_younger(d["year"],"m5")
        new["m6"]=d["m6"]+get_younger(d["year"],"m6")
        new["m7"]=d["m7"]+get_younger(d["year"],"m7")
        new["m8"]=d["m8"]+get_younger(d["year"],"m8")
        new["m9"]=d["m9"]+get_younger(d["year"],"m9")
        new["m10"]=d["m10"]+get_younger(d["year"],"m10")
        new["m11"]=d["m11"]+get_younger(d["year"],"m11")
        new["m12"]=d["m12"]+get_younger(d["year"],"m12")
        new["total"]=d["total"]+get_younger(d["year"],"total")
        r.append(new)
    return r

## Converts a tipical groyp by lor with year, month (normaly extracted from db to fill empty values)
def lod_ymv_filling(lod, year_from, year_to=date.today().year, fill_value=0, key_year="year", key_month="month", key_value="value"):
    ld_tuple=lod.lod2dod_tuple(lod, key_year, key_month)
    for year in range(year_from,year_to+1):
        for month in range (1,13):
            if not (key_year,key_month) in ld_tuple:
                ld_tuple[(key_year,key_month)]={key_year: year, key_month: month, key_value:fill_value}
    r=[]
    for d in ld_tuple.values:
        r.append(d)
    return r
