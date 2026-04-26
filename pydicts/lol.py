from gettext import translation
from importlib.resources import files
from pydicts import exceptions
from tabulate import tabulate
        
try:
    t=translation('pydicts', files("pydicts") / 'locale')
    _=t.gettext
except:
    _=str


## LOR is a list of list. 
def lol_add_column(rows, index, column):
    """
    Adds a new column to a list of lists (LoL) at a specified index.

    Args:
        rows (list): The original list of lists.
        index (int): The index at which to insert the new column.
        column (list): A list of values representing the new column.
                       Its length must match the number of rows in `rows`.

    Returns:
        list: A new list of lists with the added column.
    """
    if len(rows)!=len(column):
        raise exceptions.LolException(_("I can't add a column with different size of lol"))
    r_rows=[]
    for i, row in enumerate(rows):
        r_rows.append(row[0:index] + [column[i],] + row[index:len(row)])
    return r_rows

def lol_add_row(lol_, index, row):
    """
    Adds a new row to a list of lists (LoL) at a specified index.

    Args:
        lol_ (list): The original list of lists.
        index (int): The index at which to insert the new row.
        row (list): The new row to add. Its length must match the length of existing rows.

    Returns:
        list: The modified list of lists with the added row.

    Raises:
        exceptions.LolException: If the new row's size is different from existing rows.
    """
    if len(lol_)>0 and len(lol_[0])!=len(row):
        raise exceptions.LolException(_("I can't add a row with different size of the first row of the lol"))
    lol_.insert(index, row)
    return lol_

## Returns a list with object in positions removed
def list_remove_positions(l, listindex):
    """
    Removes elements from a list at specified indices.

    Args:
        l (list): The original list.
        listindex (list): A list of integer indices to remove.

    Returns:
        list: A new list with elements at the specified indices removed.
    """
    if l is None:
        raise exceptions.LolException(_("I can't remove positions from a None list"))
    r=[]
    for i, o in enumerate(l):
        if i not in listindex:
            r.append(o)
    return r

def lol_order_by(lol_, index, reverse=False, none_at_top=True):
    """
    Orders a list of lists (LoL) by the value at a specified column index.

    Args:
        lol_ (list): The list of lists to sort.
        index (int): The column index to sort by.
        reverse (bool, optional): If True, sort in descending order. Defaults to False.
        none_at_top (bool, optional): If True, None values are placed at the beginning of the list.
                                      If False, None values are placed at the end. Defaults to True.

    Returns:
        list: The sorted list of lists.
    """
    
    nonull=[]
    null=[]
    for o in lol_:
        com=o[index]
        if com is None:
            null.append(o)
        else:
            nonull.append(o)
    nonull=sorted(nonull, key=lambda item: item[index], reverse=reverse)
    if none_at_top==True:#Set None at top of the list
        return null+nonull
    else:
        return nonull+null


def lol_remove_columns(rows, list_of_indexes):
    """
    Removes specified columns from a list of lists (LoL).

    Args:
        rows (list): The original list of lists.
        list_of_indexes (list): A list of integer indices of columns to remove.

    Returns:
        list: A new list of lists with the specified columns removed.
    """
    r_rows=[]
    for i, row in enumerate(rows):
        r_rows.append(list_remove_positions(row,list_of_indexes))
    return r_rows

def lol_remove_rows(rows, listindex):
    """
    Removes specified rows from a list of lists (LoL).

    Args:
        rows (list): The original list of lists.
        listindex (list): A list of integer indices of rows to remove.

    Returns:
        list: A new list of lists with the specified rows removed.
    """
    return list_remove_positions(rows, listindex) #It's a list but of row

def lol_transposed(lol):
    """
    Transposes a list of lists (LoL), swapping rows and columns.

    Args:
        lol (list): The original list of lists.

    Returns:
        list: A new list of lists representing the transposed data.

    Raises:
        exceptions.LolException: If the input `lol` is None.
    """
    if lol is None:
        raise exceptions.LolException(_("I can't traspaso a None object"))
    if len(lol)==0:
        return []
    r=[]
    columns=len(lol[0])
    for column in range(columns):
        tran_row=[]
        for row in lol:
            tran_row.append(row[column])
        r.append(tran_row)
    return r

def lol_get_row(lol, row):
    """
    Extracts a specific row from a list of lists (LoL).

    Args:
        lol (list): The list of lists.
        row (int): The index of the row to extract.

    Returns:
        list: The extracted row.
    """
    return lol[row]

def lol_get_column(lol, column):
    """
    Extracts a specific column from a list of lists (LoL).

    Args:
        lol (list): The list of lists.
        column (int): The index of the column to extract.

    Returns:
        list: A list containing all values from the specified column.
    """
    r=[]
    for row in lol:
        r.append(row[column])
    return r

def lol_sum_row(row, from_index=0, to_index=None, zerovalue=0):
    """
    Calculates the sum of values in a specific range of a row.
    None values are ignored.

    Args:
        row (list): The row (list of values) to sum.
        from_index (int, optional): The starting index for summing. Defaults to 0.
        to_index (int, optional): The ending index for summing. If None, sums to the end of the row.
                                  Defaults to None.
        zerovalue (int, float, Decimal, Currency, optional): The initial value for the sum.
                                                              Useful for summing custom objects like Currency. Defaults to 0.

    Returns:
        (int, float, Decimal, Currency): The sum of the values in the specified range.
    """
    s=zerovalue
    for i, column in enumerate(row):
        if i>=from_index and i<=to_index:
            if column is not None:
                s=s + column
    return s

## Return sum of values of a column from and index to and other index position. This method ignores None values
def lol_sum_column(lol, column, from_index, to_index, zerovalue=0):
    """
    Calculates the sum of values in a specific column across a range of rows.
    None values are ignored.

    Args:
        lol (list): The list of lists.
        column (int): The index of the column to sum.
        from_index (int): The starting row index for summing.
        to_index (int): The ending row index for summing.
        zerovalue (int, float, Decimal, Currency, optional): The initial value for the sum.
                                                              Useful for summing custom objects like Currency. Defaults to 0.

    Returns:
        (int, float, Decimal, Currency): The sum of the values in the specified column and row range.
    """
    s=zerovalue
    for i, row in enumerate(lol):
        if i>=from_index and i<=to_index:
            if row[column] is not None:
                s=s + row[column]
    return s

def lol_print(lol_, number=None, align=None):
    """
    Prints a list of lists (LoL) in a tabular format using the `tabulate` module.

    Args:
        lol_ (list): The list of lists to print.
        number (int, optional): The maximum number of rows to print. If None, all rows are printed.
                                Defaults to None.
        align (list, optional): A list of strings specifying column alignment. Possible values are
                                "right", "center", "left", "decimal", or None. Defaults to None.
    """
    number=len(lol_) if number is None else number

    if len(lol_)==0:
        print(_("lol_print: This list of lists hasn't data to print"))
        return
    if number==0:
        print(_("lol_print: No data was printed due to you selected 0 rows"))
        return
    print(tabulate(lol_[0:number], tablefmt="psql", colalign=align))
