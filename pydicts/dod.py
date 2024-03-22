from gettext import translation
from importlib.resources import files
from pprint import PrettyPrinter
        
try:
    t=translation('pydicts', files("pydicts") / 'locale')
    _=t.gettext
except:
    _=str

def dod_print(dod_, indent=4, depth=None, width=80, sort_dicts=True):
    """
        Make a nice print of a dictionary of nested dictionaries
    """
    pp=PrettyPrinter(indent=4, compact=False, depth=None,  width=width, sort_dicts=sort_dicts)
    pp.pprint(dod_)
    
