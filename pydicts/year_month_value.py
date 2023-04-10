

from datetime import date
from pydicts.lod import lod2dict, lod_min_value, lod_max_value, lod2dict_tuple


## Converts a tipical groyp by lor with year, month, value into an other lor with year, 1, 2, 3 .... 12, total 
def lod_year_month_value_transposition(ld, key_year="year", key_month="month", key_value="value"):
    if len(ld)==0:
       return []

    if not key_year in ld[0] or not key_month in ld[0] or not key_value in ld[0]:
        print("Keys names are not correct in dictionary in lod_year_month_value_transposition function")
        return None

    min_year=lod_min_value(ld, key_year)
    max_year=lod_max_value(ld, key_year)
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

def lod_year_month_value_transposition_sum(lymv_a, lymv_b):
    """
        Sums to lod_year_month_value_transpositions
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
    d_younger=lod2dict(younger, "year")
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
def lod_year_month_value_filling(lod, year_from, year_to=date.today().year, fill_value=0, key_year="year", key_month="month", key_value="value"):
    ld_tuple=lod2dict_tuple(lod, key_year, key_month)
    for year in range(year_from,year_to+1):
        for month in range (1,13):
            if not (key_year,key_month) in ld_tuple:
                ld_tuple[(key_year,key_month)]={key_year: year, key_month: month, key_value:fill_value}
    r=[]
    for d in ld_tuple.values:
        r.append(d)
    return r
