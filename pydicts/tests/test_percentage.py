from decimal import Decimal
from pydicts.percentage import Percentage, percentage_between
from pytest import raises

def test_percentage_init():
    """
    Tests initialization of Percentage with None, valid numerator/denominator,
    and zero denominator (which sets value to None).
    """
    assert Percentage(None).value== None
    assert Percentage(12, 1).value == 12
    assert Percentage(12, 0).value== None

def test_percentage_add():
    """
    Tests addition of Percentage objects and None-handling.
    """
    a=Percentage(1, 2)
    b=Percentage(1, 4)
    assert a+b==Percentage(3, 4)
    assert not a+b==Percentage(None)
    assert Percentage(None)+Percentage(None)==None
    
def test_percentage_sub():
    """
    Tests subtraction of Percentage objects and None-handling.
    """
    a=Percentage(1, 2)
    b=Percentage(1, 4)
    assert a-b==Percentage(1, 4)
    assert not a+b==Percentage(None)
    assert Percentage(None)-Percentage(None)==None
    
def test_percentage_neg():
    """
    Tests unary negation (__neg__) on Percentage objects.
    """
    a=Percentage(1, 2)
    assert -(-a)==a
    assert -Percentage(None)==Percentage(None)
    
def test_percentage_repr():
    """
    Tests formatted string representation (__repr__) for Percentage instances.
    """
    assert repr(Percentage(1, 2))=="50.00 %"
    assert repr(Percentage(None))=="None %"
    
def test_percentage_mult():
    """
    Tests multiplication of Percentage objects and verifies scalar on left raises TypeError.
    """
    assert Percentage(1, 2)*Percentage(1,2 )==Percentage(1, 4)
    assert Percentage(1, 2)*Percentage(None,2 )==Percentage(None)
    with raises(TypeError):
        2*Percentage(1,2 )
    
def test_percentage_truediv():
    """
    Tests true division (/) between Percentage objects.
    """
    assert Percentage(1, 2)/Percentage(1,2 )==Percentage(1, 1)
    assert Percentage(1, 2)/Percentage(None,2 )==Percentage(None)
    
    
def test_percentage_value_100():
    """
    Tests value_100() method returning the percentage scaled to [0, 100] as a Decimal.
    """
    assert Percentage(1, 2).value_100()==Decimal(50)
    assert Percentage(None).value_100()==None
    
def test_percentage_float_100():
    """
    Tests float_100() method returning the percentage scaled to [0, 100] as a float.
    """
    assert Percentage(1, 2).float_100()==50
    assert Percentage(None).float_100()==None
    
def test_percentage_float():
    """
    Tests float() conversion returning raw ratio as a float.
    """
    assert Percentage(1, 2).float()==0.5
    assert Percentage(None).float()==None
    
def test_percentage_lt():
    """
    Tests strict less-than (<) ordering between Percentage instances.
    """
    assert not Percentage(1, 2)<Percentage(1, 4)
    assert Percentage(1, 4)<Percentage(1, 2)
    assert not Percentage(None)<Percentage(1, 2)
    assert not Percentage(1, 2)<Percentage(None)

def test_percentage_isGETZero():
    """
    Tests isGETZero() (greater than or equal to zero).
    """
    assert Percentage(1, 2).isGETZero()==True
    assert Percentage(-1, 2).isGETZero()==False
    assert Percentage(None).isGETZero()==False

def test_percentage_isLETZero():
    """
    Tests isLETZero() (less than or equal to zero).
    """
    assert Percentage(1, 2).isLETZero()==False
    assert Percentage(-1, 2).isLETZero()==True
    assert Percentage(None).isLETZero()==False
    
def test_percentage_isGTZero():
    """
    Tests isGTZero() (strictly greater than zero).
    """
    assert Percentage(1, 2).isGTZero()==True
    assert Percentage(-1, 2).isGTZero()==False
    assert Percentage(None).isGTZero()==False

def test_percentage_isLTZero():
    """
    Tests isLTZero() (strictly less than zero).
    """
    assert Percentage(1, 2).isLTZero()==False
    assert Percentage(-1, 2).isLTZero()==True
    assert Percentage(None).isLTZero()==False

def test_percentage_between():
    """
    Tests percentage_between helper function calculating ratio between two values.
    """
    assert percentage_between(1, 2)==Percentage(1,1 )
    assert percentage_between(None,1 )==Percentage(None )
    
