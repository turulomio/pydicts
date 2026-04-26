from colorama import Style,Fore
from decimal import Decimal
from pydicts.currency import Currency
from pydicts.percentage import Percentage

def blue(s):
    """Returns a string formatted in bright blue color for terminal output.

    Args:
        s (any): The string or object to color.

    Returns:
        str: The colored string.
    """
    return Style.BRIGHT + Fore.BLUE + str(s) + Style.RESET_ALL

def red(s):
    """Returns a string formatted in bright red color for terminal output.

    Args:
        s (any): The string or object to color.

    Returns:
        str: The colored string.
    """
    return Style.BRIGHT + Fore.RED + str(s) + Style.RESET_ALL

def green(s):
    """Returns a string formatted in bright green color for terminal output.

    Args:
        s (any): The string or object to color.

    Returns:
        str: The colored string.
    """
    return Style.BRIGHT + Fore.GREEN + str(s) + Style.RESET_ALL

def magenta(s):
    """Returns a string formatted in bright magenta color for terminal output.

    Args:
        s (any): The string or object to color.

    Returns:
        str: The colored string.
    """
    return Style.BRIGHT + Fore.MAGENTA + str(s) + Style.RESET_ALL

def yellow(s):
    """Returns a string formatted in bright yellow color for terminal output.

    Args:
        s (any): The string or object to color.

    Returns:
        str: The colored string.
    """
    return Style.BRIGHT + Fore.YELLOW + str(s) + Style.RESET_ALL

def white(s):
    """Returns a string formatted in bright white color for terminal output.

    Args:
        s (any): The string or object to color.

    Returns:
        str: The colored string.
    """
    return Style.BRIGHT + str(s) + Style.RESET_ALL

def cyan(s):
    """Returns a string formatted in bright cyan color for terminal output.

    Args:
        s (any): The string or object to color.

    Returns:
        str: The colored string.
    """
    return Style.BRIGHT + Fore.CYAN + str(s) + Style.RESET_ALL

def currency_color(value, currency_, decimals=2):
    """Returns a currency string formatted in green (for non-negative values) or red (for negative values).
    Non-numeric values are displayed in blue.

    Args:
        value (int, float, Decimal): The monetary value.
        currency_ (str): The currency code (e.g., "EUR").
        decimals (int, optional): The number of decimal places for formatting. Defaults to 2.

    Returns:
        str: The colored and formatted currency string.
    """
    if value.__class__ not in (float,  int,  Decimal):
        return blue("-")
    
    if value>=0:
        return green(Currency(value,currency_).string(decimals))
    else:
        return red(Currency(value,currency_).string(decimals))

def percentage_color(value, decimals=2):
    """Returns a percentage string formatted in green (for non-negative values) or red (for negative values).
    Non-numeric values are displayed in blue.

    Args:
        value (int, float, Decimal): The percentage value (e.g., 0.12 for 12%).
        decimals (int, optional): The number of decimal places for formatting. Defaults to 2.

    Returns:
        str: The colored and formatted percentage string.
    """
    if value.__class__ not in (float,  int,  Decimal):
        return blue("- %")
    if value>=0:
        return green(Percentage(value,1).string(decimals))
    else:
        return red(Currency(value,1).string(decimals))

def value_color(value, decimals=2):
    """Returns a numeric value formatted in green (for non-negative values) or red (for negative values).
    Non-numeric values are displayed in blue.

    Args:
        value (int, float, Decimal): The numeric value.
        decimals (int, optional): The number of decimal places for rounding. Defaults to 2.

    Returns:
        str: The colored and formatted value string.
    """
    if value.__class__ not in  (float,  int,  Decimal):
        return blue("-")
    if value>=0:
        return green(round(value, decimals))
    else:
        return red(round(value, decimals))
