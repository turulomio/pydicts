from gettext import translation
from importlib.resources import files
from pydicts import exceptions
from tabulate import tabulate
        
try:
    t=translation('pydicts', files("pydicts") / 'locale')
    _=t.gettext
except:
    _=str


## LOR is a list of list. Naned List Of Rows, used in myqtablewidget for example
## @param rows LOR
## @param index int with the index of the position where we are going to insert row
## @param column List with the values to add. Must be of the same size of rows
def lol_add_column(rows, index, column):
    if len(rows)!=len(column):
        raise exceptions.LolException(_("I can't add a column with different size of lol"))
    r_rows=[]
    for i, row in enumerate(rows):
        r_rows.append(row[0:index] + [column[i],] + row[index:len(row)])
    return r_rows

## Returns a list with object in positions removed
def list_remove_positions(l, listindex):
    if l is None:
        raise exceptions.LolException(_("I can't remove positions from a None list"))
    r=[]
    for i, o in enumerate(l):
        if i not in listindex:
            r.append(o)
    return r

## lol is a list of list. Naned List Of Rows, used in myqtablewidget
## @param listindex is a list of column indexes to remove
def lol_remove_columns(rows, listindex):
    r_rows=[]
    for i, row in enumerate(rows):
        r_rows.append(list_remove_positions(row,listindex))
    return r_rows

## lol is a list of list. Naned List Of Rows, used in myqtablewidget
## @param listindex is a list of column indexes to remove
def lol_remove_rows(rows, listindex):
    return list_remove_positions(rows, listindex) #It's a list but of row

## Return a lol transposed. Changed rows by columns
def lol_transposed(lol):
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

## Extract a column from the list of row
def lol_get_row(lol, row):
    return lol[row]

## Extract a column from the list of row
def lol_get_column(lol, column):
    r=[]
    for row in lol:
        r.append(row[column])
    return r

## Return sum of values of a column from and index to and other index position. This method ignores None values
## This method can sum several objects
## @param row
## @param from_index
## @param to_index
## @param zerovalue 0 or Money(self.mem, 0, self.mem.localcurrency)....
def lol_sum_row(row, from_index, to_index, zerovalue=0):
    s=zerovalue
    for i, column in enumerate(row):
        if i>=from_index and i<=to_index:
            if column is not None:
                s=s + column
    return s

## Return sum of values of a column from and index to and other index position. This method ignores None values
## This method can sum several objects
## @zerovalue 0 or Money(self.mem, 0, self.mem.localcurrency)....
def lol_sum_column(lol, column, from_index, to_index, zerovalue=0):
    s=zerovalue
    for i, row in enumerate(lol):
        if i>=from_index and i<=to_index:
            if row[column] is not None:
                s=s + row[column]
    return s

def lol_print(lod, number=None):
    """
    Function Prints a list of list with tabulate module.

    @param lol
    @type List of lists
    @param number Number of lists to print. If None prints all lod. (defaults to None)
    @type Integer
    """
    number=len(lod) if number is None else number

    if len(lod)==0:
        print(_("lol_print: This list of lists hasn't data to print"))
        return
    if number==0:
        print(_("lol_print: No data was printed due to you selected 0 rows"))
        return
    print(tabulate(lod[0:number], tablefmt="psql"))