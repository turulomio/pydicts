from decimal import Decimal

## Class to manage percentages in spreadsheets
## Converts values to decimal (Value is a decimal)
class Percentage:
    def __init__(self, numerator=None, denominator=None):
        
        self.setValue(numerator, denominator)

    def __repr__(self):
        return self.string()

    def __neg__(self):
        if self.value is None:
            return Percentage(None)
        return Percentage(-self.value, 1)

    def __lt__(self, other):
        if self.value is None or other.value is None:
            return False
        
        
        if self.value<other.value:
            return True
        return False

    def __eq__(self, b):
        
        return self.value==b.value

    def __add__(self,p):
        if self.value is None or p.value is None:
            return None
        
        return self.__class__(self.value+p.value,1)

    def __sub__(self, p):
        if self.value is None or p.value is None:
            return None
        
        return self.__class__(self.value-p.value,1)

    def __mul__(self, value):
        try:
            if value.__class__==Percentage:
                return Percentage(self.value*value.value, 1)
        except:
            return Percentage(None)

    def __truediv__(self, other):
        try:
            r=self.value/other.value
        except:
            r=None
        return Percentage(r, 1)

    def setValue(self, numerator,  denominator):
        try:
            self.value=Decimal(numerator)/Decimal(denominator)
        except:
            self.value=None

    def value_100(self):
        if self.value==None:
            return None
        else:
            return self.value*Decimal(100)

    ## @return percentage float value
    def float_100(self):
        if self.value is None:
            return None
        return float(self.value_100())

    ## @return percentage float value
    def float(self):
        if self.value is None:
            return None
        return float(self.value)

    def string(self, decimals=2):
        if self.value is None:
            return "None %"
        return "{} %".format(round(self.value_100(), decimals))

    ## Returns if the percentage is valid. I mean it's value different of None
    def isValid(self):
        if self.value!=None:
            return True
        return False

    def isGETZero(self):
        if self.isValid() and self.value>=0:
            return True
        return False

    def isGTZero(self):
        if self.isValid() and self.value>0:
            return True
        return False

    def isLTZero(self):
        if self.isValid() and self.value<0:
            return True
        return False
        
    def isLETZero(self):
        if self.isValid() and self.value<=0:
            return True
        return False

## Calculates porcentage to pass from a to b
## @param a. Can be an object divisible and that can be substracted
def percentage_between(a,b):
    try:
        return Percentage(b-a,a)
    except:
        return Percentage()
