from decimal import Decimal
from pydicts.percentage import Percentage, percentage_between
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
    assert Percentage(1, 2)*Percentage(None,2 )==Percentage(None)
    with raises(TypeError):
        2*Percentage(1,2 )
    
def test_percentage_truediv():
    assert Percentage(1, 2)/Percentage(1,2 )==Percentage(1, 1)
    assert Percentage(1, 2)/Percentage(None,2 )==Percentage(None)
    
    
def test_percentage_value_100():
    assert Percentage(1, 2).value_100()==Decimal(50)
    assert Percentage(None).value_100()==None
    
def test_percentage_float_100():
    assert Percentage(1, 2).float_100()==50
    assert Percentage(None).float_100()==None
    
def test_percentage_float():
    assert Percentage(1, 2).float()==0.5
    assert Percentage(None).float()==None
    
def test_percentage_lt():
    assert not Percentage(1, 2)<Percentage(1, 4)
    assert Percentage(1, 4)<Percentage(1, 2)
    assert not Percentage(None)<Percentage(1, 2)
    assert not Percentage(1, 2)<Percentage(None)

def test_percentage_isGETZero():
    assert Percentage(1, 2).isGETZero()==True
    assert Percentage(-1, 2).isGETZero()==False
    assert Percentage(None).isGETZero()==False

def test_percentage_isLETZero():
    assert Percentage(1, 2).isLETZero()==False
    assert Percentage(-1, 2).isLETZero()==True
    assert Percentage(None).isLETZero()==False
    
def test_percentage_isGTZero():
    assert Percentage(1, 2).isGTZero()==True
    assert Percentage(-1, 2).isGTZero()==False
    assert Percentage(None).isGTZero()==False

def test_percentage_isLTZero():
    assert Percentage(1, 2).isLTZero()==False
    assert Percentage(-1, 2).isLTZero()==True
    assert Percentage(None).isLTZero()==False

def test_percentage_between():
    assert percentage_between(1, 2)==Percentage(1,1 )
    assert percentage_between(None,1 )==Percentage(None )
    
