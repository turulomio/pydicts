"""
PyDicts: A Python library for convenient dictionary and list of dictionary manipulations.
"""
from datetime import datetime
__version__="2.0.1"
__versiondatetime__= datetime(2026, 11, 20, 7, 39)
__versiondate__=__versiondatetime__.date()

from pydicts.classes import LOD, LOL, DOD

__all__ = ["LOD", "LOL", "DOD"]
