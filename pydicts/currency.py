from decimal import Decimal
from pydicts import lod, exceptions
from importlib.resources import files



def currencies_list():
    """
    Loads the list of currencies from the 'currencies.json' file.

    Returns:
        list: A list of dictionaries, each representing a currency.
    """
    with open(files("pydicts") / 'currencies.json') as f:
        lod_=eval(f.read())
    return lod_

def currencies_odod():
    """
    Converts the list of currencies into an OrderedDict of dictionaries, keyed by currency code.
    """
    return lod.lod2odod(currencies_list(), "code")
    
currencies = currencies_odod()

## Class to manage currencies in officegenerator
##
## The symbol is defined by code with self.symbol()
class Currency:
    def __init__(self, amount=None,  currency="EUR") :
        if amount==None:
            """
            Initializes a Currency object.

            Args:
                amount (float, int, Decimal, optional): The monetary amount. Defaults to None (which becomes Decimal(0)).
                currency (str, optional): The currency code (e.g., "EUR", "USD"). Defaults to "EUR".
            """
            self.amount=Decimal(0)
        else:
            self.amount=Decimal(str(amount))
        self.currency=currency

    def __eq__(self, other):
        """
        Compares two Currency objects for equality.
        They are equal if both amount and currency are the same.
        """
        if self.amount==other.amount and self.currency==other.currency:
            return True
        return False

    def __add__(self, other):
        """
        Adds two Currency objects.
        Raises CurrencyOperationsException if currencies are different.
        
        Args: other (Currency): The other Currency object to add.
        """
        # Original comment: "Si las divisas son distintas, queda el resultado con la divisa del primero"
        if self.currency==other.currency:
            return Currency(self.amount+other.amount, self.currency)
        else:
            raise exceptions.CurrencyOperationsException("Before adding, please convert to the same currency")

    def __sub__(self, other):
        """
        Subtracts one Currency object from another.
        Raises CurrencyOperationsException if currencies are different.
        
        Args: other (Currency): The other Currency object to subtract.
        """
        # Original comment: "Si las divisas son distintas, queda el resultado con la divisa del primero"
        if self.currency==other.currency:
            return Currency(self.amount-other.amount, self.currency)
        else:
            raise exceptions.CurrencyOperationsException("Before substracting, please convert to the same currency")

    def __lt__(self, other):
        """
        Compares if this Currency object is less than another.
        Raises CurrencyOperationsException if currencies are different.
        
        Args: other (Currency): The other Currency object to compare with.
        """
        if self.currency==other.currency:
            if self.amount < other.amount:
                return True
            return False
        else:
            raise exceptions.CurrencyOperationsException("Before lt ordering, please convert to the same currency")
    
    def __le__(self, other):
        """
        Compares if this Currency object is less than or equal to another.
        Raises CurrencyOperationsException if currencies are different.
        
        Args: other (Currency): The other Currency object to compare with.
        """
        if self.currency==other.currency:
            if self.amount <= other.amount:
                return True
            return False
        else:
            raise exceptions.CurrencyOperationsException("Before lt ordering, please convert to the same currency")
            
    def __gt__(self, other):
        """
        Compares if this Currency object is greater than another.
        Raises CurrencyOperationsException if currencies are different.
        
        Args: other (Currency): The other Currency object to compare with.
        """
        if self.currency==other.currency:
            if self.amount > other.amount:
                return True
            return False
        else:
            raise exceptions.CurrencyOperationsException("Before lt ordering, please convert to the same currency")
            
    def __ge__(self, other):
        """
        Compares if this Currency object is greater than or equal to another.
        Raises CurrencyOperationsException if currencies are different.
        
        Args: other (Currency): The other Currency object to compare with.
        """
        if self.currency==other.currency:
            if self.amount >= other.amount:
                return True
            return False
        else:
            raise exceptions.CurrencyOperationsException("Before lt ordering, please convert to the same currency")

    """
    Multiplies the Currency object by another Currency object (of the same type) or a scalar.
    Raises CurrencyOperationsException if currencies are different.
    Raises TypeError if multiplying by a scalar on the left side (e.g., 2 * Currency).
    
    Args: other (Currency or int or float or Decimal): The value to multiply by.
    """
    # Original comments:
    # ## Si las divisas son distintas, queda el resultado con la divisa del primero
    # ## En caso de querer multiplicar por un numero debe ser despues. For example: other*4
    def __mul__(self, other):
        if isinstance(other, (int, float, Decimal)):
            return Currency(self.amount * Decimal(str(other)), self.currency)
        if self.currency==other.currency:
            # Removed debug print statement
            return Currency(self.amount*other.amount, self.currency)
        else:
            raise exceptions.CurrencyOperationsException("Before multiplying, please convert to the same currency")

    def __truediv__(self, other):
        """
        Divides the Currency object by another Currency object of the same type.
        Raises CurrencyOperationsException if currencies are different.
        
        Args: other (Currency): The other Currency object to divide by.
        """
        """Si las divisas son distintas, queda el resultado con la divisa del primero"""
        if self.currency==other.currency:
            return Currency(self.amount/other.amount, self.currency)
        else:
            raise exceptions.CurrencyOperationsException("Before true dividing, please convert to the same currency")

    def __repr__(self):
        return self.string(2)
    
    def string(self,   decimals=2):
        """
        Returns a typical currency string representation (e.g., "12.34 €").

        Args:
            decimals (int, optional): The number of decimal places to round to. Defaults to 2.

        Returns:
            str: The formatted currency string.
        """
        return "{} {}".format(round(self.amount, decimals), currencies[self.currency]["symbol"])

    def isZero(self):
        """
        Checks if the currency amount is exactly zero.
        """
        if self.amount==Decimal(0):
            return True
        else:
            return False

    def isGETZero(self):
        """
        Checks if the currency amount is greater than or equal to zero.
        """
        if self.amount>=Decimal(0):
            return True
        else:
            return False

    def isGTZero(self):
        """
        Checks if the currency amount is strictly greater than zero.
        """
        if self.amount>Decimal(0):
            return True
        else:
            return False

    def isLTZero(self):
        """
        Checks if the currency amount is strictly less than zero.
        """
        if self.amount<Decimal(0):
            return True
        else:
            return False

    def isLETZero(self):
        """
        Checks if the currency amount is less than or equal to zero.
        """
        if self.amount<=Decimal(0):
            return True
        else:
            return False

    def __neg__(self):
        """
        Returns a new Currency object with the negated amount.
        """
        """Devuelve otro other con el amount con signo cambiado"""
        return Currency(-self.amount, self.currency)

    def round(self, decimals=2):
        """
        Rounds the currency amount to the specified number of decimals.

        Args:
            decimals (int, optional): The number of decimal places to round to. Defaults to 2.

        Returns:
            Decimal: The rounded amount.
        """
        return round(self.amount, decimals)
