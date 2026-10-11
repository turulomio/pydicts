from gettext import translation
from importlib.resources import files
from pprint import pformat
import shutil
from typing import Optional

try:
    t = translation("pydicts", files("pydicts") / "locale")
    _ = t.gettext
except Exception:
    _ = str


def dod_string(
    dod_: dict,
    indent: int = 4,
    depth: Optional[int] = None,
    width: Optional[int] = None,
    sort_dicts: bool = True,
) -> str:
    """
    Returns a pretty-printed string representation of a dictionary of dictionaries (DoD).

    Args:
        dod_ (dict): The dictionary of dictionaries to format.
        indent (int, optional): The number of spaces to indent each level. Defaults to 4.
        depth (int, optional): The maximum depth to recurse when formatting. Defaults to None.
        width (int, optional): The maximum desired output width. If None, uses terminal width. Defaults to None.
        sort_dicts (bool, optional): If True, dictionary keys are sorted alphabetically. Defaults to True.

    Returns:
        str: The pretty-printed string.
    """
    if width is None:
        width = shutil.get_terminal_size(fallback=(80, 24)).columns
    return pformat(
        dod_,
        indent=indent,
        depth=depth,
        width=width,
        sort_dicts=sort_dicts,
        compact=False,
    )


def dod_print(
    dod_: dict,
    indent: int = 4,
    depth: Optional[int] = None,
    width: Optional[int] = None,
    sort_dicts: bool = True,
) -> None:
    """
    Prints a dictionary of dictionaries (DoD) in human-readable pretty-printed format.

    Args:
        dod_ (dict): The dictionary of dictionaries to print.
        indent (int, optional): The number of spaces to indent each level. Defaults to 4.
        depth (int, optional): The maximum depth to recurse when pretty-printing.
                               If None, there is no limit. Defaults to None.
        width (int, optional): The maximum desired output width. If None, uses terminal width. Defaults to None.
        sort_dicts (bool, optional): If True, dictionary keys are sorted alphabetically. Defaults to True.

    Returns:
        None
    """
    print(
        dod_string(
            dod_,
            indent=indent,
            depth=depth,
            width=width,
            sort_dicts=sort_dicts,
        )
    )


def dod_string_tables(
    dod_: dict,
    key_name: str = "Key",
    tablefmt: str = "simple_grid",
    wordwrap: bool = True,
    stretch: bool = False,
    number: Optional[int] = None,
    align: Optional[list] = None,
    maxcolwidths: Optional[list] = None,
) -> str:
    """
    Returns a formatted table string representation of a dictionary of dictionaries (DoD),
    with `key_name` as the first column.

    Args:
        dod_ (dict): The dictionary of dictionaries to format.
        key_name (str, optional): The column header for dictionary keys. Defaults to "Key".
        tablefmt (str, optional): The tabulate table format style. Defaults to "simple_grid".
        wordwrap (bool, optional): Whether to wrap text within columns. Defaults to True.
        stretch (bool, optional): Whether to stretch table to terminal width. Defaults to False.
        number (int, optional): Optional row number limit or start. Defaults to None.
        align (list, optional): Optional column alignments. Defaults to None.
        maxcolwidths (list, optional): Optional maximum column widths. Defaults to None.

    Returns:
        str: The tabular string representation.
    """
    from pydicts import lod
    rows = []
    for k, v in dod_.items():
        if isinstance(v, dict):
            row = {key_name: k}
            row.update(v)
        else:
            row = {key_name: k, "Value": v}
        rows.append(row)
    return lod.lod_string(
        rows,
        number=number,
        align=align,
        maxcolwidths=maxcolwidths,
        tablefmt=tablefmt,
        wordwrap=wordwrap,
        stretch=stretch,
    )


def dod_print_tables(
    dod_: dict,
    key_name: str = "Key",
    tablefmt: str = "simple_grid",
    wordwrap: bool = True,
    stretch: bool = False,
    number: Optional[int] = None,
    align: Optional[list] = None,
    maxcolwidths: Optional[list] = None,
) -> None:
    """
    Prints a dictionary of dictionaries (DoD) as a formatted table,
    with `key_name` as the first column.

    Args:
        dod_ (dict): The dictionary of dictionaries to print.
        key_name (str, optional): The header name for the keys column. Defaults to "Key".
        tablefmt (str, optional): The tabulate table format style. Defaults to "simple_grid".
        wordwrap (bool, optional): Whether to wrap text within columns. Defaults to True.
        stretch (bool, optional): Whether to stretch table to terminal width. Defaults to False.
        number (int, optional): Optional row number limit. Defaults to None.
        align (list, optional): Optional column alignments. Defaults to None.
        maxcolwidths (list, optional): Optional maximum column widths. Defaults to None.

    Returns:
        None
    """
    print(
        dod_string_tables(
            dod_,
            key_name=key_name,
            tablefmt=tablefmt,
            wordwrap=wordwrap,
            stretch=stretch,
            number=number,
            align=align,
            maxcolwidths=maxcolwidths,
        )
    )
