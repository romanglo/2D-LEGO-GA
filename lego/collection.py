from typing import List

import numpy

from lego.brick import LegoBrick
from lego.execptions import NotInitializedException


class LegoBrickCollection(object):
    """
    A class used to represent a Collection of LegoBrick which select enough bricks to cover an area.
    An instance of this class must be initialized before use, by calling the method initialize().
    Using of this instance methods before initialization may raise a NotInitializedException.

    Methods
    -------
    initialize(area: int, bricks: List[LegoBrick], uniform: bool = True):
        LegoBrickCollection instance initialization.
        This function should be called once, more calls will be meaningless.
    isInitialized() -> bool:
        Gets the initialization state of the instance.
    copy() -> LegoBrickCollection:
        Gets a LegoBrickCollection instance with the same attributes.
    getRandomBrick() -> LegoBrick:
        Gets a random brick from the collection.
    getBrick(width: int, height: int) -> LegoBrick:
        Gets a specific size brick from the collection if it available.
    returnBrick(brick: LegoBrick) -> bool:
        Returns a brick to the collection.
    getAmountOfAvailableBricks() -> int:
        Gets the amount of available bricks
    """

    __next_brick_id = 1

    def __init__(self):
        self.__initialized = False

    def initialize(self,
                   area: int,
                   bricks: List[LegoBrick],
                   uniform: bool = True):
        """
        LegoBrickCollection instance initialization.
        This function should be called once, more calls will be meaningless.

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

        if self.__initialized:
            return

        if (area < 1):
            raise ValueError("Area must be bigger then 1!")
        if (len(bricks) == 0):
            self.__amountOfAvailableBricks = 0
            self.__initialized = True
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
        self.__generatedBricks = []
        self.__initialized = True

    def getRandomBrick(self) -> LegoBrick:
        """
        Gets a random brick from the collection.

        Returns
        -------
        LegoBrick
            random brick if the collection doesn't empty, None if empty.

        Raises
        ------
        NotInitializedException
            If this method called before initialize() method
        """
        if not self.__initialized:
            raise NotInitializedException(
                "The instance used before calling initialize method")

        if self.__amountOfAvailableBricks == 0:
            return None
        while True:
            selectedBrick = numpy.random.choice(
                self.__brickTypes, 1, replace=False, p=self.__probabilities)[0]
            index = self.__brickTypes.index(selectedBrick)
            if self.__availableBricks[index] != 0:
                self.__availableBricks[index] -= 1
                self.__amountOfAvailableBricks -= 1
                copied = self.__brickTypes[index].copy()
                copied.setId(LegoBrickCollection.__next_brick_id)
                self.__generatedBricks.append(copied)
                LegoBrickCollection.__next_brick_id += 1
                return copied

    def getBrick(self, width: int, height: int) -> LegoBrick:
        """
        Gets a specific size brick from the collection if it available.

        Returns
        -------
        LegoBrick
            requested brick if available or None if didn't.

        Raises
        ------
        NotInitializedException
            If this method called before initialize() method
        """
        if not self.__initialized:
            raise NotInitializedException(
                "The instance used before calling initialize method")

        if self.__amountOfAvailableBricks == 0:
            return None

        for i in range(len(self.__brickTypes)):
            brick = self.__brickTypes[i]
            if brick.getWidth() == width and brick.getHeight() == height:
                if (self.__availableBricks[i] < 1):
                    return None
                self.__availableBricks[i] -= 1
                copied = brick.copy()
                copied.setId(LegoBrickCollection.__next_brick_id)
                self.__generatedBricks.append(copied)
                LegoBrickCollection.__next_brick_id += 1
                return copied

        return None

    def returnBrick(self, brick: LegoBrick) -> bool:
        """
        Returns a brick to the collection.

        Returns
        -------
        bool
            True if the brick belong to the collection and returned, and false if doesn't.

        Raises
        ------
        NotInitializedException
            If this method called before initialize() method
        """
        if not self.__initialized:
            raise NotInitializedException(
                "The instance used before calling initialize method")

        if brick in self.__generatedBricks:
            self.__generatedBricks.remove(brick)
            return True

        return False

    def getAmountOfAvailableBricks(self) -> int:
        """
        Gets the amount of available bricks

        Returns
        -------
        int
            The amount of available bricks

        Raises
        ------
        NotInitializedException
            If this method called before initialize() method
        """
        if not self.__initialized:
            raise NotInitializedException(
                "The instance used before calling initialize method")
        return self.__amountOfAvailableBricks

    def copy(self) -> object:
        """
        Gets a copy instance with the same attributes.

        Returns
        -------
        LegoBrickCollection:
            A LegoBrickCollection instance with the same attributes.
        """
        copy = LegoBrickCollection()
        if self.__initialized:
            copy.__amountOfAvailableBricks = self.__amountOfAvailableBricks
            copy.__availableBricks = list(self.__availableBricks)
            copy.__brickTypes = list(self.__brickTypes)
            copy.__startBricks = list(self.__startBricks)
            copy.__probabilities = list(self.__probabilities)
            copy.__generatedBricks = list(self.__generatedBricks)
            copy.__initialized = True
        return copy

    def isInitialized(self) -> bool:
        """
        Gets the initialization state of the instance

        Returns
        -------
        bool
            True if the instance is initialized and False if doesn't.
        """
        return self.__initialized

    def __str__(self):
        return self.__toString()

    def __repr__(self):
        return self.__toString()

    def __toString(self) -> str:
        if not self.__initialized:
            return "LegoBrickCollection[Not initialized]"

        return "LegoBrickCollection[BricksTypes=%s,\nStartBricks=%s,\nAvailableBricks=%s,\nGeneratedBricks=%s]" % (
            str(self.__brickTypes), str(self.__startBricks),
            str(self.__availableBricks), str(self.__generatedBricks))
