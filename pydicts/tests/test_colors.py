from pydicts import colors

def test_colors():
    s="PyDicts"
    colors.blue(s)
    colors.cyan(s)
    colors.green(s)
    colors.magenta(s)
    colors.red(s)
    colors.white(s)
    colors.yellow(s)
    
def test_currency_color():
    colors.currency_color(12, "EUR")
    colors.currency_color("string", "EUR")
    colors.currency_color(None, "EUR")
    
def test_percentage_color():
    colors.percentage_color(12)
    colors.percentage_color("string")
    colors.percentage_color(None)
    
def test_value_color():
    colors.value_color(12)
    colors.value_color("string")
    colors.value_color(None)
