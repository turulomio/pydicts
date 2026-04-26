from pydicts.lod import lod_has_key, lod_print, lod_print_first, lod_sum, lod2list, lod_average_ponderated
from gettext import translation
from importlib.resources import files
        
try:
    t=translation('pydicts', files("pydicts") / 'locale')
    _=t.gettext
except:
    _=str
## El objetivo es crear un objeto list_dict que se almacenera en self.ld con funciones set
class LOD:
    def __init__(self, name=None):
        """
        Initializes an LOD (List of Dictionaries) object.

        This class provides a wrapper around a list of dictionaries, offering convenient
        methods for common operations like printing, summing, and filtering.

        Args:
            name (str, optional): A name for this LOD instance. Defaults to the class name.
        """
        self.name=self.__class__.__name__ if name is None else name
        self.ld=[]

    def length(self):
        """
        Returns the number of dictionaries in the list.

        Returns:
            int: The number of dictionaries.
        """
        return len(self.ld)

    def has_key(self,key):
        """
        Checks if a given key exists in the first dictionary of the list.

        Args:
            key (str): The key to check for.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        return lod_has_key(self.ld,key)

    def print(self):
        """
        Prints the entire list of dictionaries using `lod_print`.
        """
        lod_print(self.ld)

    def print_first(self):
        """
        Prints only the first dictionary of the list using `lod_print_first`.
        """
        lod_print_first(self.ld)

    def sum(self, key, ignore_nones=True):
        """
        Calculates the sum of values for a specified key across all dictionaries.

        Args:
            key (str): The key whose values are to be summed.
            ignore_nones (bool, optional): If True, None values are skipped. Defaults to True.

        Returns:
            (int, float, Decimal): The sum of the values.
        """
        return lod_sum(self.ld, key, ignore_nones)

    def list(self, key, sorted=True):
        """
        Extracts all values for a specified key into a new list.

        Args:
            key (str): The key whose values are to be extracted.
            sorted (bool, optional): If True, the resulting list will be sorted. Defaults to True.

        Returns:
            list: A list containing the extracted values.
        """
        return lod2list(self.ld, key, sorted)

    def average_ponderated(self, key_numbers, key_values):
        """
        Calculates the weighted average of values for a specified key, using another key for weights.

        Args:
            key_numbers (str): The key representing the weights (numbers).
            key_values (str): The key representing the values to be averaged.

        Returns:
            (int, float, Decimal): The weighted average.
        """
        return lod_average_ponderated(self.ld, key_numbers, key_values)

    def set(self, ld):
        """
        Sets the internal list of dictionaries for this LOD object.

        Args:
            ld (list): The new list of dictionaries.

        Returns:
            LOD: The current LOD instance (for chaining).
        """
        del self.ld
        self.ld=ld
        return self

    def is_set(self):
        """
        Checks if the internal list of dictionaries (`self.ld`) has been set.

        Returns:
            bool: True if `self.ld` exists, False otherwise.
        """
        if hasattr(self, "ld"):
            return True
        print(_("You must set your lod in {}").format(self.name))
        return False

    def append(self,o):
        """
        Appends a dictionary to the internal list.

        Args:
            o (dict): The dictionary to append.
        """
        self.ld.append(o)

    def first(self):
        """
        Returns the first dictionary in the list, if available.

        Returns:
            dict or None: The first dictionary, or None if the list is empty.
        """
        return self.ld[0] if self.length()>0 else None

    def first_keys(self):
        """
        Returns a list of keys from the first dictionary in the list.

        Returns:
            list or str: A list of keys, or a message if the list is empty.
        """
        if self.length()>0:
            return self.first().keys()
        else:
            return "I can't show keys"
    
    def order_by(self, key, reverse=False):
        """
        Orders the internal list of dictionaries by the value of a specified key.

        Args:
            key (str): The key to sort by.
            reverse (bool, optional): If True, sort in descending order. Defaults to False.
        """
        self.ld=sorted(self.ld,  key=lambda item: item[key], reverse=reverse)
