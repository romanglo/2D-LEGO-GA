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

        collection = self.__createBrickCollection(width * height)
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
        width = 5
        height = 5

        collection = self.__createBrickCollection(width * height)
        layout = LegoBrickLayout()
        self.assertFalse(layout.isInitialized())
        layout.initialize(width, height, collection)
        self.assertTrue(layout.isInitialized())

        copy = layout.copy()
        self.assertTrue(layout.hasSameCoverage(copy))

        newWidth = 1
        newHeight = 1

        copy.getAreaBricks()[0][2].setWidth(newWidth)
        copy.getAreaBricks()[0][2].setHeight(newHeight)

        self.assertTrue(newWidth != layout.getAreaBricks()[0][2].getWidth())
        self.assertTrue(newHeight != layout.getAreaBricks()[0][2].getHeight())

        width = 5
        height = 5

        layout = LegoBrickLayout()
        self.assertFalse(layout.isInitialized())
        layout.initialize(width, height, collection)
        self.assertFalse(layout.hasSameCoverage(copy))

    def test_validate(self):
        width = 5
        height = 5
        layout = LegoBrickLayout()
        self.assertFalse(layout.isInitialized())
        collection = self.__createBrickCollection(width * height)
        layout.initialize(width, height, collection)
        copy = layout.copy()
        self.assertTrue(
            layout.hasSameCoverage(copy),
            "The coverage of the layout have to be the same")
        copyBricks = copy.getAreaBricks()
        copyOriginalWidth = copyBricks[0][2].getWidth()
        copyOriginalHeight = copyBricks[0][2].getHeight()
        copyBricks[0][2].setWidth(1)
        copyBricks[0][2].setHeight(1)
        self.assertTrue(copy.validateLayer(), "Validation failed!")
        self.assertFalse(layout.hasSameCoverage(
            copy)), "Tho coverage of the layout have to be different"
        copyBricks[0][2].setWidth(copyOriginalWidth)
        copyBricks[0][2].setHeight(copyOriginalHeight)
        self.assertTrue(copy.validateLayer(), "Validation failed!")
        self.assertTrue(
            layout.hasSameCoverage(copy),
            "The coverage of the layout have to be the same")

    def __createBrickCollection(self, area: int) -> LegoBrickCollection:
        bricks = []
        bricks.append(LegoBrick(2, 3))
        bricks.append(LegoBrick(3, 2))
        bricks.append(LegoBrick(2, 2))
        collection = LegoBrickCollection()
        collection.initialize(area, bricks, uniform=True)
        return collection


if __name__ == '__main__':
    unittest.main()
