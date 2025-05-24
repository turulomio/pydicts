---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# LOD

## dod2lod

Converts a dictionary of dictionaries (dod) to a list of dictionaries (lod), ignoring dictionary keys

```{code-cell}
from pydicts import lod
dod={'key2': {'a': 1, 'b': 2}, 'key1': {'a': 1, 'b': 2}}
lod.dod2lod(dod)

```

## lod2dictkv
Converts a list of dictionaries (lod) to a dictionary using a key for the new key and another key for its value


```{code-cell}
from pydicts import lod
lod_=[{"a":1,"b":2}, {"a":3,"b":4}]
lod.lod2dictkv(lod_,"a","b")

```


## lod2dod

Converts a list of dictionaries (lod) to a dictionary of dictionaries (dod) using a key as the dictionary key. This is a fast method to access dictionaries.

```{code-cell}
from pydicts import lod
lod_=[{"a":1,"b":2}, {"a":3,"b":4}]
lod.lod2dod(lod_,"b")
```

## lod2dod_tuple

```{code-cell}
:tags: [remove-input]

from pydicts import lod
help(lod.lod2dod_tuple)
```




## lod2list

Converts a list of dictionaries (lod) to list using all values of key
```{code-cell}
from pydicts import lod
lod_=[{"a":1,"b":2}, {"a":3,"b":4}]
lod.lod2list(lod_,"a")
```


## lod2list_distinct

Converts a list of dictionaries (lod) to list using all distinct values of key

```{code-cell}
from pydicts import lod
lod_= [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}, {'a': 3, 'b': 4}]
print("lod2list:",lod.lod2list(lod_,"a"))
print("lod2list_distinct:",lod.lod2list_distinct(lod_,"a"))
```


## lod2lol

Converts a list of dictionaries (lod) to a list of lists

If you don't select keys (Supposed ordereddict)

```{code-cell}
from pydicts import lod
lod_= [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}, {'a': 3, 'b': 4}]
lod.lod2lol(lod_)
```

You can select your keys in the order you need

```{code-cell}
from pydicts import lod
lod_= [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}, {'a': 3, 'b': 4}]
lod.lod2lol(lod_,["b","a"])
```

## lod2lood

```{code-cell}
:tags: [remove-input]

from pydicts import lod
help(lod.lod2lood)
```

## lod_average

Calculates average from all values is the list of dictionaries with the key passed as parameter.

```{code-cell}
from pydicts.lod import lod_print,lod_average
lod_=[{"a":1, "b":2},{"a":3, "b":2},{"a":5, "b":2}]
lod_print(lod_)
print(lod_average(lod_,"a"))
```

## lod_average_ponderated

Calculates average ponderated from all values is the list of dictionaries with the key passed as parameter, and the weight passed as a parameter.

```{code-cell}
from pydicts.lod import lod_print,lod_average_ponderated
lod_=[{"a":1, "b":1},{"a":3, "b":2},{"a":5, "b":3}]
lod_print(lod_)
print(lod_average_ponderated(lod_,"a","b"))
```

## lod_calculate
Makes calculations inside dictionary iterations
```{code-cell}
from pydicts import lod
lod_= [{'a': 1, 'b': 2, 'c':5}, {'a': 3, 'b': 4, 'c': 6}, {'a': 3, 'b': 4, 'c': 7}]
lod.lod_calculate(lod_, "d", lambda d, index: d['a']+d['b']+d['c'])
```

## lod_clone

Makes a clone of the list of dictionaries with a new list and new dictionaries


## lod_count

Count values in a list of dictioanries
```{code-cell}
from pydicts import lod
lod_= [{'a': 1, 'b': 2, 'c':5}, {'a': 3, 'b': 4, 'c': 6}, {'a': 3, 'b': 4, 'c': None}]

a=lod.lod_count(lod_,lambda d, index: d["a"]>3)
b=lod.lod_count(lod_,lambda d, index: d["c"] is None)
c=lod.lod_count(lod_,lambda d, index: index>=0)
print(a,b,c)
```

## lod_filter_dictionaries

Create a new lod leaving filtering dictionaries that returns True to lambda funcion
```{code-cell}
from pydicts import lod
lod_= [{'a': 1, 'b': 2, 'c':5}, {'a': 3, 'b': 4, 'c': 6}, {'a': 3, 'b': 4, 'c': 7}]
lod.lod_filter_dictionaries(lod_, lambda d, index: index >0 and d['c']> 6)
```


## lod_filter_keys

Creates a new list of dictionaries with dictionaries that only have the keys passed as parameters

```{code-cell}
from pydicts import lod
lod_= [{'a': 1, 'b': 2, 'c':5}, {'a': 3, 'b': 4, 'c': 6}, {'a': 3, 'b': 4, 'c': 7}]
lod.lod_print(lod_)
new_lod=lod.lod_filter_keys(lod_,  ["a", "c"])
lod.lod_print(new_lod)
```

## lod_has_key

Returns a boolean. Checks if list of dictionaries has a key

```{code-cell}
from pydicts.lod import lod_has_key
lod=[{"a":1, "b":4},{"a":2, "b":5}]
print(lod_has_key(lod,"a"))
print(lod_has_key(lod,"d"))
print(lod_has_key([ ],"d"))
```

## lod_keys

Returns a list with the keys of the first dictionary in the list

```{code-cell}
from pydicts import lod
a=[{"a":1,"b":2}, {"a":3,"b":4}]
lod.lod_keys(a)
```

## lod_max_value

Returns the maximum value of a key in a list of dictionaries (lod)

```{code-cell}
from pydicts import lod
lod_=[{"a":1,"b":2}, {"a":3,"b":4}]
lod.lod_max_value(lod_,"b")
```

## lod_median

Calculates median from all values is the list of dictionaries with the key passed as parameter.

```{code-cell}
from pydicts.lod import lod_print,lod_median
lod_=[{"a":1, "b":2},{"a":3, "b":2},{"a":5, "b":2}]
lod_print(lod_)
print(lod_median(lod_,"a"))
```

## lod_min_value

Returns the minimum value of a key in a list of dictionaries (lod)

```{code-cell}
from pydicts import lod
lod_=[{"a":1,"b":2}, {"a":3,"b":4}]
lod.lod_min_value(lod_,"b")
```

## lod_order_by

Orders a list of dictionaries (lod) by a key. You can make reverse orders and set None values at the top or the bottom of the ordered list

```{code-cell}
from pydicts import lod
lod_=[{"a":1,"b":2}, {"a":3,"b":4}, {"a":3, "b": None}]
lod.lod_order_by(lod_,"b")
```

```{code-cell}
from pydicts import lod
lod_=[{"a":1,"b":2}, {"a":3,"b":4}, {"a":3, "b": None}]
lod.lod_order_by(lod_,"b",reverse=True)
```

```{code-cell}
from pydicts import lod
lod_=[{"a":1,"b":2}, {"a":3,"b":4}, {"a":3, "b": None}]
lod.lod_order_by(lod_,"b",reverse=True, none_at_top=False)
```


## lod_print


```{code-cell}
:tags: [remove-input]

from pydicts import lod
help(lod.lod_print)
```


```{code-cell}
from pydicts.lod import lod_print
lod_=[{"a":1, "b":4},{"a":2, "b":None}]
lod_print(lod_, align=['center', 'right'])
```

## lod_rename_key

Renames a key name with other given as a parameter

```{code-cell}
from pydicts import lod
lod_=[{"a":1,"b":2}, {"a":3,"b":4}, {"a":3, "b": 4}]
lod.lod_rename_key(lod_,"b","new")
```

## lod_remove_duplicates

Removes duplicates (dictionaries with the same keys and values) from a list of dictionaries.

```{code-cell}
from pydicts.lod import lod_print, lod_remove_duplicates
lod_=[{"a":1, "b":2},{"a":1, "b":2},{"a":1, "b":2}]
lod_print(lod_)
lod_=lod_remove_duplicates(lod_)
lod_print(lod_)
```

## lod_remove_key

Removes a key in all dictionaries in the list of dictionaries

```{code-cell}
from pydicts.lod import lod_print, lod_remove_key
lod=[{"a":1, "b":4},{"a":2, "b":None}]
lod_print(lod)
lod_remove_key(lod,"b")
lod_print(lod)
```

## lod_sum

Sums all values from a lod key. None values are ignored by default

```{code-cell}
from pydicts.lod import lod_sum
lod=[{"a":1, "b":4},{"a":2, "b":None}]
lod_sum(lod,"a")
```

## lod_sum_negatives

```{code-cell}
:tags: [remove-input]

from pydicts import lod
help(lod.lod_sum_negatives)
```

## lod_sum_positives

```{code-cell}
:tags: [remove-input]

from pydicts import lod
help(lod.lod_sum_positives)
```

