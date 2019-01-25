from typing import Dict, List, Optional, Set, Tuple

import numpy


class LegoBrick(object):
    """
    A class used to represent a Lego brick.

    Methods
    -------
    setWidth(width: int)
        Sets the width of the Lego brick.
    getWidth() -> int:
        Gets the width of the LEGO brick.
    setHeight(height: int)
        Sets the height of the Lego brick.
    getHeight() -> int:
        Gets the height of the LEGO brick.
    getArea(self) -> int:
        Gets the area of the LEGO brick,
        area calculation is with width * height.
    copy(self) -> LegoBrick :
        Gets a LegoBrick instance with the same attributes.
    """

    def __init__(self, width: int, height: int):
        """
        LegoBrick constuctor.

        Parameters
        ----------
        width : int
            The brick width.
        height : int
            The brick height.

        Raises
        ------
        ValueError
            If the width or the height isn't bigger then 0.
        """
        self.setWidth(width)
        self.setHeight(height)

    def setWidth(self, width: int):
        """
        Sets the width of the Lego brick.

        Parameters
        ----------
        width : int
            The brick width.

        Raises
        ------
        ValueError
            If the width isn't bigger then 0.
        """
        if (width < 1):
            raise ValueError("width must be bigger then 1!")
        self.__width = width

    def getWidth(self) -> int:
        """
        Gets the width of the LEGO brick.

        Returns
        -------
        int
            the width of the LEGO brick.
        """
        return self.__width

    def setHeight(self, height: int):
        """
        Sets the height of the Lego brick.

        Parameters
        ----------
        height : int
            The brick width.

        Raises
        ------
        ValueError
            If the height isn't bigger then 0.
        """
        if (height < 1):
            raise ValueError("height must be bigger then 1!")
        self.__height = height

    def getHeight(self) -> int:
        """
        Gets the height of the LEGO brick.

        Returns
        -------
        int
            the height of the LEGO brick.
        """
        return self.__height

    def getArea(self) -> int:
        """
        Gets the area of the LEGO brick,
        area calculation is with width * height.

        Returns
        -------
        int
            the area of the LEGO brick.
        """
        return self.__height * self.__width

    def copy(self):
        """
        Gets a LegoBrick instance with the same attributes.

        Returns
        -------
        LegoBrick
            copied instance.
        """
        return LegoBrick(self.__width, self.__height)

    def __str__(self):
        return self.__toString()

    def __repr__(self):
        return self.__toString()

    def __toString(self) -> str:
        return "LegoBrick[width=%d, height=%d, area=%d]" % (
            self.getWidth(), self.getHeight(), self.getArea())


class LegoBrickCollection(object):
    """
    A class used to represent a Collection of LegoBrick which select enough bricks to cover an area.

    Methods
    -------
    getRandomBrick(self) -> LegoBrick:
        Gets a random brick from the collection.
    getAmountOfAvailableBricks(self) -> int:
        Gets the amount of available bricks
    """

    def __init__(self,
                 area: int,
                 bricks: List[LegoBrick],
                 uniform: bool = True):
        """
        LegoBrickCollection constuctor.

        Parameters
        ----------
        area : int
            The area to cover.
        bricks : List[LegoBrick]
            List of bricks to create the collection.
        uniform : bool
            If true the selection of bricks will keep uniform probabilty.
        Raises
        ------
        ValueError
            If the area isn't bigger then 0.
        """
        if (area < 1):
            raise ValueError("Area must be bigger then 1!")
        if (len(bricks) == 0):
            self.__amountOfAvailableBricks = 0
            return

        bricks.sort(key=lambda x: x.getArea())
        self.__brickTypes = list(bricks)

        areaSum = numpy.sum([brick.getArea() for brick in bricks])
        probabilities = []
        for brick in bricks:
            probabilities.append(brick.getArea() / areaSum)
        self.__probabilities = probabilities

        availableBricks = [0] * len(bricks)
        if (uniform):
            currentArea = 0
            i = 0
            while (currentArea < area):
                availableBricks[i] += 1
                currentArea += bricks[i].getArea()
                i += 1
                if (i == len(bricks)):
                    i = 0
        else:
            currentArea = 0
            while (currentArea < area):
                selectedBrick = numpy.random.choice(
                    bricks, 1, replace=False, p=probabilities)[0]
                selectedBrickIndex = bricks.index(selectedBrick)
                availableBricks[selectedBrickIndex] += 1
                currentArea += selectedBrick.getArea()

        self.__startBricks = list(availableBricks)
        self.__availableBricks = availableBricks
        self.__amountOfAvailableBricks = sum(availableBricks)

    def getRandomBrick(self) -> LegoBrick:
        """
        Gets a random brick from the collection.

        Returns
        -------
        LegoBrick
            selected brick.
        """
        if self.__amountOfAvailableBricks == 0:
            return None
        while True:
            selectedBrick = numpy.random.choice(
                self.__brickTypes, 1, replace=False, p=self.__probabilities)[0]
            index = self.__brickTypes.index(selectedBrick)
            if self.__availableBricks[index] != 0:
                self.__availableBricks[index] -= 1
                self.__amountOfAvailableBricks -= 1
                return self.__brickTypes[index].copy()

    def getAmountOfAvailableBricks(self) -> int:
        """
        Gets the amount of available bricks

        Returns
        -------
        int
            The amount of available bricks
        """
        return self.__amountOfAvailableBricks

    def __str__(self):
        return self.__toString()

    def __repr__(self):
        return self.__toString()

    def __toString(self) -> str:
        return "LegoBrickCollection[BricksTypes=%s,\nStartBricks=%s,\nAvailableBricks=%s]" % (
            str(self.__brickTypes), str(self.__startBricks),
            str(self.__availableBricks))
