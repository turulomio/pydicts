from pydicts.currency import Currency, currencies_list
from decimal import Decimal
from pydicts import lod, exceptions
from pytest import raises
def test_currency():
    assert Currency(None).amount== 0

def test_currency_currencies_dictionary():
    lod.lod_print(currencies_list())
#    assert False
    
    
def test_currency_init():
    assert Currency().string()=="0.00 €"
    
def test_currency_add():
    a=Currency(12.12, "EUR")
    b=Currency(0.88, "USD")
    assert a+a==Currency(24.24, "EUR")
    with raises(exceptions.CurrencyOperationsException):
        a+b
            
def test_currency_eq():
    a=Currency(12.12, "EUR")
    b=Currency(0.88, "USD")
    assert not a==b
    
        
def test_currency_sub():
    a=Currency(12.12, "EUR")
    b=Currency(0.88, "USD")
    assert a-a==Currency(0, "EUR")
    with raises(exceptions.CurrencyOperationsException):
        a-b        
        
def test_currency_mul():
    a=Currency(12.12, "EUR")
    b=Currency(0.88, "USD")
    # Test multiplication with another Currency of the same type
    assert (a * a) == Currency(Decimal("12.12") * Decimal("12.12"), "EUR")
    assert (a * a) == Currency(Decimal("146.8944"), "EUR")
    # Test multiplication with a scalar (int, float, Decimal)
    assert (a * 2) == Currency(Decimal("24.24"), "EUR")
    assert (a * 0.5) == Currency(Decimal("6.06"), "EUR")
    assert (a * Decimal("3")) == Currency(Decimal("36.36"), "EUR")
    with raises(exceptions.CurrencyOperationsException):
        a*b
    with raises(TypeError):
        2*a
    
    a*2==Currency(24.24, "EUR")


def test_currency_lt():
    a=Currency(12.12, "EUR")
    b=Currency(0.88, "USD")
    with raises(exceptions.CurrencyOperationsException):
        a<b
    assert not a<a
    assert a< a+a
    
def test_currency_lte():
    a=Currency(12.12, "EUR")
    b=Currency(0.88, "USD")
    with raises(exceptions.CurrencyOperationsException):
        a<=b
    assert a<=a
    assert a<= a+a

def test_currency_gt():
    a=Currency(12.12, "EUR")
    b=Currency(0.88, "USD")
    with raises(exceptions.CurrencyOperationsException):
        a>b
    assert not a>a
    assert a+a> a
    
def test_currency_gte():
    a=Currency(12.12, "EUR")
    b=Currency(0.88, "USD")
    with raises(exceptions.CurrencyOperationsException):
        a>=b
    assert a>=a

def test_currency_truediv():
    a = Currency(Decimal("10.00"), "EUR")
    b = Currency(Decimal("2.00"), "EUR")
    c = Currency(Decimal("3.00"), "USD")

    # Test division with another Currency of the same type
    assert (a / b) == Currency(Decimal("5.00"), "EUR")

    # Test division with different currency (should raise exception)
    with raises(exceptions.CurrencyOperationsException):
        a / c

def test_currency_isZero():
    assert Currency(0, "EUR").isZero() is True
    assert Currency(10, "EUR").isZero() is False
    assert Currency(-5, "EUR").isZero() is False

def test_currency_isGETZero():
    assert Currency(10, "EUR").isGETZero() is True
    assert Currency(0, "EUR").isGETZero() is True
    assert Currency(-5, "EUR").isGETZero() is False

def test_currency_isGTZero():
    assert Currency(10, "EUR").isGTZero() is True
    assert Currency(0, "EUR").isGTZero() is False
    assert Currency(-5, "EUR").isGTZero() is False

def test_currency_isLTZero():
    assert Currency(-10, "EUR").isLTZero() is True
    assert Currency(0, "EUR").isLTZero() is False
    assert Currency(5, "EUR").isLTZero() is False

def test_currency_isLETZero():
    assert Currency(-10, "EUR").isLETZero() is True
    assert Currency(0, "EUR").isLETZero() is True
    assert Currency(5, "EUR").isLETZero() is False

def test_currency_round():
    a = Currency(Decimal("12.12345"), "EUR")
    assert a.round(2) == Decimal("12.12")
    assert a.round(3) == Decimal("12.123")
    assert a.round(0) == Decimal("12")
    assert Currency(Decimal("12.999"), "EUR").round(2) == Decimal("13.00")
    assert a+a>= a

def test_currency_truediv():
    a = Currency(Decimal("10.00"), "EUR")
    b = Currency(Decimal("2.00"), "EUR")
    c = Currency(Decimal("3.00"), "USD")

    # Test division with another Currency of the same type
    assert (a / b) == Currency(Decimal("5.00"), "EUR")

    # Test division with different currency (should raise exception)
    with raises(exceptions.CurrencyOperationsException):
        a / c

def test_currency_isZero():
    assert Currency(0, "EUR").isZero() is True
    assert Currency(10, "EUR").isZero() is False
    assert Currency(-5, "EUR").isZero() is False

def test_currency_isGETZero():
    assert Currency(10, "EUR").isGETZero() is True
    assert Currency(0, "EUR").isGETZero() is True
    assert Currency(-5, "EUR").isGETZero() is False

def test_currency_isGTZero():
    assert Currency(10, "EUR").isGTZero() is True
    assert Currency(0, "EUR").isGTZero() is False
    assert Currency(-5, "EUR").isGTZero() is False

def test_currency_isLTZero():
    assert Currency(-10, "EUR").isLTZero() is True
    assert Currency(0, "EUR").isLTZero() is False
    assert Currency(5, "EUR").isLTZero() is False

def test_currency_isLETZero():
    assert Currency(-10, "EUR").isLETZero() is True
    assert Currency(0, "EUR").isLETZero() is True
    assert Currency(5, "EUR").isLETZero() is False

def test_currency_round():
    a = Currency(Decimal("12.12345"), "EUR")
    assert a.round(2) == Decimal("12.12")
    assert a.round(3) == Decimal("12.123")
    assert a.round(0) == Decimal("12")
    assert Currency(Decimal("12.999"), "EUR").round(2) == Decimal("13.00")
    assert a+a>= a
