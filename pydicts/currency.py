from decimal import Decimal
from pydicts import lod, exceptions
from importlib.resources import files



def currencies_list():
    with open(files("pydicts") / 'currencies.json') as f:
        lod_=eval(f.read())
    return lod_

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

    def __add__(self, other):
        """Si las divisas son distintas, queda el resultado con la divisa del primero"""
        if self.currency==other.currency:
            return Currency(self.amount+other.amount, self.currency)
        else:
            raise exceptions.CurrencyOperationsException("Before adding, please convert to the same currency")

    def __sub__(self, other):
        """Si las divisas son distintas, queda el resultado con la divisa del primero"""
        if self.currency==other.currency:
            return Currency(self.amount-other.amount, self.currency)
        else:
            raise exceptions.CurrencyOperationsException("Before substracting, please convert to the same currency")

    def __lt__(self, other):
        if self.currency==other.currency:
            if self.amount < other.amount:
                return True
            return False
        else:
            raise exceptions.CurrencyOperationsException("Before lt ordering, please convert to the same currency")
    
    def __le__(self, other):
        if self.currency==other.currency:
            if self.amount <= other.amount:
                return True
            return False
        else:
            raise exceptions.CurrencyOperationsException("Before lt ordering, please convert to the same currency")
            
    def __gt__(self, other):
        if self.currency==other.currency:
            if self.amount > other.amount:
                return True
            return False
        else:
            raise exceptions.CurrencyOperationsException("Before lt ordering, please convert to the same currency")
            
    def __ge__(self, other):
        if self.currency==other.currency:
            if self.amount >= other.amount:
                return True
            return False
        else:
            raise exceptions.CurrencyOperationsException("Before lt ordering, please convert to the same currency")

    ## Si las divisas son distintas, queda el resultado con la divisa del primero
    ##
    ## En caso de querer multiplicar por un numero debe ser despues. For example: other*4
    def __mul__(self, other):
        if other.__class__.__name__ in ("int",  "float", "Decimal"):
            return Currency(self.amount*other, self.currency)

        if self.currency==other.currency:
            print(self.amount, other.amount, self.amount*other.amount)
            return Currency(self.amount*other.amount, self.currency)
        else:
            raise exceptions.CurrencyOperationsException("Before multiplying, please convert to the same currency")

    def __truediv__(self, other):
        """Si las divisas son distintas, queda el resultado con la divisa del primero"""
        if self.currency==other.currency:
            return Currency(self.amount/other.amount, self.currency)
        else:
            raise exceptions.CurrencyOperationsException("Before true dividing, please convert to the same currency")

    def __repr__(self):
        return self.string(2)

    ## Returs a typical currency string
    ## @param digits int that defines the number of decimals. 2 by default
    ## @return string
    def string(self,   decimals=2):
        return "{} {}".format(round(self.amount, decimals), currencies[self.currency]["symbol"])

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
        """Devuelve otro other con el amount con signo cambiado"""
        return Currency(-self.amount, self.currency)

    def round(self, decimals=2):
        return round(self.amount, decimals)





