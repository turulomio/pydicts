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

# prueba

Converts a dictionary of dictionaries (dod) to a list of dictionaries (lod), ignoring dictionary keys

```{code-cell}
from pydicts import lod
dod={'key2': {'a': 1, 'b': 2}, 'key1': {'a': 1, 'b': 2}}
lod.dod2lod(dod)

```


``` python
>>> from pydicts import lod
>>> dod={'key2': {'a': 1, 'b': 2}, 'key1': {'a': 1, 'b': 2}}
>>> lod.dod2lod(dod)
[{'a': 1, 'b': 2}, {'a': 1, 'b': 2}]

```
# lod2dictkv

# lod2dod

Converts a list of dictionaries (lod) to a dictionary of dictionaries (dod) using a key as the dictionary key. This is a fast method to access dictionaries.
``` python
>>> from pydicts import lod
>>> lod_=[{"a":1,"b":2}, {"a":3,"b":4}]
>>> lod.lod2dod(lod_,"b")
{2: {'a': 1, 'b': 2}, 4: {'a': 3, 'b': 4}}
```

# lod2dod_tuple

# lod2list

Converts a list of dictionaries (lod) to list using all values of key
``` python
>>> from pydicts import lod
>>> lod_=[{"a":1,"b":2}, {"a":3,"b":4}]
>>> lod.lod2list(lod_,"a")
[1, 3]
```

# lod2list_distinct

Converts a list of dictionaries (lod) to list using all distinct values of key
``` python
>>> from pydicts import lod
>>> lod_= [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}, {'a': 3, 'b': 4}]
>>> lod.lod2list_distinct(lod_,"b")
[2, 4]
>>> lod.lod2list(lod_,"b")
[2, 4, 4]
```


# lod2lol

# lod2lood

# lod_average

# lod_average_ponderated

# lod_calculate
Makes calculations inside dictionary iterations
```python
>>> from pydicts import lod
>>> lod_= [{'a': 1, 'b': 2, 'c':5}, {'a': 3, 'b': 4, 'c': 6}, {'a': 3, 'b': 4, 'c': 7}]
>>> lod.lod_calculate(lod_, "d", lambda d, index: d['a']+d['b']+d['c'])
[{'a': 1, 'b': 2, 'c': 5, 'd': 8}, {'a': 3, 'b': 4, 'c': 6, 'd': 13}, {'a': 3, 'b': 4, 'c': 7, 'd': 14}]

```

# lod_clone

Makes a clone of the list of dictionaries createing a new list and new dictionaries

# lod_filter_dictionaries

Create a new lod leaving filtering dictionaries that returns True to lambda funcion
```python
>>> from pydicts import lod
>>> lod_= [{'a': 1, 'b': 2, 'c':5}, {'a': 3, 'b': 4, 'c': 6}, {'a': 3, 'b': 4, 'c': 7}]
>>> lod.lod_filter_dictionaries(lod_, lambda d, index: index >0 and d['c']> 6)
[{'a': 3, 'b': 4, 'c': 7}]

```


# lod_filter_keys

Creates a new list of dictionaries with dictionaries that only have the keys passed as parameters

``` python
>>> from pydicts import lod
>>> lod_= [{'a': 1, 'b': 2, 'c':5}, {'a': 3, 'b': 4, 'c': 6}, {'a': 3, 'b': 4, 'c': 7}]
>>> lod.lod_print(lod_)
+-----+-----+-----+
|   a |   b |   c |
|-----+-----+-----|
|   1 |   2 |   5 |
|   3 |   4 |   6 |
|   3 |   4 |   7 |
+-----+-----+-----+

>>> new_lod=lod.lod_filter_keys(lod_,  ["a", "c"])
>>> lod.lod_print(new_lod)
+-----+-----+
|   a |   c |
|-----+-----|
|   1 |   5 |
|   3 |   6 |
|   3 |   7 |
+-----+-----+


```
    

# lod_has_key

Returns a boolean. Checks if list of dictionaries has a key

```python
>>> from pydicts.lod import lod_has_key
>>> lod=[{"a":1, "b":4},{"a":2, "b":5}]
>>> lod_has_key(lod,"a")
True
>>> lod_has_key(lod,"d")
False
>>> lod_has_key([ ],"d")
False
```

# lod_keys

Returns a list with the keys of the first dictionary in the list

```python
>>> from pydicts import lod
>>> a=[{"a":1,"b":2}, {"a":3,"b":4}]
>>> lod.lod_keys(a)
['a', 'b']
>>> lod.lod_keys([ ]) is None
True
```

# lod_max_value

Returns the maximum value of a key in a list of dictionaries (lod)

```python
>>> from pydicts import lod
>>> lod_=[{"a":1,"b":2}, {"a":3,"b":4}]
>>> lod.lod_max_value(lod_,"b")
4
>>>lod.lod_max_value([ ],"b") is None
True
```


# lod_median

# lod_min_value

Returns the minimum value of a key in a list of dictionaries (lod)

```python
>>> from pydicts import lod
>>> lod_=[{"a":1,"b":2}, {"a":3,"b":4}]
>>> lod.lod_min_value(lod_,"b")
2
>>>lod.lod_min_value([ ],"b") is None
True
```

# lod_order_by

Orders a list of dictionaries (lod) by a key. You can make reverse orders and set None values at the top or the bottom of the ordered list

```python
>>> from pydicts import lod
>>> lod_=[{"a":1,"b":2}, {"a":3,"b":4}, {"a":3, "b": None}]
>>> lod.lod_order_by(lod_,"b")
[{'a': 3, 'b': None}, {'a': 1, 'b': 2}, {'a': 3, 'b': 4}]
>>> lod.lod_order_by(lod_,"b",reverse=True)
[{'a': 3, 'b': None}, {'a': 3, 'b': 4}, {'a': 1, 'b': 2}]
>>> lod.lod_order_by(lod_,"b",reverse=True, none_at_top=False)
[{'a': 3, 'b': 4}, {'a': 1, 'b': 2}, {'a': 3, 'b': None}]

```

# lod_print

Prints a list of dictionaries in a tabulated way

```python
>>> from pydicts.lod import lod_print
>>> lod_=[{"a":1, "b":4},{"a":2, "b":None}]
>>> lod_print(lod_)
+-----+-----+
|   a |   b |
|-----+-----|
|   1 |   4 |
|   2 |     |
+-----+-----+
```

# lod_rename_key

Renames a key name with other given as a parameter

```python
>>> from pydicts import lod
>>> lod_=[{"a":1,"b":2}, {"a":3,"b":4}, {"a":3, "b": 4}]
>>> lod.lod_rename_key(lod_,"b","new")
[{'a': 1, 'new': 2}, {'a': 3, 'new': 4}, {'a': 3, 'new': 4}]
```

# lod_remove_key

Removes a key in all dictionaries in the list of dictionaries

```python
>>> from pydicts.lod import lod_print, lod_remove_key
>>> lod=[{"a":1, "b":4},{"a":2, "b":None}]
>>> lod_print(lod)
+-----+-----+
|   a |   b |
|-----+-----|
|   1 |   4 |
|   2 |     |
+-----+-----+
>>> lod_remove_key(lod,"b")
>>> lod_print(lod)
+-----+
|   a |
|-----|
|   1 |
|   2 |
+-----+
```

# lod_sum

Sums all values from a lod key. None values are ignored by default

```python
>>> from pydicts.lod import lod_sum
>>> lod=[{"a":1, "b":4},{"a":2, "b":None}]
>>> lod_sum(lod,"a")
3
>>> lod_sum(lod,"b")
4
>>> lod_sum(lod,"b",ignore_nones=False)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/keko/Proyectos/pydicts/pydicts/lod.py", line 46, in lod_sum
    r=r+d[key]
TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'
```

# lod_sum_negatives

# lod_sum_positives

