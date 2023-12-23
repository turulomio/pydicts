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
