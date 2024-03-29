from pydicts import lol, exceptions
from pytest import raises,  fixture

@fixture(autouse=True)
def reload_lol_():
    global lol_
    lol_=[]
    for i in range(10):
        lol_.append([1*i,2*i,3*i])

def test_lol_add_column():
    new_lol=lol.lol_add_column(lol_, 2,  [1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
    assert len(lol_[0])+1==len(new_lol[0])
    with raises(exceptions.LolException):
        lol.lol_add_column(lol_, 2,  [1, ]) #Different size

def test_lol_order_by():
    new_lol=lol.lol_add_row(lol_, 2,  [None]*3)
    new_lol=lol.lol_order_by(new_lol, 2)
    assert new_lol[0][0]==None
    new_lol=lol.lol_order_by(new_lol, 2, reverse=True, none_at_top=False)
    assert new_lol[0][0]==9

def test_lol_remove_columns():
    new_lol=lol.lol_remove_columns(lol_, [2])
    assert len(lol_[0])-1==len(new_lol[0])

def test_lol_print():
    lol.lol_print(lol_)
    lol.lol_print(lol_,0)
    lol.lol_print(lol_,-1)
    
def test_lol_transposed():
    transposed=lol.lol_transposed(lol_)
    assert transposed[0]==[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    transposed=lol.lol_transposed([])
    assert transposed==[]

    with raises(exceptions.LolException):
        lol.lol_transposed(None)

#
#    lor=[]
#    column_to_add=[]
#    for i in range(10):
#        lor.append([1*i,2*i,3*i])
#        column_to_add.append(-i)
#    print_lor(lor)
#
#    lor=lor_add_column(lor, 0, column_to_add)
#    lor=lor_add_column(lor, 2, column_to_add)
#    lor=lor_add_column(lor, 5, column_to_add)
#    print_lor(lor)
#
#    a=lor_remove_columns(lor,[2,3])
#    print_lor(a)
#    b=lor_remove_rows(a,[8,9])
#    print_lor(b)
#
#    c=lor_transposed(b)
#    print_lor(c)
#
#    d=Decimal("12.3")
#    json_d=var2json(d)
#    print (d, json_d, json_d.__class__)
#    d=None
#    json_d=var2json(d)
#    print (d, json_d, json_d.__class__)
#    d=True
#    json_d=var2json(d)
#    print (d, json_d, json_d.__class__)
