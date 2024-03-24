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

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.base64bytes2bytes)
```

### bytes2base64bytes
```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.bytes2base64bytes)
```

### bytes2str

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.bytes2str)
```
### dtaware2dtnaive

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.dtaware2dtnaive)
```
### dtaware2epochmicros

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.dtaware2epochmicros)
```
### dtaware2epochms

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.dtaware2epochms)
```
### dtaware2str

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.dtaware2str)
```
### dtnaive2dtaware

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.dtnaive2dtaware)
```

### dtnaive2str

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.dtnaive2str)
```

### epochmicros2dtaware

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.epochmicros2dtaware)
```

### epochms2dtaware

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.epochms2dtaware)
```

### none2alternative

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.none2alternative)
```

### str2bool

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.str2bool)
```

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

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.str2bytes)
```

### str2date

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.str2date)
```

### str2decimal

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.str2decimal)
```

### str2dtaware

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.str2dtaware)
```

### str2dtnaive

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.str2dtnaive)
```

### str2time

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.str2time)
```

### str2timedelta

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.str2timedelta)
```

### time2str

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.time2str)
```

### timedelta2str

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.timedelta2str)
```

## Date and time utils

### date_first_of_the_month

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.date_first_of_the_month)
```

### date_first_of_the_next_x_months

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.date_first_of_the_next_x_months)
```

### date_first_of_the_year

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.date_first_of_the_year)
```

### date_last_of_the_month

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.date_last_of_the_month)
```

### date_last_of_the_next_x_months

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.date_last_of_the_next_x_months)
```

### date_last_of_the_year

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.date_last_of_the_year)
```

### dtaware

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.dtaware)
```

### dtaware_changes_tz

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.dtaware_changes_tz)
```

### dtaware_day_end

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.dtaware_day_end)
```

### dtaware_day_end_from_date

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.dtaware_day_end_from_date)
```

###  dtaware_day_start

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.dtaware_day_start)
```

### dtaware_day_start_from_date

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.dtaware_day_start_from_date)
```

### dtaware_month_end

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.dtaware_month_end)
```

### dtaware_month_start

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.dtaware_month_start)
```

### dtaware_now

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.dtaware_now)
```

Returns a aware datetime object of current moment. By default returns UTC timezone

```{code-cell}
from pydicts import casts
print(casts.dtaware_now())
print(casts.dtaware_now("Europe/Madrid"))
```


### dtaware_year_end

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.dtaware_year_end)
```

### dtaware_year_start

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.dtaware_year_start)
```

### dtnaive

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.dtnaive)
```


### dtnaive_day_end

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.dtnaive_day_end)
```

### dtnaive_day_end_from_date

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.dtnaive_day_end_from_date)
```

###  dtnaive_day_start

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.dtnaive_day_start)
```

### dtnaive_day_start_from_date

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.dtnaive_day_start_from_date)
```

### dtnaive_now

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.dtnaive_now)
```

Returns a naive datetime object of current moment. By default returns UTC timezone

```{code-cell}
from pydicts import casts
casts.dtnaive_now()
```

### is_aware

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.is_aware)
```

Returns if a datetime object is aware (with timezone) 

```{code-cell}
from pydicts import casts
print(casts.is_aware(casts.dtaware_now()))
print(casts.is_aware(casts.dtnaive_now()))
```

### is_naive

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.is_naive)
```

```{code-cell}
from pydicts import casts
print(casts.is_naive(casts.dtaware_now()))
print(casts.is_naive(casts.dtnaive_now()))
```

### months

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.months)
```


## Other utils

### is_noe

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.is_noe)
```

Return if value is None or an empty string

```{code-cell}
from pydicts import casts
print(casts.is_noe(None))
print(casts.is_noe(""))
print(casts.is_noe(1))
```


### object_or_empty

```{code-cell}
:tags: [remove-input]

from pydicts import casts
help(casts.object_or_empty)
```

