from pydicts.currency import Currency, currencies_list
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
    assert (a*a)==Currency( 146.8944, "EUR")
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
    assert a+a>= a
