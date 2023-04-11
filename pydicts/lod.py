from collections import OrderedDict

def lod_has_key(lod, key):
    if len(lod)==0:
        return False
    return key in lod[0]


## Order data columns. None values are set at the beginning
def lod_order_by(ld, key, reverse=False, none_at_top=True):
    nonull=[]
    null=[]
    for o in ld:
        com=o[key]
        if com is None:
            null.append(o)
        else:
            nonull.append(o)
    nonull=sorted(nonull, key=lambda item: item[key], reverse=reverse)
    if none_at_top==True:#Set None at top of the list
        return null+nonull
    else:
        return nonull+null



def lod_print(lod):
    for row in lod:
        print(row)

def lod_print_first(lod):
    if len(lod)==0:
        print("No rows in lod")
        return
    print("Printing first dict in a lod")
    keys=list(lod[0].keys())
    keys.sort()
    for key in keys:
        print(f"    - {key}: {lod[0][key]}")

def lod_sum(lod, key, ignore_nones=True):
    r=0
    for d in lod:
        if ignore_nones is True and d[key] is None:
            continue
        r=r+d[key]
    return r

def lod_sum_negatives(lod, key):
    r=0
    for d in lod:
        if d[key] is None or d[key]>0:
            continue
        r=r+d[key]
    return r

def lod_sum_positives(lod, key):
    r=0
    for d in lod:
        if d[key] is None or d[key]<0:
            continue
        r=r+d[key]
    return r


def lod_average(lod, key):
    return lod_sum(lod,key)/len(lod)

def lod_average_ponderated(lod, key_numbers, key_values):
    prods=0
    for d in lod:
        prods=prods+d[key_numbers]*d[key_values]
    return prods/lod_sum(lod, key_numbers)


def lod_median(lod, key):
    from statistics import median
    return median(lod2list(lod, key, sorted=True))


## Converts a lod to a dict using key as new dict key, and value as the key of the value field
def lod2dictkv(lod, key, value):
    d={}
    for ld in lod:
        d[ld[key]]=ld[value]
    return d

## Converts a lod to a dict using key as new dict key, and the dict as a value
def lod2dict(lod, key):
    d={}
    for ld in lod:
        d[ld[key]]=ld
    return d
    
## Converts a lod to a dict using (key1,key2) tuple  as new dict key, and the dict as a value
def lod2dict_tuple(lod, key1, key2):
    d={}
    for ld in lod:
        d[(ld[key1],ld[key2])]=ld
    return d

## Converts a dict of dictionaries (prefered orderdict) to a list of dictionaries
def dict2lod(d):
    r=[]
    for k,v in d.items():
        r.append(v)
    return r

## Returns a list from a lod key
## @param lod
## @param key String with the key to extract
## @param sorted Boolean. If true sorts final result
## @param cast String. "str", "float", casts the content of the key
def lod2list(lod, key, sorted=False, cast=None):
    r=[]
    for ld in lod:
        if cast is None:
            r.append(ld[key])
        elif cast == "str":
            r.append(str(ld[key]))
        elif cast == "float":
            r.append(float(ld[key]))
    if sorted is True:
        r.sort()
    return r


## Returns a list from a lod key, with distinct values, not all values
## @param lod
## @param key String with the key to extract
## @param sorted Boolean. If true sorts final result
## @param cast String. "str", "float", casts the content of the key
def lod2list_distinct(lod, key, sorted=False, cast=None):
    set_=set()
    for ld in lod:
        if cast is None:
            set_.add(ld[key])
        elif cast == "str":
            set_.add(str(ld[key]))
        elif cast == "float":
            set_.add(float(ld[key]))
    r=list(set_)
    if sorted is True:
        r.sort()
    return r

## Returns the max of a key in lod
def lod_max(lod, key):
    return max(lod2list(lod,key))

## Returns the min of a key in lod
def lod_min(lod, key):
    return min(lod2list(lod,key))

## Converts a list of ordereddict to a list of rows. ONLY DATA
## @params keys If None we must suppose is an ordered dict or keys will be randomized
def lod2lol(lod,  keys=None):
    if len(lod)==0:
        return []
        
    if keys is None:
        keys=lod[0].keys()
        
    r=[]  
    for od in lod:
        row_r=[]
        for key in keys:
            row_r.append(od[key])
        r.append(row_r)
    return r

def lod2lood(ld, keys):
    if len(ld)==0:
        return []
                
    r=[]  
    for d in ld:
        r_d=OrderedDict()
        for key in keys:
            r_d[key]=d[key]
        r.append(r_d)
    return r


## Returns maximum value of a given key. Is unique. REturns NOne if lod is empty
def lod_max_value(ld, key):
     if len(ld)>0:
          r=ld[0][key]
     else:
         return None
     for d in ld:
         if  d[key]>r:
             r=d[key]
     return r

## Returns minimum value of a given key. Is unique. REturns NOne if lod is empty
def lod_min_value(ld, key):
     if len(ld)>0:
          r=ld[0][key]
     else:
         return None
     for d in ld:
         if  d[key]<r:
             r=d[key]
     return r

def lod_rename_key(ld, from_, to_):
    """
        Renames a key(from_) to another key(to_) in each dictionary in ld
    """
    for d in ld:
        d[to_]=d.pop(from_)
    return ld

