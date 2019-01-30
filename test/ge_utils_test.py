# brick_test.py

import unittest

import lego.ga_utils as GaUtils
from lego.brick import LegoBrick
from lego.collection import LegoBrickCollection
from lego.layout import LegoBrickLayout


class GaUtils_Test(unittest.TestCase):
    def test_addMutation(self):
        layout = self.__createBrickLayout(5, 5)
        copy = layout.copy()
        sizeBeforeMutation = len(layout.getAreaBricks())
        if GaUtils.addMutation(layout):
            self.assertEqual(sizeBeforeMutation + 1,
                             len(layout.getAreaBricks()))
            self.assertFalse(copy.hasSameCoverage(layout))
        else:
            self.assertEqual(sizeBeforeMutation, len(layout.getAreaBricks()))
            self.assertTrue(copy.hasSameCoverage(layout))

    def test_removeMutation(self):
        layout = self.__createBrickLayout(5, 5)
        copy = layout.copy()
        sizeBeforeMutation = len(layout.getAreaBricks())
        if GaUtils.removeMutation(layout):
            self.assertEqual(sizeBeforeMutation - 1,
                             len(layout.getAreaBricks()))
            self.assertFalse(copy.hasSameCoverage(layout))
        else:
            self.assertEqual(sizeBeforeMutation, len(layout.getAreaBricks()))
            self.assertTrue(copy.hasSameCoverage(layout))

    def __createBrickLayout(self, width: int, height: int) -> LegoBrickLayout:
        bricks = []
        bricks.append(LegoBrick(1, 1))
        bricks.append(LegoBrick(1, 2))
        bricks.append(LegoBrick(2, 2))
        collection = LegoBrickCollection()
        collection.initialize(width * height, bricks, uniform=True)
        self.assertTrue(collection.isInitialized())
        layout = LegoBrickLayout()
        layout.initialize(width, height, collection)
        self.assertTrue(layout.isInitialized())
        return layout


if __name__ == '__main__':
    unittest.main()
