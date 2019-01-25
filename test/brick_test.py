# brick_test.py

import unittest

from lego import brick


class LegoBrick_Test(unittest.TestCase):
    def test_wrongInitialization(self):
        throws = False
        try:
            brick.LegoBrick(10, 0)
        except ValueError as e:
            throws = True
        self.assertTrue(
            throws,
            "LegoBrick constructor didn't throw ValueError on illegal paramter"
        )

        throws = False
        try:
            brick.LegoBrick(0, 10)
        except ValueError as e:
            throws = True
        self.assertTrue(
            throws,
            "LegoBrick constructor didn't throw ValueError on illegal paramter"
        )

    def test_initialization(self):
        width = 5
        height = 5
        b = brick.LegoBrick(width, height)
        self.assertEqual(b.getHeight(), height)
        self.assertEqual(b.getWidth(), width)
        self.assertEqual(b.getArea(), width * height)

    def test_setAttributes(self):
        height = 5
        b = brick.LegoBrick(height, height)
        width = 10
        b.setWidth(width)
        self.assertEqual(b.getHeight(), height)
        self.assertEqual(b.getWidth(), width)
        self.assertEqual(b.getArea(), width * height)

    def test_copy(self):
        b = brick.LegoBrick(5, 5)
        copy = b.copy()
        self.assertEqual(b.getHeight(), copy.getHeight())
        self.assertEqual(b.getWidth(), copy.getWidth())
        self.assertEqual(b.getArea(), copy.getArea())


class LegoBrickCollection_Test(unittest.TestCase):
    def test_wrongInitialization(self):
        throws = False
        try:
            brick.LegoBrickCollection(0, [])
        except ValueError as e:
            throws = True
        self.assertTrue(
            throws,
            "LegoBrickCollection constructor didn't throw ValueError on illegal paramter"
        )

    def test_initialization(self):

        try:
            brick.LegoBrickCollection(10, [])
        except Exception as e:
            self.fail(
                "LegoBrickCollection constructor raise exception on unexpected place"
            )

        try:
            brick.LegoBrickCollection(50, list([brick.LegoBrick(1, 1)]))
        except Exception as e:
            self.fail(
                "LegoBrickCollection constructor raise exception on unexpected place"
            )

    def test_emptyCollection(self):
        col = brick.LegoBrickCollection(10, [])
        self.assertEqual(col.getAmountOfAvailableBricks(), 0)
        rnd = col.getRandomBrick()
        self.assertIsNone(rnd)

    def test_uniformCollection(self):
        col = brick.LegoBrickCollection(5, list([brick.LegoBrick(1, 1)]), True)
        amount = col.getAmountOfAvailableBricks()
        while amount != 0:
            rnd = col.getRandomBrick()
            self.assertIsNotNone(rnd)
            amount -= 1
        self.assertEqual(amount, col.getAmountOfAvailableBricks())
        rnd = col.getRandomBrick()
        self.assertIsNone(rnd)

    def test_nonUniformCollection(self):
        col = brick.LegoBrickCollection(5, list([brick.LegoBrick(1, 1)]),
                                        False)
        amount = col.getAmountOfAvailableBricks()
        while amount != 0:
            rnd = col.getRandomBrick()
            self.assertIsNotNone(rnd)
            amount -= 1
        self.assertEqual(amount, col.getAmountOfAvailableBricks())
        rnd = col.getRandomBrick()
        self.assertIsNone(rnd)


if __name__ == '__main__':
    unittest.main()
