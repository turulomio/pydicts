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
# Casts

## str2bool

Converts a string to a boolean

```{code-cell}
from pydicts import casts
casts.str2bool("true")
```
```{code-cell}
from pydicts import casts
casts.str2bool("0")
```

`casts.str2bool(None)` will throw a CastException, but you can 

```{code-cell}
from pydicts import casts
print(casts.str2bool(None,ignore_exception=True))
```
