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
# LOL

## lol_add_column

## lol_add_row

Adds a row at index position

```{code-cell}
from pydicts import lol
lol_=[[1, 2, 3], [4, 5, 6]]
lol_=lol.lol_add_row(lol_, 1, [2,3,5])
lol.lol_print(lol_)

print("""
Will raise error:
    - lol.lol_add_row(lol_, 1, [2,3])
""")
```

## lol_order_by

Order a list of list by column index

```{code-cell}
from pydicts import lol
lol_=[[1, 2, 3], [4, 5, 6], [None, 4, None]]
lol_=lol.lol_order_by(lol_, 2, reverse=True, none_at_top=False)
lol.lol_print(lol_)

```


## lol_print

Prints a list of lists in a tabulated way

```{code-cell}
from pydicts import lol
lol_=[[1, 2, 3], [4, 5, 6]]
lol.lol_print(lol_)

```

## list_remove_positions

## lol_remove_columns

## lol_remove_rows

## lol_transposed

Returns a trasnsposed list of lists 

```{code-cell}
from pydicts.lol import lol_transposed
lol_=[[1, 2, 3], [4, 5, 6]]
lol.lol_print(lol_)
transposed=lol.lol_transposed(lol_)
lol.lol_print(transposed)
```

## lol_get_column

## lol_sum_row

## lol_sum_column
