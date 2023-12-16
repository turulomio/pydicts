from pydicts.percentage import Percentage
from pytest import raises

def test_percentage_init():
    assert Percentage(None).value== None
    assert Percentage(12, 1).value == 12
    assert Percentage(12, 0).value== None

def test_percentage_add():
    a=Percentage(1, 2)
    b=Percentage(1, 4)
    assert a+b==Percentage(3, 4)
    assert not a+b==Percentage(None)
    assert Percentage(None)+Percentage(None)==None
    
def test_percentage_sub():
    a=Percentage(1, 2)
    b=Percentage(1, 4)
    assert a-b==Percentage(1, 4)
    assert not a+b==Percentage(None)
    assert Percentage(None)-Percentage(None)==None
    
def test_percentage_neg():
    a=Percentage(1, 2)
    assert -(-a)==a
    assert -Percentage(None)==Percentage(None)
    
def test_percentage_repr():
    assert repr(Percentage(1, 2))=="50.00 %"
    assert repr(Percentage(None))=="None %"
    
def test_percentage_mult():
    assert Percentage(1, 2)*Percentage(1,2 )==Percentage(1, 4)
    with raises(TypeError):
        2*Percentage(1,2 )
    
def test_percentage_truediv():
    assert Percentage(1, 2)/Percentage(1,2 )==Percentage(1, 1)
    with raises(TypeError):
        2/Percentage(1,2 )
    
def test_percentage_lt():
    assert not Percentage(1, 2)<Percentage(1, 4)
    assert Percentage(1, 4)<Percentage(1, 2)
    assert not Percentage(None)<Percentage(1, 2)
    assert not Percentage(1, 2)<Percentage(None)
