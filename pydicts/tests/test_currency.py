from pydicts.currency import Currency, currencies_list
from decimal import Decimal
from pydicts import lod, exceptions
from pytest import raises
def test_currency():
    """
    Tests the initialization of the Currency class with None amount.
    """
    assert Currency(None).amount== 0

def test_currency_currencies_dictionary():
    """
    Tests if the currencies_list function returns a valid list of currencies.
    """
    lod.lod_print(currencies_list())
#    assert False
    
    
def test_currency_init():
    assert Currency().string()=="0.00 €"
    
def test_currency_add():
    """
    Tests the addition of Currency objects.
    """
def test_currency_add():
    a=Currency(12.12, "EUR")
    b=Currency(0.88, "USD")
    assert a+a==Currency(24.24, "EUR")
    # Test adding currencies of different types should raise an exception
    with raises(exceptions.CurrencyOperationsException):
        a+b
            
def test_currency_eq():
    a=Currency(12.12, "EUR")
    b=Currency(0.88, "USD")
    """
    Tests the equality comparison of Currency objects.
    """
    assert not a==b
    
        
def test_currency_sub():
    """
    Tests the subtraction of Currency objects.
    """
    a=Currency(12.12, "EUR")
    b=Currency(0.88, "USD")
    assert a-a==Currency(0, "EUR")
    with raises(exceptions.CurrencyOperationsException):
        a-b        
        
def test_currency_mul():
    """
    Tests the multiplication of Currency objects by other Currency objects or scalars.
    """
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
    """
    Tests the less than (<) comparison of Currency objects.
    """
    a=Currency(12.12, "EUR")
    b=Currency(0.88, "USD")
    with raises(exceptions.CurrencyOperationsException):
        a<b
    assert not a<a
    assert a< a+a
    
def test_currency_lte():
    """
    Tests the less than or equal to (<=) comparison of Currency objects.
    """
    a=Currency(12.12, "EUR")
    b=Currency(0.88, "USD")
    with raises(exceptions.CurrencyOperationsException):
        a<=b
    assert a<=a
    assert a<= a+a

def test_currency_gt():
    """
    Tests the greater than (>) comparison of Currency objects.
    """
    a=Currency(12.12, "EUR")
    b=Currency(0.88, "USD")
    with raises(exceptions.CurrencyOperationsException):
        a>b
    assert not a>a
    assert a+a> a
    
def test_currency_gte():
    """
    Tests the greater than or equal to (>=) comparison of Currency objects.
    """
    a=Currency(12.12, "EUR")
    b=Currency(0.88, "USD")
    with raises(exceptions.CurrencyOperationsException):
        a>=b
    assert a>=a

def test_currency_truediv():
    """
    Tests the true division (/) of Currency objects.
    """
    a = Currency(Decimal("10.00"), "EUR")
    b = Currency(Decimal("2.00"), "EUR")
    c = Currency(Decimal("3.00"), "USD")

    # Test division with another Currency of the same type
    assert (a / b) == Currency(Decimal("5.00"), "EUR")

    # Test division with different currency (should raise exception)
    with raises(exceptions.CurrencyOperationsException):
        a / c

def test_currency_isZero():
    """
    Tests the isZero method of the Currency class.
    """
    assert Currency(0, "EUR").isZero() is True
    assert Currency(10, "EUR").isZero() is False
    assert Currency(-5, "EUR").isZero() is False

def test_currency_isGETZero():
    assert Currency(10, "EUR").isGETZero() is True
    assert Currency(0, "EUR").isGETZero() is True
    """
    Tests the isGETZero method of the Currency class.
    """
    assert Currency(-5, "EUR").isGETZero() is False

def test_currency_isGTZero():
    assert Currency(10, "EUR").isGTZero() is True
    assert Currency(0, "EUR").isGTZero() is False
    assert Currency(-5, "EUR").isGTZero() is False

def test_currency_isGTZero():
    """Tests the isGTZero method of the Currency class."""

def test_currency_isLTZero():
    assert Currency(-10, "EUR").isLTZero() is True
    assert Currency(0, "EUR").isLTZero() is False
    assert Currency(5, "EUR").isLTZero() is False

def test_currency_isLETZero():
    assert Currency(-10, "EUR").isLETZero() is True
    """Tests the isLETZero method of the Currency class."""
    assert Currency(0, "EUR").isLETZero() is True
    assert Currency(5, "EUR").isLETZero() is False

def test_currency_round():
    """Tests the round method of the Currency class."""
    a = Currency(Decimal("12.12345"), "EUR")
    assert a.round(2) == Decimal("12.12")
    assert a.round(3) == Decimal("12.123")
    assert a.round(0) == Decimal("12")
    assert Currency(Decimal("12.999"), "EUR").round(2) == Decimal("13.00")
    assert a+a>= a
