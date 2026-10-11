from pydicts import lol, exceptions
from pytest import raises,  fixture

@fixture(autouse=True)
def reload_lol_():
    global lol_
    lol_=[]
    for i in range(10):
        lol_.append([1*i,2*i,3*i])

def test_lol_add_column():
    """
    Tests the lol_add_column function to add a new column to a list of lists.
    """
    new_lol=lol.lol_add_column(lol_, 2,  [1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
    assert len(lol_[0])+1==len(new_lol[0])
    with raises(exceptions.LolException):
        lol.lol_add_column(lol_, 2,  [1, ]) #Different size

def test_lol_order_by():
    """
    Tests the lol_order_by function to sort a list of lists by a specific column.
    """
    new_lol=lol.lol_add_row(lol_, 2,  [None]*3)
    new_lol=lol.lol_order_by(new_lol, 2)
    assert new_lol[0][0]==None
    new_lol=lol.lol_order_by(new_lol, 2, reverse=True, none_at_top=False)
    assert new_lol[0][0]==9

def test_lol_remove_columns():
    """
    Tests the lol_remove_columns function to remove specified columns from a list of lists.
    """
    new_lol=lol.lol_remove_columns(lol_, [2])
    assert len(lol_[0])-1==len(new_lol[0])

def test_lol_print():
    lol.lol_print(lol_)
    lol.lol_print(lol_,0)
    lol.lol_print(lol_,-1)
    """
    Tests the lol_print function to ensure it runs without errors for various inputs.
    """
    
def test_lol_transposed():
    transposed=lol.lol_transposed(lol_)
    assert transposed[0]==[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    Tests the lol_transposed function to transpose a list of lists.
    """

    transposed=lol.lol_transposed([])
    assert transposed==[]

    with raises(exceptions.LolException):
        lol.lol_transposed(None)

def test_lol_add_row_exception():
    """
    Tests that lol_add_row raises LolException when inserting a row with different column length.
    """
    with raises(exceptions.LolException):
        lol.lol_add_row([[1, 2]], 0, [1, 2, 3])

def test_list_remove_positions():
    """
    Tests list_remove_positions for removing items by index and raising LolException when list is None.
    """
    assert lol.list_remove_positions([10, 20, 30], [1]) == [10, 30]
    with raises(exceptions.LolException):
        lol.list_remove_positions(None, [0])

def test_lol_print_align():
    """
    Tests the lol_print function with alignment, maxcolwidths and tablefmt options.
    """
    lol.lol_print(lol_, align=["left","center","right"])
    lol.lol_print(lol_, maxcolwidths=[10, 10, 10])
    lol.lol_print(lol_, tablefmt="grid")
    lol.lol_print(lol_, stretch=False)
    lol.lol_print(lol_, wordwrap=False, stretch=False)
    s = lol.lol_string(lol_, stretch=False)
    assert isinstance(s, str)
    s_raw = lol.lol_string(lol_, wordwrap=False, stretch=False)
    assert isinstance(s_raw, str)
    assert "hasn't data" in lol.lol_string([])
    assert "No data was printed" in lol.lol_string(lol_, number=0)
    s_stretched = lol.lol_string(lol_, stretch=True)
    assert isinstance(s_stretched, str)