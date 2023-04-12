


## Converts a tipical groyp by lor with A, B, value, value into an other lod with A as rows, B as columns and value as AxB list of dic
## columns order can be defined in order
def lod_xyv_transformation(ld, key_x, key_y, key_value, order=None):
    if len(ld)==0:
       return []

    if not key_x in ld[0] or not key_y in ld[0] or not key_value in ld[0]:
        print("Keys names are not correct in dictionary in lod_year_month_value_transposition function")
        return None

    #Searches for all diferent keys
    columns=set()
    rows=set()
    for d in ld:
        columns.add(d[key_y])
        rows.add(d[key_x])
    columns=list(columns)
    rows=list(rows)
    
    #Initialize result with a dictionary of dictionary
    dd={}
    for row in rows:
        d={"title": row}
        for column in columns:
            d[column]=0
        dd[row]=d

    #Assign values
    for d in ld:
        dd[d[key_x]][d[key_y]]=d[key_value]
    
    ## Converts dd to a ld
    r=[]
    for k, v in dd.items():
        r.append(v)
    
    return r
