# layout.py

import math
from typing import List, Tuple

import numpy as np
import random

from lego.brick import LegoBrick
from lego.collection import LegoBrickCollection
from lego.exceptions import NotInitializedException


class LegoBrickLayout(object):
    """
    A class used to represent a Layout of LegoBrick which cover an area.
    An instance of this class must be initialized before use, by calling the method initialize().
    Using of this instance methods before initialization may raise a NotInitializedException.

    Methods
    -------
    initialize( width: int, height: int, brickCollection: LegoBrickCollection):
        LegoBrickLayout instance initialization.
        This function should be called once, more calls will be meaningless.
    isInitialized() -> bool:
        Gets the initialization state of the instance.
    copy() -> LegoBrickLayout:
        Gets a LegoBrickLayout instance with the same attributes.
    getAreaMatrix() -> np.ndarray:
        Gets a matrix which represents the cover of the layer.
    getAreaBricks() -> List[Tuple[int, int, LegoBrick]]:
        Gets a list of all the bricks in the layer and their location on the layer.
    getCoveredArea() -> int:
        Gets the number of the covered cells in the matrix.
    getWidth() -> int:
        Gets the width of the layer.
    getHeight() -> int:
        Gets the width of the layer.
    validateLayer():
        Validate the layer after changes from outside.
    isSameCoverage(otherLayout: LegoBrickLayout) -> bool:
        Check if the received layer has exactly the same coverage.
    """

    def __init__(self):
        self.__initialized = False

    def initialize(self, width: int, height: int,
                   brickCollection: LegoBrickCollection):
        """
        LegoBrickLayout instance initialization.
        This function should be called once, more calls will be meaningless.

        Parameters
        ----------
        width : int
            The brick width.
        height : int
            The brick height.
        brickCollection : LegoBrickCollection
            An collection of bricks to create the layer

        Raises
        ------
        ValueError
            If the width or the height isn't bigger then 0.
        TypeError
            If the List[LegoBrick] is None
        """

        if self.__initialized:
            return

        if width < 1:
            raise ValueError("width must be bigger then 1!")
        self.__width = width
        if height < 1:
            raise ValueError("height must be bigger then 1!")
        self.__height = height
        if brickCollection is None:
            raise TypeError("brick collection is none!")
        if not brickCollection.isInitialized():
            raise NotInitializedException(
                "Received brick collection not initialized!")

        self.__brickCollection = brickCollection.copy()
        self.__layout = []
        self.__coveredArea = 0
        self.__area = np.zeros((width, height), dtype=np.int32)

        if self.__brickCollection.getAmountOfAvailableBricks() != 0:
            self.__createRandomLayout()

        self.__initialized = True

    def __createRandomLayout(self):
        # TODO ROMAN: Gives too "good" coverage, probably unnecessary and should be deleted.
        # numberOfAttempts = round(
        #     math.sqrt(self.__brickCollection.getNumberOfBricksTypes()))
        numberOfAttempts = 1
        for i in range(self.__width):
            for j in range(self.__height):
                if self.__brickCollection.getAmountOfAvailableBricks() == 0:
                    # the bricks collection is empty
                    return
                if self.__area[i][j] != 0:
                    continue
                for _ in range(numberOfAttempts):
                    firstVertical = bool(random.getrandbits(1))
                    selectedBrick = self.__brickCollection.getRandomBrick()
                    if self.__tryAdd(i, j, selectedBrick, firstVertical):
                        break
                    else:
                        self.__brickCollection.returnBrick(selectedBrick)

    def __tryAdd(self, row: int, column: int, brick: LegoBrick,
                 firstVertical: bool) -> bool:
        if firstVertical:
            if not self.__tryAddVertical(row, column, brick):
                return self.__tryAddHorizontal(row, column, brick)
        else:
            if not self.__tryAddHorizontal(row, column, brick):
                return self.__tryAddVertical(row, column, brick)

    def __tryAddHorizontal(self, row: int, column: int,
                           brick: LegoBrick) -> bool:
        if column + brick.getWidth() > self.__height or row + brick.getHeight(
        ) > self.__width:
            return False

        for i in range(row, row + brick.getHeight()):
            for j in range(column, column + brick.getWidth()):
                if self.__area[i][j] != 0:
                    return False

        self.__layout.append((row, column, brick))

        for i in range(row, row + brick.getHeight()):
            self.__area[i][column:column + brick.getWidth()] = brick.getId()

        self.__coveredArea += brick.getArea()
        return True

    def __tryAddVertical(self, row: int, column: int,
                         brick: LegoBrick) -> bool:
        if column + brick.getHeight() > self.__height or row + brick.getWidth(
        ) > self.__width:
            return False

        for i in range(row, row + brick.getWidth()):
            for j in range(column, column + brick.getHeight()):
                if self.__area[i][j] != 0:
                    return False

        self.__layout.append((row, column, brick))

        for i in range(row, row + brick.getWidth()):
            self.__area[i][column:column + brick.getHeight()] = brick.getId()

        self.__coveredArea += brick.getArea()
        return True

    def copy(self) -> object:
        """
        Gets a copy instance with the same attributes.

        Returns
        -------
        LegoBrickLayout:
            A LegoBrickLayout instance with the same attributes.
        """
        copy = LegoBrickLayout()
        if self.__initialized:
            copy.__width = self.__width
            copy.__height = self.__height
            copy.__area = self.__area.copy()
            copy.__coveredArea = self.__coveredArea
            copy.__layout = list(self.__layout)
            copy.__brickCollection = self.__brickCollection.copy()
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

    def getAreaMatrix(self) -> np.ndarray:
        """
        Gets a matrix which represents the cover of the layer.

        Returns
        -------
        np.ndarray
            matrix which represents the cover of the layer.

        Raises
        ------
        NotInitializedException
            If this method called before initialize() method
        """
        if not self.__initialized:
            raise NotInitializedException(
                "The instance used before calling initialize method")
        return self.__area

    def getAreaBricks(self) -> List[Tuple[int, int, LegoBrick]]:
        """
        Gets a list of all the bricks in the layer and their location on the layer.

        Returns
        -------
        List[Tuple[int, int, LegoBrick]]
            list of all the bricks in the layer and their location on the layer.

        Raises
        ------
        NotInitializedException
            If this method called before initialize() method
        """
        if not self.__initialized:
            raise NotInitializedException(
                "The instance used before calling initialize method")
        return self.__layout

    def getCoveredArea(self) -> int:
        """
        Gets the number of the covered cells in the matrix.

        Returns
        -------
        int
            number of the covered cells in the matrix.

        Raises
        ------
        NotInitializedException
            If this method called before initialize() method
        """
        if not self.__initialized:
            raise NotInitializedException(
                "The instance used before calling initialize method")
        return self.__coveredArea

    def getWidth(self) -> int:
        """
        Gets the width of the layer.

        Returns
        -------
        int
            width of the layer

        Raises
        ------
        NotInitializedException
            If this method called before initialize() method
        """
        if not self.__initialized:
            raise NotInitializedException(
                "The instance used before calling initialize method")
        return self.__width

    def getHeight(self) -> int:
        """
        Gets the width of the layer.

        Returns
        -------
        int
            width of the layer

        Raises
        ------
        NotInitializedException
            If this method called before initialize() method
        """
        if not self.__initialized:
            raise NotInitializedException(
                "The instance used before calling initialize method")
        return self.__height

    def validateLayer(self):
        """
        Validate the layer after changes from outside.

        Raises
        ------
        NotInitializedException
            If this method called before initialize() method
        """
        if not self.__initialized:
            raise NotInitializedException(
                "The instance used before calling initialize method")

        raise NotImplementedError("validateLayer not implemented yet!")

    def isSameCoverage(self, otherLayout) -> bool:
        """
        Check if the received layer has exactly the same coverage.

        Parameters
        ----------
        otherLayout : LegoBrickLayout
            The brick to check.

        Returns
        -------
        bool
            True if the two layers have the same coverage and false if haven't.

        Raises
        ------
        NotInitializedException
            If this method called before initialize() method
        """
        if not self.__initialized:
            raise NotInitializedException(
                "The instance used before calling initialize method")

        if otherLayout is None or type(self) != type(otherLayout):
            return False

        if self.__width != otherLayout.getWidth(
        ) or self.__height != otherLayout.getHeight() or len(
                self.__layout) != len(otherLayout.getAreaBricks()):
            return False

        otherArea = otherLayout.getAreaMatrix()
        for i in range(self.__width):
            for j in range(self.__height):
                if not ((self.__area[i][j] == 0 and otherArea[i][j] == 0) or
                        (self.__area[i][j] != 0 and otherArea[i][j] != 0)):
                    return False
        return True

    def __str__(self):
        return self.__toString()

    def __repr__(self):
        return self.__toString()

    def __toString(self) -> str:
        if not self.__initialized:
            return "LegoBrickLayout[Not initialized]"

        return "LegoBrickLayout[Covering %d from %d]" % (
            self.__coveredArea, self.__width * self.__height)
