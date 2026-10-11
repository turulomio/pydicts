# AGENTS.md — Instrucciones y Guía de Arquitectura para Agentes

Este documento contiene las directrices, estructura y convenciones esenciales del repositorio `pydicts` para que cualquier agente o desarrollador trabaje de manera coherente.

---

## 1. Visión General del Proyecto

`pydicts` es una librería en Python (soporta Python 3.10+) orientada a facilitar la manipulación, formateo, ordenación, agregación y conversión de estructuras de datos comunes en Python:
- **LOD**: *List of Dictionaries* (`list[dict]`).
- **LOL**: *List of Lists* (`list[list]`).
- **DOD**: *Dictionary of Dictionaries* (`dict[Any, dict]`).
- **LOD_XYV / LOD_YMV**: Estructuras especializadas con coordenadas X/Y o Año/Mes.
- Clases de soporte: `Currency`, `Percentage`, codecs JSON (`MyJsonEncoder`), conversor LaTeX (`pylatex`).

---

## 2. Estructura del Código

```text
pydicts/
├── pydicts/
│   ├── __init__.py          # Exporta __version__, __versiondate__, LOD, LOL, DOD
│   ├── classes.py           # Envoltorios orientados a objetos (LOD, LOL, DOD)
│   ├── lod.py               # Funciones funcionales y de formato para LOD
│   ├── lol.py               # Funciones para manipular listas de listas
│   ├── dod.py               # Funciones para diccionarios de diccionarios
│   ├── casts.py             # Funciones de casteo y conversión de tipos
│   ├── currency.py          # Clase y utilidades para monedas
│   ├── percentage.py        # Clase y utilidades para porcentajes
│   ├── lod_xyv.py           # Manipulación de matrices dispersas / coordenadas
│   ├── lod_ymv.py           # Agrupación temporal año-mes-valor
│   ├── poethepoet.py        # Tareas poe (test, coverage, translate, release)
│   └── tests/               # Batería completa de pruebas unitarias pytest
├── jupyter/                 # Documentación basada en Jupyter Book
├── pyproject.toml           # Configuración de Poetry, dependencias y scripts Poe
└── AGENTS.md                # Esta guía
```

---

## 3. Directrices de Diseño y Convenciones

### Estilo de Importaciones
- Dentro de `classes.py` o módulos internos, **usar imports genéricos del módulo** (`from pydicts import lod, lol, dod`) en lugar de importar decenas de funciones individuales sueltas.
- Calificar las llamadas internas como `lod.lod_sum(...)`, `lol.lol_order_by(...)`, `dod.dod_print(...)`.

### Clases de Objetos (`LOD`, `LOL`, `DOD`)
- Implementan los protocolos nativos de Python (`collections.abc.Sequence` y `Mapping`):
  - Soportan `len()`, iteración (`for item in obj:`), indexación (`obj[0]`), slicing (`obj[1:3]`), pertenencia (`in`) y evaluación booleana.
  - Implementan `__repr__` y `__str__` (mostrando tablas formateadas cuando aplica).
- Soportan *method chaining* en operaciones mutables (`order_by`, `filter`, `calculate`, etc.).
- Permiten conversión bidireccional limpia:
  - `lod.to_dod(key)`, `lod.to_lol(keys)`, `lod.to_dictkv(...)`
  - `dod.to_lod()`

### Soporte de Lambdas en Filtros y Cálculos
- Funciones como `filter()` y `calculate()` deben soportar opcionalmente tanto lambdas de un argumento `lambda d: ...` como de dos argumentos `lambda d, idx: ...`.

### Formateo e I18n
- Se utiliza `gettext` para localización (`_("...")`). No romper los bloques `try/except` de importación de `translation`.
- Las tablas en consola usan `tabulate` y las funciones internas `_fit_maxcolwidths` para adaptarse al ancho de la terminal sin desbordar.

---

## 4. Flujo de Trabajo y Comandos

El proyecto utiliza **Poetry** como gestor de paquetes y **PoeThePoet** para tareas:

- **Ejecutar tests**:
  ```bash
  poetry run pytest
  # o bien:
  poetry run poe test
  ```
- **Ver cobertura**:
  ```bash
  poetry run poe coverage
  ```
- **Actualizar traducciones gettext**:
  ```bash
  poetry run poe translate
  ```
- **Construir / levantar Jupyter Book**:
  ```bash
  poetry run poe jupyter
  ```

---

## 5. Reglas Esenciales para Modificaciones

1. **Mantener siempre los tests en verde**: Ejecutar `poetry run pytest` antes de finalizar cualquier tarea.
2. **Preservar compatibilidad hacia atrás**: No renombrar ni romper la signatura de las funciones históricas en `lod.py`, `lol.py` ni `dod.py`.
3. **Tipado y docstrings**: Mantener type hints (`typing` / Python 3.10+) y docstrings claros en formato Google/Sphinx.
