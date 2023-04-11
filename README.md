# pydicts
Module to use dictionaries in various situations

## Acronyms
pydicts uses several acronyms to call functions and parameters

- lod: List of dictionaries
- lood: List of ordered dictionaries (OrderedDicts from collections module)
- lol: List of lists 

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
### 0.1.0 (2023-04-10)
- First version addapting listdict_functions from reusingcode
