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

## dod_print

Prints in console a dictionary of nested dictionaries nicely

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
