from pydicts.currency import Currency, currencies_odod
def test_currency():
    assert Currency(None).amount== 0

def test_currency_currencies_dictionary():
    print(currencies_odod())
    assert False
