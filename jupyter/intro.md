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

# Pydicts project


```{code-cell}
:tags: [remove-input]
from pydicts import __version__
print("Version:",  __version__)
```


Module to use dictionaries, list of dictionaries and other data structures

## Project links

* https://github.com/turulomio/pydicts/
* https://pypi.org/project/pydicts/
* [Changelog](./changelog.md)

## Acronyms

PyDicts uses several acronyms to call modulues, functions and parameters

- **LOD**: List of dictionaries `[{"a":1,"b":2}, {"a":3,"b":4}]`
- **LOOD**: List of ordered dictionaries (OrderedDicts from collections module) `[OrderedDict([('a', 1), ('b', 2)]), OrderedDict([('a', 3), ('b', 4)])]`
- **LOL**: List of lists `[[1, 2, 3], [4, 5, 6]]` 
- **DOD**: Dictionary of dictionaries `{'key2': {'a': 1, 'b': 2}, 'key1': {'a': 1, 'b': 2}}`
- **ODOD**: Ordered dictionary of dictionaries `OrderedDict({'key2': {'a': 1, 'b': 2}, 'key1': {'a': 1, 'b': 2}})`
- **LOD_XYV**: List of dictionaries with x-y-value keys `[{'X': 21, 'Y': 12, 'value': 180}, {'X': 2, 'Y': 122, 'value': 170}]`
- **LOD_YMV**: List of dictionaries with year-month-value keys `[{'year': 2021, 'month': 1, 'value': 12.12}, {'year': 2023, 'month': 3, 'value': 13.03}]`

