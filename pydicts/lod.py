from collections import OrderedDict
from tabulate import tabulate
from gettext import translation
from importlib.resources import files
        
try:
    t=translation('pydicts', files("pydicts") / 'locale')
    _=t.gettext
except:
    _=str

def lod_has_key(lod_, key):
    if len(lod_)==0:
        return False
    return key in lod_[0]

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

def lod_print(lod_, number=None, align=None):
    """
    Prints a list of dictionaries with tabulate module.

        - lod_: List of dictionaries
        - number: Number of dictionaries in the list to print. If None prints all lod_. (defaults to None)
        - align: Cells alignment with tabultate sintaxis. (defaults to None). Possible column alignments are: 
                 right, center, left, decimal (only for numbers), and None (to disable alignment). Omitting an 
                 alignment uses the default.
    """
    number=len(lod_) if number is None else number
    if len(lod_)==0:
        print(_("This list of dictionaries hasn't data to print"))
    print(tabulate(lod_[0:number], headers="keys", tablefmt="psql", colalign=align))

def lod_sum(lod_, key, ignore_nones=True):
    r=0
    for d in lod_:
        if ignore_nones is True and d[key] is None:
            continue
        r=r+d[key]
    return r

def lod_sum_negatives(lod_, key):
    r=0
    for d in lod_:
        if d[key] is None or d[key]>0:
            continue
        r=r+d[key]
    return r

def lod_sum_positives(lod_, key):
    r=0
    for d in lod_:
        if d[key] is None or d[key]<0:
            continue
        r=r+d[key]
    return r

def lod_average(lod_, key):
    return lod_sum(lod_,key)/len(lod_)

def lod_average_ponderated(lod_, key_numbers, key_values):
    prods=0
    for d in lod_:
        prods=prods+d[key_numbers]*d[key_values]
    return prods/lod_sum(lod_, key_numbers)

def lod_count(lod_, lambdafunction):
    """
        Counts dictionaries that cumpliments lambda function
        lod_count(lod, lambda d,index: d["cmd"]==1)
    """
    r=0   
    for index,  d in enumerate(lod_):
        if lambdafunction(d,index) is True:
            r+=1
    return r

def lod_median(lod_, key):
    from statistics import median
    return median(lod2list(lod_, key, sorted=True))

## Converts a lod_ to a dict using key as new dict key, and value as the key of the value field
def lod2dictkv(lod_, key, value):
    d={}
    for ld in lod_:
        d[ld[key]]=ld[value]
    return d

## Converts a lod_ to a dict using key as new dict key, and the dict as a value
def lod2dod(lod_, key):
    d={}
    for ld in lod_:
        d[ld[key]]=ld
    return d
    
## Converts a lod_ to an ordered dictionary of dictionarys
def lod2odod(lod_, key):
    d=OrderedDict()
    for ld in lod_:
        d[ld[key]]=ld
    return d
    
## Converts a lod_ to a dict using (key1,key2) tuple  as new dict key, and the dict as a value
def lod2dod_tuple(lod_, key1, key2):
    d={}
    for ld in lod_:
        d[(ld[key1],ld[key2])]=ld
    return d

## Converts a dict of dictionaries (prefered orderdict) to a list of dictionaries
def dod2lod(d):
    r=[]
    for k,v in d.items():
        r.append(v)
    return r

## Returns a list from a lod_ key
## @param lod_
## @param key String with the key to extract
## @param sorted Boolean. If true sorts final result
## @param cast String. "str", "float", casts the content of the key
def lod2list(lod_, key, sorted=False, cast=None):
    r=[]
    for ld in lod_:
        if cast is None:
            r.append(ld[key])
        elif cast == "str":
            r.append(str(ld[key]))
        elif cast == "float":
            r.append(float(ld[key]))
    if sorted is True:
        r.sort()
    return r

## Returns a list from a lod_ key, with distinct values, not all values
## @param lod_
## @param key String with the key to extract
## @param sorted Boolean. If true sorts final result
## @param cast String. "str", "float", casts the content of the key
def lod2list_distinct(lod_, key, sorted=False, cast=None):
    set_=set()
    for ld in lod_:
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


## Converts a list of ordereddict to a list of rows. ONLY DATA
## @params keys If None we must suppose is an ordered dict or keys will be randomized
def lod2lol(lod_,  keys=None):
    if len(lod_)==0:
        return []
        
    if keys is None:
        keys=lod_[0].keys()
        
    r=[]  
    for od in lod_:
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


## Returns maximum value of a given key. Is unique. REturns NOne if lod_ is empty
def lod_max_value(ld, key):
     if len(ld)>0:
          r=ld[0][key]
     else:
         return None
     for d in ld:
         if  d[key]>r:
             r=d[key]
     return r

## Returns minimum value of a given key. Is unique. REturns NOne if lod_ is empty
def lod_min_value(ld, key):
     if len(ld)>0:
          r=ld[0][key]
     else:
         return None
     for d in ld:
         if  d[key]<r:
             r=d[key]
     return r

def lod_remove_duplicates(lod_):
    """
        Remove duplicated dictionaries (same keys and values) from a list of dictionaries
        Params:
            - lod_ List of dictionaries
        Returns:
            A list of dictionaries
    """
    seen = set()
    unique_dicts = []
    for d in lod_:
        # Convert dictionary to a tuple of its items for hashability
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            unique_dicts.append(d)
    return unique_dicts

def lod_rename_key(ld, from_, to_):
    """
        Renames a key(from_) to another key(to_) in each dictionary in ld
    """
    for d in ld:
        d[to_]=d.pop(from_)
    return ld

def lod_remove_key(lod_, key):
    """
        Removes a key from all dictionaries in a list of dictionaries
    """
    for d in lod_:
        del d[key]
    return lod_
    
def lod_keys(lod_):
    """
        Return the keys of the list of dicts
        Return None if length of lod_ is 0. 
        Retuurn the keys of the first dictionary as a list
    """
    if len(lod_)>0:
        return list(lod_[0].keys())
    return None
    
def lod_clone(lod_):
    new_lod=[]
    for d in lod_:
        new_d={}
        for key, value in d.items():
            new_d[key]=value
        new_lod.append(new_d)
    return new_lod

def lod_filter_keys(lod_, keys):
    """
        Create a new lod_ leaving only keys in parameter
        @param keys List of keys to copy in new lod_
    """
    new_lod=[]
    for d in lod_:
        new_d={}
        for key in keys:
            new_d[key]=d[key]
        new_lod.append(new_d)
    return new_lod


def lod_filter_dictionaries(lod_, lambda_function):
    """
        Create a new lod_ leaving filtering dictionaries that returns True to lambda funcion
        @param lambda_function needs two parameters (d, index) where d is the dictionary used to iterate and index is the position of the dictionary in the list of dictionaries
    """
    new_lod=[]
    for index,  d in enumerate(lod_):
        if lambda_function(d, index) is True:
            new_lod.append(d)
    return new_lod
    
def lod_calculate(lod_, key, lambda_function, clone=False):
    """
        Creates or replaces a column with the result of tthe lambda function in the lod_ passed as parameter
        @param key  Dictionary key where lambda_function result is going to be set
        @param lambda_function needs two parameters (d, index) where d is the dictionary used to iterate and index is the position of the dictionary in the list of dictionaries
        @param clone if True returns a clone of the lod_ parameter
    """
    if clone is True:
        l_o_d=lod_clone(lod_)
    else:
        l_o_d=lod_
        
    for index,  d in enumerate(l_o_d):
        d[key]=lambda_function(d, index)
    return l_o_d



    
    
