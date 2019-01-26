""" Files named __init__.py are used to mark directories
    on disk as a Python package directories. """

from test.brick_test import LegoBrick_Test
from test.collection_test import LegoBrickCollection_Test
from test.layout_test import LegoBrickLayout_Test

__all__ = ["brick_test", "collection_test", "layout_test"]
