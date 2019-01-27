# brick_test.py

import unittest

from lego.brick import LegoBrick
from lego.collection import LegoBrickCollection
from lego.exceptions import NotInitializedException


class LegoBrickCollection_Test(unittest.TestCase):
    def test_wrongInitialization(self):
        throws = False
        try:
            col = LegoBrickCollection()
            col.initialize(0, [])
        except ValueError as e:
            throws = True
        self.assertTrue(
            throws,
            "LegoBrickCollection constructor didn't throw ValueError on illegal parameter"
        )

        throws = False
        try:
            col = LegoBrickCollection()
            col.initialize(10, None)
        except TypeError as e:
            throws = True
        self.assertTrue(
            throws,
            "LegoBrickCollection constructor didn't throw TypeError on illegal parameter"
        )

    def test_initialization(self):
        col = LegoBrickCollection()
        self.assertFalse(col.isInitialized())

        try:
            col.initialize(10, [])
        except Exception as e:
            self.fail(
                "LegoBrickCollection constructor raise exception on unexpected place"
            )
        self.assertTrue(col.isInitialized())

        col = LegoBrickCollection()
        self.assertFalse(col.isInitialized())
        try:
            col.initialize(50, list([LegoBrick(1, 1)]))
        except Exception as e:
            self.fail(
                "LegoBrickCollection constructor raise exception on unexpected place"
            )
        self.assertTrue(col.isInitialized())

    def test_emptyCollection(self):
        col = LegoBrickCollection()
        col.initialize(10, [])
        self.assertEqual(col.getAmountOfAvailableBricks(), 0)
        rnd = col.getRandomBrick()
        self.assertIsNone(rnd)

    def test_uniformCollection(self):
        col = LegoBrickCollection()
        col.initialize(5, list([LegoBrick(1, 1)]), True)
        amount = col.getAmountOfAvailableBricks()
        while amount != 0:
            rnd = col.getRandomBrick()
            self.assertIsNotNone(rnd)
            amount -= 1
        self.assertEqual(amount, col.getAmountOfAvailableBricks())
        rnd = col.getRandomBrick()
        self.assertIsNone(rnd)

    def test_nonUniformCollection(self):
        col = LegoBrickCollection()
        col.initialize(10, list([LegoBrick(1, 1), LegoBrick(1, 2)]), False)
        amount = col.getAmountOfAvailableBricks()
        while amount != 0:
            rnd = col.getRandomBrick()
            self.assertIsNotNone(rnd)
            amount -= 1
        self.assertEqual(amount, col.getAmountOfAvailableBricks())
        rnd = col.getRandomBrick()
        self.assertIsNone(rnd)

    def test_notInitializeExceptions(self):
        col = LegoBrickCollection()
        throws = False
        try:
            col.getAmountOfAvailableBricks()
        except NotInitializedException as e:
            throws = True
        self.assertTrue(
            throws,
            "LegoBrickCollection.getAmountOfAvailableBricks() didn't throw NotInitializedException after calling method before initialization"
        )

        throws = False
        try:
            col.getNumberOfBricksTypes()
        except NotInitializedException as e:
            throws = True
        self.assertTrue(
            throws,
            "LegoBrickCollection.getNumberOfBricksTypes() didn't throw NotInitializedException after calling method before initialization"
        )

        throws = False
        try:
            col.getRandomBrick()
        except NotInitializedException as e:
            throws = True
        self.assertTrue(
            throws,
            "LegoBrickCollection.getRandomBrick() didn't throw NotInitializedException after calling method before initialization"
        )

        throws = False
        try:
            col.getBrick(1, 1)
        except NotInitializedException as e:
            throws = True
        self.assertTrue(
            throws,
            "LegoBrickCollection.getBrick() didn't throw NotInitializedException after calling method before initialization"
        )

        throws = False
        try:
            col.returnBrick(LegoBrick(1, 1))
        except NotInitializedException as e:
            throws = True
        self.assertTrue(
            throws,
            "LegoBrickCollection.returnBrick() didn't throw NotInitializedException after calling method before initialization"
        )

    def test_copy(self):
        col = LegoBrickCollection()
        colCopy = col.copy()
        self.assertEqual(col.isInitialized(), colCopy.isInitialized())
        col.initialize(5, list([LegoBrick(1, 1)]), False)
        colCopy = col.copy()
        self.assertEqual(col.isInitialized(), colCopy.isInitialized())
        self.assertEqual(col.getAmountOfAvailableBricks(),
                         colCopy.getAmountOfAvailableBricks())

    def test_randomBrickId(self):
        col = LegoBrickCollection()
        col.initialize(5, list([LegoBrick(1, 1)]))
        colCopy = col.copy()
        self.assertNotEqual(col.getRandomBrick().getId(),
                            colCopy.getRandomBrick().getId())
        self.assertEqual(col.getRandomBrick().getId() + 1,
                         colCopy.getRandomBrick().getId())
        self.assertEqual(colCopy.getRandomBrick().getId() + 1,
                         col.getRandomBrick().getId())

    def test_getSpecificBrick(self):
        col = LegoBrickCollection()
        col.initialize(10, list([LegoBrick(1, 1)]))
        self.assertIsNotNone(col.getBrick(1, 1))
        self.assertIsNone(col.getBrick(2, 1))

    def test_returnBrick(self):
        col = LegoBrickCollection()
        col.initialize(10, list([LegoBrick(1, 1)]))
        b = col.getRandomBrick()
        self.assertFalse(col.returnBrick(LegoBrick(1, 1)))
        self.assertTrue(col.returnBrick(b))
        self.assertFalse(col.returnBrick(b))

    def test_numberOfBricksTypes(self):
        bricks = list([LegoBrick(1, 1)])
        col = LegoBrickCollection()
        col.initialize(10, bricks)
        self.assertEqual(col.getNumberOfBricksTypes(), len(bricks))
        col = LegoBrickCollection()
        col.initialize(10, [])
        self.assertEqual(col.getNumberOfBricksTypes(), 0)

    def test_amountOfBricks(self):
        bricks = list([LegoBrick(1, 1)])
        col = LegoBrickCollection()
        col.initialize(10, bricks)
        startAmount = col.getAmountOfAvailableBricks()
        rndBrick = col.getRandomBrick()
        self.assertEqual(col.getAmountOfAvailableBricks(), startAmount - 1)
        col.returnBrick(LegoBrick(12, 12))
        self.assertEqual(col.getAmountOfAvailableBricks(), startAmount - 1)
        col.returnBrick(rndBrick)
        self.assertEqual(col.getAmountOfAvailableBricks(), startAmount)


if __name__ == '__main__':
    unittest.main()
