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
        width (int, optional): The maximum desired output width. If None, uses the terminal columns. Defaults to None.
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
    Prints a dictionary of dictionaries (DoD) in a human-readable, pretty-printed format.

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
