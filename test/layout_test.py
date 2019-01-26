# brick_test.py

import unittest

from lego.brick import LegoBrick
from lego.collection import LegoBrickCollection
from lego.layout import LegoBrickLayout
from lego.exceptions import NotInitializedException


class LegoBrickLayout_Test(unittest.TestCase):
    def test_wrongInitialization(self):
        layout = LegoBrickLayout()
        throws = False
        try:
            layout.initialize(0, 0, None)
        except ValueError as e:
            throws = True
        self.assertTrue(
            throws,
            "LegoBrickLayout initialize() didn't throw ValueError on illegal parameter"
        )
        self.assertFalse(layout.isInitialized())

        throws = False
        try:
            layout.initialize(10, 0, None)
        except ValueError as e:
            throws = True
        self.assertTrue(
            throws,
            "LegoBrickLayout initialize() didn't throw ValueError on illegal parameter"
        )
        self.assertFalse(layout.isInitialized())

        throws = False
        try:
            layout.initialize(10, 10, None)
        except TypeError as e:
            throws = True
        self.assertTrue(
            throws,
            "LegoBrickLayout initialize() didn't throw TypeError on illegal parameter"
        )

    def test_initialization(self):
        width = 1
        height = 1

        collection = self.__createBrickCollection(1)
        layout = LegoBrickLayout()
        self.assertFalse(layout.isInitialized())
        layout.initialize(width, height, collection)
        self.assertTrue(layout.isInitialized())
        self.assertEqual(width, layout.getWidth())
        self.assertEqual(height, layout.getHeight())
        self.assertEqual(0, layout.getCoveredArea())

    def test_copy(self):
        width = 1
        height = 1

        collection = self.__createBrickCollection(5)
        layout = LegoBrickLayout()
        layout.initialize(width, height, collection)
        self.assertEqual(width, layout.getWidth())
        self.assertEqual(height, layout.getHeight())
        self.assertEqual(0, layout.getCoveredArea())

    def test_equals(self):
        width = 1
        height = 1

        collection = self.__createBrickCollection(1)
        layout = LegoBrickLayout()
        self.assertFalse(layout.isInitialized())
        layout.initialize(width, height, collection)
        self.assertTrue(layout.isInitialized())

        copy = layout.copy()
        self.assertTrue(layout.isSameCoverage(copy))

        width = 5
        height = 5

        layout = LegoBrickLayout()
        self.assertFalse(layout.isInitialized())
        layout.initialize(width, height, collection)
        self.assertFalse(layout.isSameCoverage(copy))

    def __createBrickCollection(self, area: int) -> LegoBrickCollection:
        bricks = []
        bricks.append(LegoBrick(2, 1))
        bricks.append(LegoBrick(1, 2))
        bricks.append(LegoBrick(2, 2))
        collection = LegoBrickCollection()
        collection.initialize(area, bricks, uniform=False)
        return collection


if __name__ == '__main__':
    unittest.main()
