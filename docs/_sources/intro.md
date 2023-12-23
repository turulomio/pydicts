# Pydicts project

:::{note}
    In construction. Please help me
:::

## Casts

Casting is essential in programming. With Pydicts I try to put together main castings, to work easyly with all king of data structures.



## Data structures

PyDicts uses several acronyms to call modulues, functions and parameters

- **LOD**: List of dictionaries `[{"a":1,"b":2}, {"a":3,"b":4}]`
- **LOOD**: List of ordered dictionaries (OrderedDicts from collections module) `[OrderedDict([('a', 1), ('b', 2)]), OrderedDict([('a', 3), ('b', 4)])]`
- **LOL**: List of lists `[[1, 2, 3], [4, 5, 6]]` 
- **DOD**: Dictionary of dictionaries `{'key2': {'a': 1, 'b': 2}, 'key1': {'a': 1, 'b': 2}}`
- **ODOD**: Ordered dictionary of dictionaries `OrderedDict({'key2': {'a': 1, 'b': 2}, 'key1': {'a': 1, 'b': 2}})`
- **LOD_XYV**: List of dictionaries with x-y-value keys `[{'X': 21, 'Y': 12, 'value': 180}, {'X': 2, 'Y': 122, 'value': 170}]`
- **LOD_YMV**: List of dictionaries with year-month-value keys `[{'year': 2021, 'month': 1, 'value': 12.12}, {'year': 2023, 'month': 3, 'value': 13.03}]`

You can read modules documentation:

- [LOD (List of dictionaries)](lod.md))
- [LOL (List of lists)](lol.md)
