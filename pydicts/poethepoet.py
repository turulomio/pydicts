from pydicts import __version__, lod
from os import system

def release():
    """
    Prints instructions for creating a new release of the pydicts library.
    """
    print("""Nueva versión:
  * Cambiar la version en pyproject.toml
  * Cambiar la versión y la fecha en __init__.py
  * Ejecutar otra vez poe release
  * git checkout -b pydicts-{0}
  * poe translate
  * linguist
  * poe translate
  * poe test
  * poe jupyter
  * git commit -a -m 'pydicts-{0}'
  * git push
  * Hacer un pull request con los cambios a main
  * Hacer un nuevo tag en GitHub
  * git checkout main
  * git pull
  * poetry build
  * poetry publish
  * Crea un nuevo ebuild de pydicts en Gentoo con la nueva versión
  * Subelo al repositorio myportage

""".format(__version__))

def jupyter():
    """
    Starts the Jupyter Book documentation server. I's not needed to be build due to it will be build in Github
    for GitHub Pages publication.
    """
    system("cd jupyter && jupyter book start --execute")
    system("touch docs/.nojekyll")
    
def coverage():
    """
    Runs pytest with coverage, generates a coverage report, and creates an HTML report.
    """
    system("coverage run --omit='*uno.py' -m pytest && coverage report && coverage html")


def translate():
    """
    Generates translation files (.pot, .po, .mo) for the pydicts project.
    It extracts translatable strings, merges them with existing translations,
    and compiles them into binary message catalogs.
    """
    #es
    system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o pydicts/locale/pydicts.pot pydicts/*.py")
    system("msgmerge -N --no-wrap -U pydicts/locale/es.po pydicts/locale/pydicts.pot")
    system("msgfmt -cv -o pydicts/locale/es/LC_MESSAGES/pydicts.mo pydicts/locale/es.po")
    
    
def currencies():
    """
    Updates the `currencies.json` file with the latest currency data from the `ccy` module.

    This script is necessary because `ccy` updates can be slow, and this allows
    for a more up-to-date currency list.

    **Note:** The `ccy` module must be installed manually (`pip install ccy`)
    before running this function to update `currencies.json`.

    The original `ccy` project license is included below for reference:

    Copyright (c) 2009-2023, Quantmind
    All rights reserved.

    Redistribution and use in source and binary forms, with or without modification,
    are permitted provided that the following conditions are met:

        * Redistributions of source code must retain the above copyright notice,
           this list of conditions and the following disclaimer.
         * Redistributions in binary form must reproduce the above copyright notice,
           this list of conditions and the following disclaimer in the documentation
           and/or other materials provided with the distribution.
         * Neither the name of the author nor the names of its contributors
           may be used to endorse or promote products derived from this software without
           specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
        ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
        WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
        IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
        INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
        BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
        DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
        LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
        OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
        OF THE POSSIBILITY OF SUCH DAMAGE.
    """
    from ccy import dump_currency_table
    from html import unescape
    lod_=[]
    for code_, name, iso, symbol, country, order, rounding in dump_currency_table()[1:]:
        print(code_, name, iso, symbol, country, order, rounding)
        lod_.append({
            "code":code_, 
            "name":name, 
            "iso":iso, 
            "symbol_html":symbol, 
            "symbol": unescape(symbol), 
            "country":country, 
            "order":order, 
            "rounding":rounding
        })
    lod_.append({
        "code":"u", 
        "name": "Unit", 
        "iso":"", 
        "symbol_html":"u", 
        "symbol": "u", 
        "country":"WW", 
        "order": 0, 
        "rounding":6, 
    })
    lod_=lod.lod_order_by(lod_,"code")
    with open("pydicts/currencies.json", "w") as f:
        f.write(str(lod_))
        
