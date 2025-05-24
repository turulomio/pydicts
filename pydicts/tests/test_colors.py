from pydicts import colors,currency

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
    assert colors.currency_color(12, "EUR", 0)== colors.green("12 €")
    assert colors.currency_color("string", "EUR") == colors.blue("-")
    assert colors.currency_color(None, "EUR") == colors.blue("-")
    assert colors.currency_color(0.12345, "EUR", decimals=1)==colors.green("0.1 €")
    
def test_percentage_color():
    assert colors.percentage_color(12, decimals=0) == colors.green("1200 %")
    assert colors.percentage_color("string") == colors.blue("- %")
    assert colors.percentage_color(None) == colors.blue("- %")
    assert colors.percentage_color(0.12345, decimals=1)==colors.green("12.3 %")

    
def test_value_color():
    assert colors.value_color(12, decimals=0) == colors.green(12)
    assert colors.value_color("string") == colors.blue("-")
    assert colors.value_color(None) == colors.blue("-")
    assert colors.value_color(0.12345, decimals=1)==colors.green("0.1")
    assert colors.value_color(-0.12345, decimals=3)==colors.red("-0.123")
