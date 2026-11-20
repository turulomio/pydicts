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

# DOD

## dod_string

Returns a pretty-printed string representation of a dictionary of dictionaries.

```{code-cell}
from pydicts import dod

sample_dod = {
    "emp_1": {"name": "Alice", "role": "admin"},
    "emp_2": {"name": "Bob", "role": "developer"},
}
formatted_str = dod.dod_string(sample_dod, indent=2)
print(formatted_str)
```

## dod_print

Prints a dictionary of dictionaries (DoD) in a human-readable, pretty-printed format.

```{code-cell}
:tags: [remove-input]

from pydicts import dod
help(dod.dod_print)
```

```{code-cell}
from pydicts import dod
from datetime import date, datetime
from decimal import Decimal
d={"a": datetime.now(), "b": date.today(), "c": Decimal('12.32'), "d": None, "e": int(12), "f":None, "g":True, "h":False,  "nested": {"x":1, "y":2, "z":{"n":4, "m":5, "o":6}}}
dod_={}
dod_["first"]=d
dod_["second"]=d
dod.dod_print(dod_)
```

## dod_string_tables and dod_print_tables

Formats and prints the DoD as a table, placing dictionary keys as the first column:

```{code-cell}
from pydicts import dod

sample_dod = {
    "emp_1": {"name": "Alice", "role": "admin", "active": True},
    "emp_2": {"name": "Bob", "role": "developer", "active": True},
}
# Print directly as a table
dod.dod_print_tables(sample_dod, key_name="ID")

# Or obtain the table string representation
table_str = dod.dod_string_tables(sample_dod, key_name="ID")
```



