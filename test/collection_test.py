# brick_test.py

import unittest

from lego.brick import LegoBrick
from lego.collection import LegoBrickCollection
from lego.execptions import NotInitializedException


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
            "LegoBrickCollection constructor didn't throw ValueError on illegal paramter"
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
        col.initialize(5, list([LegoBrick(1, 1)]), False)
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
            col.getRandomBrick()
        except NotInitializedException as e:
            throws = True
        self.assertTrue(
            throws,
            "LegoBrickCollection.getRandomBrick() didn't throw NotInitializedException after calling method before initialization"
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


if __name__ == '__main__':
    unittest.main()
