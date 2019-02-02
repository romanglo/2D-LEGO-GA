# brick_test.py

import unittest

import lego.ga_utils as GaUtils
from lego.brick import LegoBrick
from lego.collection import LegoBrickCollection
from lego.layout import LegoBrickLayout


class GaUtils_Test(unittest.TestCase):

    __manyTestValue = 10

    def test_moveMutation(self):
        layout = self.__createBrickLayout(5, 5)
        copy = layout.copy()
        sizeBeforeMutation = len(layout.getAreaBricks())
        if GaUtils.moveMutation(layout):
            self.assertFalse(
                copy.hasSameCoverage(layout),
                "Coverage should be different after move mutation")
        else:
            self.assertTrue(
                copy.hasSameCoverage(layout),
                "Coverage should be the same if move mutation failed")

        self.assertEqual(sizeBeforeMutation, len(layout.getAreaBricks()))

    def test_manyMoveMutation(self):
        for _ in range(GaUtils_Test.__manyTestValue):
            self.test_moveMutation()

    def test_changeMutation(self):
        layout = self.__createBrickLayout(5, 5)
        copy = layout.copy()
        sizeBeforeMutation = len(layout.getAreaBricks())
        if GaUtils.changeMutation(layout):
            self.assertFalse(
                copy.hasSameCoverage(layout),
                "Coverage should be different after change mutation")
        else:
            self.assertTrue(
                copy.hasSameCoverage(layout),
                "Coverage should be the same if change mutation failed")

        self.assertEqual(sizeBeforeMutation, len(layout.getAreaBricks()))

    def test_manyChangeMutation(self):
        for _ in range(GaUtils_Test.__manyTestValue):
            self.test_changeMutation()

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

    def test_manyAddMutation(self):
        for _ in range(GaUtils_Test.__manyTestValue):
            self.test_addMutation()

    def test_removeMutation(self):
        layout = self.__createBrickLayout(5, 5)
        copy = layout.copy()
        sizeBeforeMutation = len(layout.getAreaBricks())
        collectionAmountBeforeMutation = layout.getCollection(
        ).getAmountOfAvailableBricks()
        if GaUtils.removeMutation(layout):
            self.assertEqual(sizeBeforeMutation - 1,
                             len(layout.getAreaBricks()))
            self.assertEqual(
                collectionAmountBeforeMutation + 1,
                layout.getCollection().getAmountOfAvailableBricks())
            self.assertFalse(copy.hasSameCoverage(layout))
        else:
            self.assertEqual(sizeBeforeMutation, len(layout.getAreaBricks()))
            self.assertEqual(
                collectionAmountBeforeMutation,
                layout.getCollection().getAmountOfAvailableBricks())
            self.assertTrue(copy.hasSameCoverage(layout))

    def test_manyRemoveMutation(self):
        for _ in range(GaUtils_Test.__manyTestValue):
            self.test_removeMutation()

    def test_crossover(self):
        width = 5
        height = 5
        collection = LegoBrickCollection()
        collection.initialize(width * height, [LegoBrick(1, 1)], uniform=True)
        self.assertTrue(collection.isInitialized())
        layout = LegoBrickLayout()
        layout.initialize(width, height, collection)
        self.assertTrue(layout.isInitialized())
        copy = layout.copy()
        children = GaUtils.crossover(layout, copy)

    def test_crossAndConstraints(self):
        width = 5
        height = 5
        collection = LegoBrickCollection()
        collection.initialize(width * height, [LegoBrick(1, 1)], uniform=True)
        self.assertTrue(collection.isInitialized())
        layout = LegoBrickLayout()
        layout.initialize(width, height, collection)
        self.assertTrue(layout.isInitialized())
        xRange = [1, 3]
        yRange = [1, 3]
        cross, constraint = GaUtils.VisibilityForTests_getCrossAndConstraints(
            xRange, yRange, layout)
        expectedSize = (xRange[1] - xRange[0] + 1) * (
            yRange[1] - yRange[0] + 1)
        self.assertEqual(len(cross), expectedSize)
        self.assertEqual(len(constraint), 0)

        copyCross = list(cross)
        copyConstraint = list(constraint)

        GaUtils.VisibilityForTests_validateCrossData(cross, constraint,
                                                     copyCross, copyConstraint)
        self.assertEqual(len(cross), expectedSize)
        self.assertEqual(len(constraint), 0)
        self.assertEqual(len(copyCross), expectedSize)
        self.assertEqual(len(copyConstraint), 0)
        self.assertEqual(cross, copyCross)
        self.assertEqual(constraint, copyConstraint)

    def test_crossAndConstraints3(self):
        width = 5
        height = 5
        collection = LegoBrickCollection()
        collection.initialize(width * height, [LegoBrick(2, 2)], uniform=True)
        self.assertTrue(collection.isInitialized())
        layout = LegoBrickLayout()
        layout.initialize(width, height, collection)
        self.assertTrue(layout.isInitialized())
        xRange = [0, 1]
        yRange = [0, 1]
        cross, constraint = GaUtils.VisibilityForTests_getCrossAndConstraints(
            xRange, yRange, layout)
        self.assertEqual(len(cross), 1)
        self.assertEqual(len(constraint), 0)
        xRange = [2, 3]
        yRange = [2, 3]
        cross, constraint = GaUtils.VisibilityForTests_getCrossAndConstraints(
            xRange, yRange, layout)
        self.assertEqual(len(cross), 1)
        self.assertEqual(len(constraint), 0)

    def test_crossAndConstraints2(self):
        width = 5
        height = 5
        xRange = [1, 3]
        yRange = [1, 3]

        collection = LegoBrickCollection()
        collection.initialize(
            width * height, [LegoBrick(1, 1), LegoBrick(2, 2)], uniform=True)
        self.assertTrue(collection.isInitialized())
        layout = LegoBrickLayout()
        layout.initialize(width, height, collection)
        self.assertTrue(layout.isInitialized())

        cross, constraint = GaUtils.VisibilityForTests_getCrossAndConstraints(
            xRange, yRange, layout)

        collection2 = LegoBrickCollection()
        collection2.initialize(width * height, [LegoBrick(1, 1)], uniform=True)
        self.assertTrue(collection2.isInitialized())
        layout2 = LegoBrickLayout()
        layout2.initialize(width, height, collection2)
        self.assertTrue(layout2.isInitialized())
        cross2, constraint2 = GaUtils.VisibilityForTests_getCrossAndConstraints(
            xRange, yRange, layout2)

        expectedSize = (xRange[1] - xRange[0] + 1) * (
            yRange[1] - yRange[0] + 1)
        self.assertEqual(len(cross2), expectedSize)
        self.assertEqual(len(constraint2), 0)

        GaUtils.VisibilityForTests_validateCrossData(cross, constraint, cross2,
                                                     constraint2)
        self.assertEqual(len(cross), expectedSize)

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
