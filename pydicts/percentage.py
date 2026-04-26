from decimal import Decimal

class Percentage:
    """
    A class to manage percentage values, providing arithmetic operations and formatting.
    It stores the percentage as a Decimal value (e.g., 0.5 for 50%).
    """
    def __init__(self, numerator=None, denominator=None):
        """
        Initializes a Percentage object.

        Args:
            numerator (int, float, Decimal, optional): The numerator of the fraction.
            denominator (int, float, Decimal, optional): The denominator of the fraction.
                                                         If denominator is 0 or None, the value will be None.
        """
        self.setValue(numerator, denominator)

    def __repr__(self):
        """
        Returns the string representation of the percentage (e.g., "50.00 %").
        """
        return self.string()

    def __neg__(self):
        """
        Returns a new Percentage object with the negated value.
        """
        if self.value is None:
            return Percentage(None)
        return Percentage(-self.value, 1)

    def __lt__(self, other):
        if self.value is None or other.value is None:
            return False
        """
        Compares if this Percentage object is less than another.
        Returns False if either value is None.

        Args: other (Percentage): The other Percentage object to compare with.
        """
        
        
        if self.value<other.value:
            return True
        return False

    def __eq__(self, b):
        """
        Compares two Percentage objects for equality.

        Args: b (Percentage): The other Percentage object to compare with.
        """
        return self.value==b.value

    def __add__(self,p):
        """
        Adds two Percentage objects.
        Returns None if either value is None.

        Args: p (Percentage): The other Percentage object to add.
        """
        if self.value is None or p.value is None:
            return None
        
        return self.__class__(self.value+p.value,1)

    def __sub__(self, p):
        """
        Subtracts another Percentage object from this one.
        Returns None if either value is None.

        Args: p (Percentage): The other Percentage object to subtract.
        """
        if self.value is None or p.value is None:
            return None
        
        return self.__class__(self.value-p.value,1)

    def __mul__(self, value):
        """
        Multiplies this Percentage object by another Percentage object.
        Returns None if either value is None.

        Args: value (Percentage): The other Percentage object to multiply by.
        """
        try:
            if value.__class__==Percentage:
                return Percentage(self.value*value.value, 1)
        except:
            return Percentage(None)

    def __truediv__(self, other):
        """
        Divides this Percentage object by another Percentage object.
        Returns None if division by zero or other error occurs.

        Args: other (Percentage): The other Percentage object to divide by.
        """
        try:
            r=self.value/other.value
        except:
            r=None
        return Percentage(r, 1)

    def setValue(self, numerator,  denominator):
        """
        Sets the internal value of the percentage based on a numerator and denominator.
        If denominator is 0 or None, the value is set to None.

        Args:
            numerator (int, float, Decimal): The numerator.
            denominator (int, float, Decimal): The denominator.
        """
        try:
            self.value=Decimal(numerator)/Decimal(denominator)
        except:
            self.value=None

    def value_100(self):
        """
        Returns the percentage value multiplied by 100 (e.g., 50 for 0.5).
        Returns None if the internal value is None.
        """
        if self.value==None:
            return None
        else:
            return self.value*Decimal(100)

    def float_100(self):
        """
        Returns the percentage value multiplied by 100 as a float.
        Returns None if the internal value is None.
        """
        if self.value is None:
            return None
        return float(self.value_100())

    def float(self):
        """
        Returns the percentage value as a float (e.g., 0.5 for 50%).
        Returns None if the internal value is None.
        """
        if self.value is None:
            return None
        return float(self.value)

    def string(self, decimals=2):
        """
        Returns the formatted string representation of the percentage (e.g., "50.00 %").
        Returns "None %" if the internal value is None.

        Args:
            decimals (int, optional): The number of decimal places to round to. Defaults to 2.
        """
        if self.value is None:
            return "None %"
        return "{} %".format(round(self.value_100(), decimals))

    def isValid(self):
        """
        Checks if the percentage has a valid (non-None) value.
        """
        if self.value!=None:
            return True
        return False

    def isGETZero(self):
        """
        Checks if the percentage value is greater than or equal to zero.
        Returns False if the value is not valid.
        """
        if self.isValid() and self.value>=0:
            return True
        return False

    def isGTZero(self):
        """
        Checks if the percentage value is strictly greater than zero.
        Returns False if the value is not valid.
        """
        if self.isValid() and self.value>0:
            return True
        return False

    def isLTZero(self):
        """
        Checks if the percentage value is strictly less than zero.
        Returns False if the value is not valid.
        """
        if self.isValid() and self.value<0:
            return True
        return False
        
    def isLETZero(self):
        """
        Checks if the percentage value is less than or equal to zero.
        Returns False if the value is not valid.
        """
        if self.isValid() and self.value<=0:
            return True
        return False

def percentage_between(a,b):
    """
    Calculates the percentage change from value `a` to value `b`.

    Args:
        a (int, float, Decimal): The starting value.
        b (int, float, Decimal): The ending value.

    Returns:
        Percentage: A Percentage object representing the change.
                    Returns Percentage(None) if calculation is not possible (e.g., a is zero).
    """
    try:
        return Percentage(b-a,a)
    except:
        return Percentage()
