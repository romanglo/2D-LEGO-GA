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
            "LegoBrick constructor didn't throw ValueError on illegal parameter"
        )

        throws = False
        try:
            LegoBrick(0, 10)
        except ValueError as e:
            throws = True
        self.assertTrue(
            throws,
            "LegoBrick constructor didn't throw ValueError on illegal parameter"
        )

    def test_initialization(self):
        width = 5
        height = 5
        b = LegoBrick(width, height)
        self.assertEqual(b.getHeight(), height)
        self.assertEqual(b.getWidth(), width)
        self.assertEqual(b.getArea(), width * height)
        self.assertEqual(b.getId(), LegoBrick.NONE_ID)
        id = 13
        b = LegoBrick(width, height, id)
        self.assertEqual(b.getHeight(), height)
        self.assertEqual(b.getWidth(), width)
        self.assertEqual(b.getArea(), width * height)
        self.assertEqual(b.getId(), id)

    def test_setAttributes(self):
        height = 5
        b = LegoBrick(height, height)
        width = 10
        b.setWidth(width)
        self.assertEqual(b.getHeight(), height)
        self.assertEqual(b.getWidth(), width)
        self.assertEqual(b.getArea(), width * height)
        id = 13
        b.setId(id)
        self.assertEqual(b.getId(), id)

    def test_copy(self):
        b = LegoBrick(5, 5)
        copy = b.copy()
        self.assertEqual(b.getHeight(), copy.getHeight())
        self.assertEqual(b.getWidth(), copy.getWidth())
        self.assertEqual(b.getArea(), copy.getArea())
        self.assertEqual(b.getId(), copy.getId())

    def test_equals(self):
        b1 = LegoBrick(5, 5)
        b1copy = b1.copy()
        self.assertTrue(b1 == b1copy)
        b1copy.setId(b1.getId() + 10)
        self.assertFalse(b1 == b1copy)
        b2 = LegoBrick(10, 5)
        self.assertFalse(b2 == b1)


if __name__ == '__main__':
    unittest.main()
