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

### base64bytes2bytes

### bytes2base64bytes

### bytes2str

### dtaware2dtnaive

### dtaware2epochmicros

### dtaware2epochms

### dtaware2str

### dtnaive2dtaware

### dtnaive2str

### epochmicros2dtaware

### epochms2dtaware

### none2alternative

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


### str2bytes

### str2date

### str2decimal

### str2dtaware

### str2dtnaive

### str2time

### str2timedelta

### time2str

### timedelta2str

## Date and time utils

### date_first_of_the_month

### date_first_of_the_next_x_months

### date_first_of_the_year

### date_last_of_the_month

### date_last_of_the_next_x_months

### date_last_of_the_year

### dtaware

### dtaware_changes_tz

### dtaware_day_end

### dtaware_day_end_from_date

###  dtaware_day_start

### dtaware_day_start_from_date

### dtaware_month_end

### dtaware_month_start

### dtaware_now

### dtaware_year_end

### dtaware_year_start

### dtnaive


### dtnaive_day_end

### dtnaive_day_end_from_date

###  dtnaive_day_start

### dtnaive_day_start_from_date

### dtnaive_now

### is_aware

### is_naive

### months


## Other utils

### is_noe

Return if value is None or an empty string

```{code-cell}
from pydicts import casts
print(casts.is_noe(None))
print(casts.is_noe(""))
print(casts.is_noe(1))
```


### object_or_empty

