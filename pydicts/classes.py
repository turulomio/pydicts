from collections.abc import Mapping, Sequence
from gettext import translation
from importlib.resources import files
import inspect
from typing import Any, Callable, Iterator, Optional, Union

from pydicts import dod, lod, lol

try:
    t = translation("pydicts", files("pydicts") / "locale")
    _ = t.gettext
except Exception:
    _ = str


# ==============================================================================
# LOD (List of Dictionaries)
# ==============================================================================

class LOD(Sequence[dict]):
    """
    Wrapper around a list of dictionaries (LOD) providing Pythonic container protocols
    and convenient manipulation, aggregation, conversion, and display methods.
    """

    def __init__(self, data: Optional[Union[list[dict], "LOD"]] = None, name: Optional[str] = None):
        """
        Initializes an LOD (List of Dictionaries) object.

        Args:
            data (list[dict] | LOD, optional): Initial list of dictionaries. Defaults to empty list.
            name (str, optional): A name for this LOD instance. Defaults to the class name.
        """
        self.name = self.__class__.__name__ if name is None else name
        if data is None:
            self.ld: list[dict] = []
        elif isinstance(data, LOD):
            self.ld = list(data.ld)
        elif isinstance(data, list):
            self.ld = list(data)
        else:
            self.ld = list(data)

    # ---------------------------------------------------------
    # Python Container Protocols
    # ---------------------------------------------------------

    def __len__(self) -> int:
        return len(self.ld)

    def __iter__(self) -> Iterator[dict]:
        return iter(self.ld)

    def __getitem__(self, index: Union[int, slice]) -> Union[dict, "LOD"]:
        if isinstance(index, slice):
            return self.__class__(self.ld[index], name=self.name)
        return self.ld[index]

    def __bool__(self) -> bool:
        return bool(self.ld)

    def __contains__(self, item: Any) -> bool:
        return item in self.ld

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, LOD):
            return self.ld == other.ld
        if isinstance(other, list):
            return self.ld == other
        return False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, length={len(self)})"

    def __str__(self) -> str:
        return self.string()

    # ---------------------------------------------------------
    # Backward compatibility and access helpers
    # ---------------------------------------------------------

    def length(self) -> int:
        """
        Returns the number of dictionaries in the list.
        """
        return len(self.ld)

    def has_key(self, key: str) -> bool:
        """
        Checks if a given key exists in the first dictionary of the list.
        """
        return lod.lod_has_key(self.ld, key)

    def is_set(self) -> bool:
        """
        Checks if the internal list of dictionaries (`self.ld`) has been set.
        """
        if hasattr(self, "ld"):
            return True
        print(_("You must set your lod in {}").format(self.name))
        return False

    def set(self, ld_: list[dict]) -> "LOD":
        """
        Sets the internal list of dictionaries for this LOD object.
        """
        self.ld = ld_ if isinstance(ld_, list) else list(ld_)
        return self

    def append(self, o: dict) -> None:
        """
        Appends a dictionary to the internal list.
        """
        self.ld.append(o)

    def extend(self, items: Union[list[dict], "LOD"]) -> None:
        """
        Extends the internal list with another list of dictionaries or LOD.
        """
        if isinstance(items, LOD):
            self.ld.extend(items.ld)
        else:
            self.ld.extend(items)

    def first(self) -> Optional[dict]:
        """
        Returns the first dictionary in the list, or None if empty.
        """
        return self.ld[0] if len(self.ld) > 0 else None

    def first_keys(self) -> list:
        """
        Returns a list of keys from the first dictionary in the list, or an empty list if empty.
        """
        if len(self.ld) > 0:
            return list(self.first().keys())
        return []

    def keys(self) -> Optional[list]:
        """
        Returns all unique keys present across all dictionaries in the list.
        """
        return lod.lod_keys(self.ld)

    # ---------------------------------------------------------
    # Formatting and Display
    # ---------------------------------------------------------

    def string(
        self,
        number: Optional[int] = None,
        align: Optional[list] = None,
        maxcolwidths: Optional[list] = None,
        tablefmt: str = "simple_grid",
        wordwrap: bool = True,
        stretch: bool = False,
    ) -> str:
        """
        Returns the formatted table string of the list of dictionaries using `lod.lod_string`.
        """
        return lod.lod_string(
            self.ld,
            number=number,
            align=align,
            maxcolwidths=maxcolwidths,
            tablefmt=tablefmt,
            wordwrap=wordwrap,
            stretch=stretch,
        )

    def print(
        self,
        number: Optional[int] = None,
        align: Optional[list] = None,
        maxcolwidths: Optional[list] = None,
        tablefmt: str = "simple_grid",
        wordwrap: bool = True,
        stretch: bool = False,
    ) -> None:
        """
        Prints the formatted list of dictionaries using `lod.lod_print`.
        """
        lod.lod_print(
            self.ld,
            number=number,
            align=align,
            maxcolwidths=maxcolwidths,
            tablefmt=tablefmt,
            wordwrap=wordwrap,
            stretch=stretch,
        )

    def print_first(self) -> None:
        """
        Prints only the first dictionary of the list using `lod.lod_print(..., number=1)`.
        """
        lod.lod_print(self.ld, number=1)

    # ---------------------------------------------------------
    # Aggregations & Calculations
    # ---------------------------------------------------------

    def sum(self, key: str, ignore_nones: bool = True) -> Any:
        """
        Calculates the sum of values for a specified key across all dictionaries.
        """
        return lod.lod_sum(self.ld, key, ignore_nones)

    def sum_positives(self, key: str) -> Any:
        """
        Calculates the sum of positive values for a specified key across all dictionaries.
        """
        return lod.lod_sum_positives(self.ld, key)

    def sum_negatives(self, key: str) -> Any:
        """
        Calculates the sum of negative values for a specified key across all dictionaries.
        """
        return lod.lod_sum_negatives(self.ld, key)

    def average(self, key: str) -> Any:
        """
        Calculates the average of values for a specified key across all dictionaries.
        """
        return lod.lod_average(self.ld, key)

    def average_ponderated(self, key_numbers: str, key_values: str) -> Any:
        """
        Calculates the weighted average of values for a specified key, using another key for weights.
        """
        return lod.lod_average_ponderated(self.ld, key_numbers, key_values)

    def median(self, key: str) -> Any:
        """
        Calculates the median of values for a specified key across all dictionaries.
        """
        return lod.lod_median(self.ld, key)

    def min_value(self, key: str) -> Any:
        """
        Returns the minimum value for a specified key.
        """
        return lod.lod_min_value(self.ld, key)

    def max_value(self, key: str) -> Any:
        """
        Returns the maximum value for a specified key.
        """
        return lod.lod_max_value(self.ld, key)

    def count(self, condition_func: Callable[..., bool]) -> int:
        """
        Counts the number of dictionaries matching the given predicate function.
        `condition_func` can accept `(d)` or `(d, index)`.
        """
        try:
            sig = inspect.signature(condition_func)
            params = len(sig.parameters)
        except (ValueError, TypeError):
            params = 1

        wrapper = condition_func if params >= 2 else (lambda d, idx: condition_func(d))
        return lod.lod_count(self.ld, wrapper)

    def list(self, key: str, sorted: bool = True, cast: Optional[str] = None) -> list:
        """
        Extracts all values for a specified key into a new list.
        """
        return lod.lod2list(self.ld, key, sorted=sorted, cast=cast)

    def list_distinct(self, key: str, sorted: bool = True, cast: Optional[str] = None) -> list:
        """
        Extracts distinct values for a specified key into a new list.
        """
        return lod.lod2list_distinct(self.ld, key, sorted=sorted, cast=cast)

    # ---------------------------------------------------------
    # Transformations & Manipulations
    # ---------------------------------------------------------

    def order_by(self, key: str, reverse: bool = False, none_at_top: bool = True) -> "LOD":
        """
        Orders the internal list of dictionaries by the value of a specified key.
        Updates self in place and returns self for chaining.
        """
        self.ld = lod.lod_order_by(self.ld, key, reverse=reverse, none_at_top=none_at_top)
        return self

    def filter_keys(self, keys: list[str]) -> "LOD":
        """
        Returns a new LOD containing only the specified keys in each dictionary.
        """
        return self.__class__(lod.lod_filter_keys(self.ld, keys), name=self.name)

    def filter(self, condition_func: Callable[..., bool]) -> "LOD":
        """
        Returns a new LOD containing dictionaries that satisfy condition_func.
        `condition_func` can accept `(d)` or `(d, index)`.
        """
        try:
            sig = inspect.signature(condition_func)
            params = len(sig.parameters)
        except (ValueError, TypeError):
            params = 1

        wrapper = condition_func if params >= 2 else (lambda d, idx: condition_func(d))
        return self.__class__(lod.lod_filter_dictionaries(self.ld, wrapper), name=self.name)

    def calculate(self, key: str, formula_func: Callable[..., Any]) -> "LOD":
        """
        Calculates a new key or updates an existing key using formula_func.
        Modifies self in place and returns self for chaining.
        `formula_func` can accept `(d)` or `(d, index)`.
        """
        try:
            sig = inspect.signature(formula_func)
            params = len(sig.parameters)
        except (ValueError, TypeError):
            params = 1

        wrapper = formula_func if params >= 2 else (lambda d, idx: formula_func(d))
        self.ld = lod.lod_calculate(self.ld, key, wrapper, clone=False)
        return self

    def rename_key(self, from_: str, to_: str) -> "LOD":
        """
        Renames a key in all dictionaries in place.
        """
        self.ld = lod.lod_rename_key(self.ld, from_, to_)
        return self

    def remove_key(self, key: str) -> "LOD":
        """
        Removes a key from all dictionaries in place.
        """
        self.ld = lod.lod_remove_key(self.ld, key)
        return self

    def reorder_keys(self, keys: list[str]) -> "LOD":
        """
        Reorders keys in all dictionaries according to the specified list.
        """
        self.ld = lod.lod_reorder_keys(self.ld, keys)
        return self

    def remove_duplicates(self) -> "LOD":
        """
        Removes duplicate dictionaries from the list in place.
        """
        self.ld = lod.lod_remove_duplicates(self.ld)
        return self

    def aggregate_sum(self, key_to_sum: str) -> "LOD":
        """
        Groups dictionaries by all keys except one, summing that key for duplicates.
        """
        return self.__class__(lod.lod_aggregate_sum(self.ld, key_to_sum), name=self.name)

    def join(self, other: Union[list[dict], "LOD"], calc_key: str, operation: str = "+") -> "LOD":
        """
        Joins another LOD or list of dictionaries on matching keys and applies an operation.
        """
        other_list = other.ld if isinstance(other, LOD) else other
        return self.__class__(lod.lod_join(self.ld, other_list, calc_key=calc_key, operation=operation), name=self.name)

    def clone(self) -> "LOD":
        """
        Returns a deep copy of this LOD instance.
        """
        return self.__class__(lod.lod_clone(self.ld), name=self.name)

    # ---------------------------------------------------------
    # Conversions
    # ---------------------------------------------------------

    def to_dod(self, key: str) -> "DOD":
        """
        Converts this LOD to a DOD (Dictionary of Dictionaries) indexed by key.
        """
        return DOD(lod.lod2dod(self.ld, key), name=self.name)

    def to_odod(self, key: str) -> "DOD":
        """
        Converts this LOD to an OrderedDict of Dictionaries indexed by key.
        """
        return DOD(lod.lod2odod(self.ld, key), name=self.name)

    def to_dod_tuple(self, key1: str, key2: str) -> "DOD":
        """
        Converts this LOD to a DOD with tuple keys (key1, key2).
        """
        return DOD(lod.lod2dod_tuple(self.ld, key1, key2), name=self.name)

    def to_dictkv(self, key: str, value: str) -> dict:
        """
        Converts this LOD to a key-value dictionary using the specified keys.
        """
        return lod.lod2dictkv(self.ld, key, value)

    def to_lol(self, keys: Optional[list[str]] = None) -> "LOL":
        """
        Converts this LOD to a LOL (List of Lists), with an optional header or key selection.
        """
        return LOL(lod.lod2lol(self.ld, keys=keys), name=self.name)

    def to_lood(self, keys: list[str]) -> list:
        """
        Converts this LOD to a list of OrderedDicts with specified keys.
        """
        return lod.lod2lood(self.ld, keys)


# ==============================================================================
# LOL (List of Lists)
# ==============================================================================

class LOL(Sequence[list]):
    """
    Wrapper around a list of lists (LOL) providing Pythonic container protocols
    and convenient manipulation, aggregation, and display methods.
    """

    def __init__(self, data: Optional[Union[list[list], "LOL"]] = None, name: Optional[str] = None):
        """
        Initializes an LOL (List of Lists) object.

        Args:
            data (list[list] | LOL, optional): Initial list of lists. Defaults to empty list.
            name (str, optional): A name for this LOL instance. Defaults to the class name.
        """
        self.name = self.__class__.__name__ if name is None else name
        if data is None:
            self.lol: list[list] = []
        elif isinstance(data, LOL):
            self.lol = [list(r) for r in data.lol]
        elif isinstance(data, list):
            self.lol = [list(r) if isinstance(r, list) else r for r in data]
        else:
            self.lol = list(data)

    # ---------------------------------------------------------
    # Python Container Protocols
    # ---------------------------------------------------------

    def __len__(self) -> int:
        return len(self.lol)

    def __iter__(self) -> Iterator[list]:
        return iter(self.lol)

    def __getitem__(self, index: Union[int, slice]) -> Union[list, "LOL"]:
        if isinstance(index, slice):
            return self.__class__(self.lol[index], name=self.name)
        return self.lol[index]

    def __bool__(self) -> bool:
        return bool(self.lol)

    def __contains__(self, item: Any) -> bool:
        return item in self.lol

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, LOL):
            return self.lol == other.lol
        if isinstance(other, list):
            return self.lol == other
        return False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, rows={len(self)})"

    def __str__(self) -> str:
        return self.string()

    # ---------------------------------------------------------
    # Access and Mutation
    # ---------------------------------------------------------

    def set(self, data: list[list]) -> "LOL":
        """
        Sets the internal list of lists.
        """
        self.lol = data if isinstance(data, list) else list(data)
        return self

    def append(self, row: list) -> None:
        """
        Appends a row to the internal list of lists.
        """
        self.lol.append(row)

    def extend(self, rows: Union[list[list], "LOL"]) -> None:
        """
        Extends the list of lists with other rows or another LOL.
        """
        if isinstance(rows, LOL):
            self.lol.extend(rows.lol)
        else:
            self.lol.extend(rows)

    def add_row(self, index: int, row: list) -> "LOL":
        """
        Inserts a row at the specified index.
        """
        self.lol = lol.lol_add_row(self.lol, index, row)
        return self

    def add_column(self, index: int, column: list) -> "LOL":
        """
        Inserts a column across all rows at the specified index.
        """
        self.lol = lol.lol_add_column(self.lol, index, column)
        return self

    def remove_rows(self, indexes: list[int]) -> "LOL":
        """
        Removes rows by index.
        """
        self.lol = lol.lol_remove_rows(self.lol, indexes)
        return self

    def remove_columns(self, indexes: list[int]) -> "LOL":
        """
        Removes columns by index from all rows.
        """
        self.lol = lol.lol_remove_columns(self.lol, indexes)
        return self

    def get_row(self, row_index: int) -> list:
        """
        Returns a specific row by index.
        """
        return lol.lol_get_row(self.lol, row_index)

    def get_column(self, col_index: int) -> list:
        """
        Returns a specific column by index across all rows.
        """
        return lol.lol_get_column(self.lol, col_index)

    def transposed(self) -> "LOL":
        """
        Returns a transposed copy of the list of lists.
        """
        return self.__class__(lol.lol_transposed(self.lol), name=self.name)

    def order_by(self, index: int, reverse: bool = False, none_at_top: bool = True) -> "LOL":
        """
        Sorts rows by the value at the given column index.
        """
        self.lol = lol.lol_order_by(self.lol, index, reverse=reverse, none_at_top=none_at_top)
        return self

    # ---------------------------------------------------------
    # Aggregations
    # ---------------------------------------------------------

    def sum_row(self, row_index: int, from_index: int = 0, to_index: Optional[int] = None, zerovalue: Any = 0) -> Any:
        """
        Calculates the sum of elements within a specific row.
        """
        row = self.get_row(row_index)
        return lol.lol_sum_row(row, from_index=from_index, to_index=to_index, zerovalue=zerovalue)

    def sum_column(self, column_index: int, from_index: int = 0, to_index: Optional[int] = None, zerovalue: Any = 0) -> Any:
        """
        Calculates the sum of elements in a specific column across a range of rows.
        """
        end_idx = len(self.lol) if to_index is None else to_index
        return lol.lol_sum_column(self.lol, column_index, from_index, end_idx, zerovalue=zerovalue)

    # ---------------------------------------------------------
    # Formatting and Display
    # ---------------------------------------------------------

    def string(
        self,
        number: Optional[int] = None,
        align: Optional[list] = None,
        maxcolwidths: Optional[list] = None,
        tablefmt: str = "simple_grid",
        wordwrap: bool = True,
        stretch: bool = False,
    ) -> str:
        """
        Returns the formatted table string using `lol.lol_string`.
        """
        return lol.lol_string(
            self.lol,
            number=number,
            align=align,
            maxcolwidths=maxcolwidths,
            tablefmt=tablefmt,
            wordwrap=wordwrap,
            stretch=stretch,
        )

    def print(
        self,
        number: Optional[int] = None,
        align: Optional[list] = None,
        maxcolwidths: Optional[list] = None,
        tablefmt: str = "simple_grid",
        wordwrap: bool = True,
        stretch: bool = False,
    ) -> None:
        """
        Prints the formatted list of lists table using `lol.lol_print`.
        """
        lol.lol_print(
            self.lol,
            number=number,
            align=align,
            maxcolwidths=maxcolwidths,
            tablefmt=tablefmt,
            wordwrap=wordwrap,
            stretch=stretch,
        )


# ==============================================================================
# DOD (Dictionary of Dictionaries)
# ==============================================================================

class DOD(Mapping[Any, dict]):
    """
    Wrapper around a dictionary of dictionaries (DOD) providing Pythonic mapping protocols
    and convenient conversion and pretty-printing methods.
    """

    def __init__(self, data: Optional[Union[dict[Any, dict], "DOD"]] = None, name: Optional[str] = None):
        """
        Initializes a DOD (Dictionary of Dictionaries) object.

        Args:
            data (dict[Any, dict] | DOD, optional): Initial dictionary of dictionaries. Defaults to empty dict.
            name (str, optional): A name for this DOD instance. Defaults to the class name.
        """
        self.name = self.__class__.__name__ if name is None else name
        if data is None:
            self.dod: dict[Any, dict] = {}
        elif isinstance(data, DOD):
            self.dod = dict(data.dod)
        elif isinstance(data, dict):
            self.dod = dict(data)
        else:
            self.dod = dict(data)

    # ---------------------------------------------------------
    # Python Mapping Protocols
    # ---------------------------------------------------------

    def __len__(self) -> int:
        return len(self.dod)

    def __iter__(self) -> Iterator[Any]:
        return iter(self.dod)

    def __getitem__(self, key: Any) -> dict:
        return self.dod[key]

    def __setitem__(self, key: Any, value: dict) -> None:
        self.dod[key] = value

    def __delitem__(self, key: Any) -> None:
        del self.dod[key]

    def __bool__(self) -> bool:
        return bool(self.dod)

    def __contains__(self, key: Any) -> bool:
        return key in self.dod

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, DOD):
            return self.dod == other.dod
        if isinstance(other, dict):
            return self.dod == other
        return False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, entries={len(self)})"

    # ---------------------------------------------------------
    # Dict helpers
    # ---------------------------------------------------------

    def keys(self):
        return self.dod.keys()

    def values(self):
        return self.dod.values()

    def items(self):
        return self.dod.items()

    def get(self, key: Any, default: Any = None) -> Any:
        return self.dod.get(key, default)

    def set(self, data: dict[Any, dict]) -> "DOD":
        """
        Sets the internal dictionary of dictionaries.
        """
        self.dod = data if isinstance(data, dict) else dict(data)
        return self

    # ---------------------------------------------------------
    # Display & Conversion
    # ---------------------------------------------------------

    def print(self, indent: int = 4, depth: Optional[int] = None, width: int = 80, sort_dicts: bool = True) -> None:
        """
        Pretty-prints the dictionary of dictionaries using `dod.dod_print`.
        """
        dod.dod_print(self.dod, indent=indent, depth=depth, width=width, sort_dicts=sort_dicts)

    def to_lod(self) -> LOD:
        """
        Converts this dictionary of dictionaries into an LOD using `lod.dod2lod`.
        """
        return LOD(lod.dod2lod(self.dod), name=self.name)
