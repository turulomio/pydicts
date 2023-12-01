# PyDicts  [![PyPI - Downloads](https://img.shields.io/pypi/dm/pydicts?label=Pypi%20downloads)](https://pypi.org/project/pydicts/)

Module to use dictionaries, list of dictionaries and other data structures 

I've developed this module because I needed this kind of methods developing with Django and python

## Links

- https://github.com/turulomio/pydicts/
- https://pypi.org/project/pydicts/


## MODULES

PyDicts uses several acronyms to call modulues, functions and parameters

- lod: List of dictionaries `[{"a":1,"b":2}, {"a":3,"b":4}]`
- lood: List of ordered dictionaries (OrderedDicts from collections module) `[OrderedDict([('a', 1), ('b', 2)]), OrderedDict([('a', 3), ('b', 4)])]`
- lol: List of lists `[[1, 2, 3], [4, 5, 6]]` 
- dod: Dictionary of dictionaries `{'key2': {'a': 1, 'b': 2}, 'key1': {'a': 1, 'b': 2}}`
- lod_ymv: List of dictionaries with year-month-value keys `[{'year': 2021, 'month': 1, 'value': 12.12}, {'year': 2023, 'month': 3, 'value': 13.03}]`
- lod_xyv: List of dictionaries with x-y-value keys `[{'X': 21, 'Y': 12, 'value': 180}, {'X': 2, 'Y': 122, 'value': 170}]`

You can read modules documentation:

- [lod](docs/LOD.md)


## CHANGELOG

## 0.8.0 (2023-11-26)
- Migrating casts and datetime_functions to pydicts.casts. Utils to make casting easy
- Create lol (List of lists) module

### 0.7.0 (2023-11-04)
- Improved documentation
- Removed duplicated lod_min and lod_max methods
- Added lod_filter_keys function
- Added lod_filter_dictionaries function
- Added lod_clone function
- Added lod_calculate function

### 0.6.0 (2023-07-02)
- Fixed a race condition bug in lod_ymv_transposition_with_percentages

### 0.5.0 (2023-05-04)
- Added support to latex tables from list of dictionaries

### 0.4.0 (2023-04-19)
- Added poetry support
- Added poethepoet support
- Added lod_remove_key

### 0.3.0 (2023-04-16)
- Added lod_ymv_transposition_with_porcentages

### 0.2.0 (2023-04-12)
- Added lod_print with tabulate module
- Improving documentation
- Refactorized modules to lod_xyv, lod_ymmv

### 0.1.0 (2023-04-10)
- First version addapting listdict_functions from reusingcode
