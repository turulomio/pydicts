from gettext import translation
from importlib.resources import files
from pprint import PrettyPrinter
        
try:
    t=translation('pydicts', files("pydicts") / 'locale')
    _=t.gettext
except:
    _=str

def dod_print(dod_, indent=4, depth=None, width=80, sort_dicts=True):
    """Prints a dictionary of dictionaries (DoD) in a human-readable, pretty-printed format.

    Args:
        dod_ (dict): The dictionary of dictionaries to print.
        indent (int, optional): The number of spaces to indent each level. Defaults to 4.
        depth (int, optional): The maximum depth to recurse when pretty-printing.
                               If None, there is no limit. Defaults to None.
        width (int, optional): The maximum desired output width. Defaults to 80.
        sort_dicts (bool, optional): If True, dictionary keys are sorted alphabetically. Defaults to True.

    Returns:
        None
    """
    pp=PrettyPrinter(indent=4, compact=False, depth=None,  width=width, sort_dicts=sort_dicts)
    pp.pprint(dod_)
    
