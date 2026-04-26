class LodException(Exception):
    """
    Custom exception for errors related to List of Dictionaries (LoD) operations.
    """
    pass
    
class CastException(Exception):
    """
    Custom exception for errors during type casting operations.
    """
    pass
    
class LodXYVException(Exception):
    """
    Custom exception for errors related to List of Dictionaries (X, Y, Value) transformations.
    """
    pass
    
class LodYMVException(Exception):
    """
    Custom exception for errors related to List of Dictionaries (Year, Month, Value) transformations.
    """
    pass
    
class LolException(Exception):
    """
    Custom exception for errors related to List of Lists (LoL) operations.
    """
    pass

class CurrencyOperationsException(Exception):
    """
    Custom exception for errors during Currency object operations, especially when currencies mismatch.
    """
    pass
