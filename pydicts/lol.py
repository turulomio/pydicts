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

def lol_add_row(lol_, index, row):
    """
        Adds a row to a list of rows
        Checks if new row has the same size of the first row of the LOL
        Parameters:
            - lol_
            - index: int with the index of the position where we are going to insert row
            - row
        Returns
            LOL
            
        Will raise error:
            - lol.lol_add_row(lol_, 1, [2,3]) #New row size is different to first row
    """
    if len(lol_)>0 and len(lol_[0])!=len(row):
        raise exceptions.LolException(_("I can't add a row with different size of the first row of the lol"))
    lol_.insert(index, row)
    return lol_

## Returns a list with object in positions removed
def list_remove_positions(l, listindex):
    if l is None:
        raise exceptions.LolException(_("I can't remove positions from a None list"))
    r=[]
    for i, o in enumerate(l):
        if i not in listindex:
            r.append(o)
    return r

## Order data columns. 
def lol_order_by(lol_, index, reverse=False, none_at_top=True):
    """
        Orders a list of lists by a index
        Parameters:
            - lol
            - index
            - reverse
            - none_at_top: None values are set at the beginning
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


## lol is a list of list. Naned List Of Rows, used in myqtablewidget
## @param list_of_indexes is a list of column indexes to remove
def lol_remove_columns(rows, list_of_indexes):
    r_rows=[]
    for i, row in enumerate(rows):
        r_rows.append(list_remove_positions(row,list_of_indexes))
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
def lol_sum_row(row, from_index=0, to_index=None, zerovalue=0):
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

def lol_print(lol_, number=None, align=None):
    """
        Prints a list of list with tabulate module.
        
        Parameters:
            - lol_: List of list
            - number: Númber of lists to print. If None prints all lod. (defaults to None)
            - align: Cells alignment with tabultate sintaxis. (defaults to None). Possible column alignments
                     are: right, center, left, decimal (only for numbers), and None (to disable alignment). 
                     Omitting an alignment uses the default
    """
    number=len(lol_) if number is None else number

    if len(lol_)==0:
        print(_("lol_print: This list of lists hasn't data to print"))
        return
    if number==0:
        print(_("lol_print: No data was printed due to you selected 0 rows"))
        return
    print(tabulate(lol_[0:number], tablefmt="psql", colalign=align))
