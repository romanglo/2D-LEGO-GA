""" Files named __init__.py are used to mark directories
    on disk as a Python package directories. """

from lego.exceptions import NotInitializedException

from lego.brick import LegoBrick
from lego.collection import LegoBrickCollection
from lego.layout import LegoBrickLayout

__all__ = ["exceptions", "brick", "collection", "layout"]
