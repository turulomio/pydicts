# pydicts
Module to use dictionaries in various situations

## Acronyms
pydicts uses several acronyms to call functions and parameters

- lod: List of dictionaries `[{"a":1,"b":2}, {"a":3,"b":4}]`
- lood: List of ordered dictionaries (OrderedDicts from collections module) `[OrderedDict([('a', 1), ('b', 2)]), OrderedDict([('a', 3), ('b', 4)])]`
- lol: List of lists `[[1, 2, 3], [4, 5, 6]]` 
- dod: Dictionary of dictionaries `{'key2': {'a': 1, 'b': 2}, 'key1': {'a': 1, 'b': 2}}`
- lod_ymv: List of dictionaries with year-month-value keys `[{'year': 2021, 'month': 1, 'value': 12.12}, {'year': 2023, 'month': 3, 'value': 13.03}]`
- lod_xyv: List of dictionaries with x-y-value keys `[{'X': 21, 'Y': 12, 'value': 180}, {'X': 2, 'Y': 122, 'value': 170}]`

## LOD
### lod_has_key

Returns a boolean. Checks if list of dictionaries has a key

```python
>>> from pydicts.lod import lod_has_key
>>> lod=[{"a":1, "b":4},{"a":2, "b":5}]
>>> lod_has_key(lod,"a")
True
>>> lod_has_key(lod,"d")
False
>>> lod_has_key([],"d")
False
```

### lod_print

Prints a list of dictionaries in a tabulated way

```python
>>> from pydicts.lod import lod_print
>>> lod=[{"a":1, "b":4},{"a":2, "b":None}]
>>> lod_print(lod)
+-----+-----+
|   a |   b |
|-----+-----|
|   1 |   4 |
|   2 |     |
+-----+-----+
```

### lod_sum

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


## Testing
poetry run pytest

## CHANGELOG

### 0.2.0 (2023-04-12)
- Added lod_print with tabulate module
- Improving documentation
- Refactorized modules to lod_xyv, lod_ymmv

### 0.1.0 (2023-04-10)
- First version addapting listdict_functions from reusingcode
