from pydicts import __version__
from os import system

def release():
    print("""Nueva versión:
  * Cambiar la version en pyproject.toml
  * Cambiar la versión y la fecha en __init__.py
  * Ejecutar otra vez poe release
  * git checkout -b pydicts-{0}
  * Modificar el Changelog en README
  * poe translate
  * linguist
  * poe translate
  * poe test
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

    
def coverage():
    system("coverage run --omit='*uno.py' -m pytest && coverage report && coverage html")


def translate():
    #es
    system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o pydicts/locale/pydicts.pot pydicts/*.py")
    system("msgmerge -N --no-wrap -U pydicts/locale/es.po pydicts/locale/pydicts.pot")
    system("msgfmt -cv -o pydicts/locale/es/LC_MESSAGES/pydicts.mo pydicts/locale/es.po")
    system("msgfmt -cv -o pydicts/locale/en/LC_MESSAGES/pydicts.mo pydicts/locale/en.po")

