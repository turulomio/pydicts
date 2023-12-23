## lol_add_column

## lol_print

Prints a list of lists in a tabulated way

```python
>>> from pydicts.lol import lol_print
>>> lol_=[[1, 2, 3], [4, 5, 6]]
>>> lol.lol_print(lol_)
+---+---+---+
| 1 | 2 | 3 |
| 4 | 5 | 6 |
+---+---+---+
```


## list_remove_positions

## lol_remove_columns

## lol_remove_rows

## lol_transposed

Returns a trasnsposed list of lists 

```python
>>> from pydicts.lol import lol_transposed
>>> lol_=[[1, 2, 3], [4, 5, 6]]
>>> lol.lol_print(lol_)
+---+---+---+
| 1 | 2 | 3 |
| 4 | 5 | 6 |
+---+---+---+
>>> transposed=lol.lol_transposed(lol_)
>>> lol.lol_print(transposed)
+---+---+
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |
+---+---+
```

## lol_get_column

## lol_sum_row

## lol_sum_column
