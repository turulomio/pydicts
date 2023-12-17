from decimal import Decimal
from ccy import dump_currency_table
from html import unescape
from pydicts import lod, exceptions



def currencies_list():
    lod_=[]
    for code_, name, iso, symbol, country, order, rounding in dump_currency_table()[1:]:
        lod_.append({
            "code":code_, 
            "name":name, 
            "iso":iso, 
            "symbol_html":symbol, 
            "symbol": unescape(symbol), 
            "country":country, 
            
            "order":order, 
            "rounding":rounding
        })
    lod_.append({
        "code":"u", 
        "name": "Unit", 
        "iso":"", 
        "symbol_html":"u", 
        "symbol": "u", 
        "country":"WW", 
        "order": 0, 
        "rounding":6, 
    })
    return lod.lod_order_by(lod_,"code")

def currencies_odod():
    return lod.lod2odod(currencies_list(), "code")
    
currencies=currencies_odod()

## Class to manage currencies in officegenerator
##
## The symbol is defined by code with self.symbol()
class Currency:
    def __init__(self, amount=None,  currency="EUR") :
        if amount==None:
            self.amount=Decimal(0)
        else:
            self.amount=Decimal(str(amount))
        self.currency=currency

    def __eq__(self, other):
        if self.amount==other.amount and self.currency==other.currency:
            return True
        return False

    def __add__(self, money):
        """Si las divisas son distintas, queda el resultado con la divisa del primero"""
        if self.currency==money.currency:
            return self.__class__(self.amount+money.amount, self.currency)
        else:
            raise exceptions.CurrencyOperationsException("Before adding, please convert to the same currency")

    def __sub__(self, money):
        """Si las divisas son distintas, queda el resultado con la divisa del primero"""
        if self.currency==money.currency:
            return self.__class__(self.amount-money.amount, self.currency)
        else:
            raise exceptions.CurrencyOperationsException("Before substracting, please convert to the same currency")

    def __lt__(self, money):
        if self.currency==money.currency:
            if self.amount < money.amount:
                return True
            return False
        else:
            raise exceptions.CurrencyOperationsException("Before lt ordering, please convert to the same currency")

    ## Si las divisas son distintas, queda el resultado con la divisa del primero
    ##
    ## En caso de querer multiplicar por un numero debe ser despues. For example: money*4
    def __mul__(self, money):
        if money.__class__.__name__ in ("int",  "float", "Decimal"):
            return self.__class__(self.amount*money, self.currency)
        if self.currency==money.currency:
            return self.__class__(self.amount*money.amount, self.currency)
        else:
            raise exceptions.CurrencyOperationsException("Before multiplying, please convert to the same currency")

    def __truediv__(self, money):
        """Si las divisas son distintas, queda el resultado con la divisa del primero"""
        if self.currency==money.currency:
            return self.__class__(self.amount/money.amount, self.currency)
        else:
            raise exceptions.CurrencyOperationsException("Before true dividing, please convert to the same currency")

    def __repr__(self):
        return self.string(2)

    ## Returs a typical currency string
    ## @param digits int that defines the number of decimals. 2 by default
    ## @return string
    def string(self,   digits=2):
        return "{} {}".format(round(self.amount, digits), currencies[self.currency]["symbol"])

    def isZero(self):
        if self.amount==Decimal(0):
            return True
        else:
            return False

    def isGETZero(self):
        if self.amount>=Decimal(0):
            return True
        else:
            return False

    def isGTZero(self):
        if self.amount>Decimal(0):
            return True
        else:
            return False

    def isLTZero(self):
        if self.amount<Decimal(0):
            return True
        else:
            return False

    def isLETZero(self):
        if self.amount<=Decimal(0):
            return True
        else:
            return False

    def __neg__(self):
        """Devuelve otro money con el amount con signo cambiado"""
        return self.__class__(-self.amount, self.currency)

    def round(self, digits=2):
        return round(self.amount, digits)





