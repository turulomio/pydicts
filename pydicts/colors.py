from colorama import Style,Fore
from pydicts.currency import Currency
from pydicts.percentage import Percentage

def blue(s):
    return Style.BRIGHT + Fore.BLUE + str(s) + Style.RESET_ALL

def red(s):
    return Style.BRIGHT + Fore.RED + str(s) + Style.RESET_ALL

def green(s):
    return Style.BRIGHT + Fore.GREEN + str(s) + Style.RESET_ALL

def magenta(s):
    return Style.BRIGHT + Fore.MAGENTA + str(s) + Style.RESET_ALL

def yellow(s):
    return Style.BRIGHT + Fore.YELLOW + str(s) + Style.RESET_ALL

def white(s):
    return Style.BRIGHT + str(s) + Style.RESET_ALL

def cyan(s):
    return Style.BRIGHT + Fore.CYAN + str(s) + Style.RESET_ALL

def currency_color(value, currency_):
    if value>=0:
        return green(Currency(value,currency_))
    else:
        return red(Currency(value,currency_))

def percentage_color(value):
    if value>=0:
        return green(Percentage(value,1))
    else:
        return red(Currency(value,1))

def value_color(value):
    if value>=0:
        return green(value)
    else:
        return red(value)
