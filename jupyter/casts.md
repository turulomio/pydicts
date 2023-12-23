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
# Casts and other utils


Casting is essential in programming. With Pydicts I try to put together main castings, to work easyly with all kind of data structures.

## ignore_exception

Morever, this module casting function has two additional parameters, that are useful for rapid development:

- **ignore_exception**. By default False. If you set this parameter to True, casting with return ignore_exception_value if a CastException happens.
- **ignore_exception_value**. By default None. It's the value casting will return if a CastException happens

For example, this code  `casts.str2bool(None)`  will raise a CastException, due to None is not a valid value.

But this code will return None
```{code-cell}
from pydicts import casts
casts.str2bool(None, ignore_exception=True)
```

And this code will return False
```{code-cell}
from pydicts import casts
casts.str2bool(None, ignore_exception=True,ignore_exception_value=False)
```

## Casts

### str2bool

Converts a string to a boolean

```{code-cell}
from pydicts import casts
casts.str2bool("true")
```
```{code-cell}
from pydicts import casts
casts.str2bool("0")
```

These calls will raise CastException:
- `casts.str2bool(None)`
- `casts.str2bool(True)`
- `casts.str2bool("Verdadero")`


## Date and time utils

## Other utils
