# brick_test.py

import unittest

from lego.brick import LegoBrick


class LegoBrick_Test(unittest.TestCase):
    def test_wrongInitialization(self):
        throws = False
        try:
            LegoBrick(10, 0)
        except ValueError as e:
            throws = True
        self.assertTrue(
            throws,
            "LegoBrick constructor didn't throw ValueError on illegal paramter"
        )

        throws = False
        try:
            LegoBrick(0, 10)
        except ValueError as e:
            throws = True
        self.assertTrue(
            throws,
            "LegoBrick constructor didn't throw ValueError on illegal paramter"
        )

    def test_initialization(self):
        width = 5
        height = 5
        b = LegoBrick(width, height)
        self.assertEqual(b.getHeight(), height)
        self.assertEqual(b.getWidth(), width)
        self.assertEqual(b.getArea(), width * height)

    def test_setAttributes(self):
        height = 5
        b = LegoBrick(height, height)
        width = 10
        b.setWidth(width)
        self.assertEqual(b.getHeight(), height)
        self.assertEqual(b.getWidth(), width)
        self.assertEqual(b.getArea(), width * height)

    def test_copy(self):
        b = LegoBrick(5, 5)
        copy = b.copy()
        self.assertEqual(b.getHeight(), copy.getHeight())
        self.assertEqual(b.getWidth(), copy.getWidth())
        self.assertEqual(b.getArea(), copy.getArea())


if __name__ == '__main__':
    unittest.main()
