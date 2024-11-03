from colorama import Style,Fore
from pydicts.currency import Currency
from pydicts.percentage import Percentage

def blue(s):
    """
        Shows a string in blue bright color
    """
    return Style.BRIGHT + Fore.BLUE + str(s) + Style.RESET_ALL

def red(s):
    """
        Shows a string in red bright color
    """
    return Style.BRIGHT + Fore.RED + str(s) + Style.RESET_ALL

def green(s):
    """
        Shows a string in green bright color
    """
    return Style.BRIGHT + Fore.GREEN + str(s) + Style.RESET_ALL

def magenta(s):
    """
        Shows a string in magenta bright color
    """
    return Style.BRIGHT + Fore.MAGENTA + str(s) + Style.RESET_ALL

def yellow(s):
    """
        Shows a string in yellow bright color
    """
    return Style.BRIGHT + Fore.YELLOW + str(s) + Style.RESET_ALL

def white(s):
    """
        Shows a string in white bright color
    """
    return Style.BRIGHT + str(s) + Style.RESET_ALL

def cyan(s):
    """
        Shows a string in cyan bright color
    """
    return Style.BRIGHT + Fore.CYAN + str(s) + Style.RESET_ALL

def currency_color(value, currency_):
    """
        Shows a currency string in green or red color
    """
    if value>=0:
        return green(Currency(value,currency_))
    else:
        return red(Currency(value,currency_))

def percentage_color(value):
    """
        Shows a percentage string in green or red color
    """
    if value>=0:
        return green(Percentage(value,1))
    else:
        return red(Currency(value,1))

def value_color(value):
    """
        Shows a value string in green or red color
    """
    if value>=0:
        return green(value)
    else:
        return red(value)
