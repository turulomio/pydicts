# pydicts
Module to use dictionaries in various situations

## Acronyms
pydicts uses several acronyms to call functions and parameters

- lod: List of dictionaries
- lood: List of ordered dictionaries (OrderedDicts from collections module)
- lol: List of lists 

## LOD
### lod_has_key
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

## Testing
poetry run pytest

## CHANGELOG
### 0.1.0 (2023-04-10)
- First version addapting listdict_functions from reusingcode
