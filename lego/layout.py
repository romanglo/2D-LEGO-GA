# layout.py

import math
import random
from enum import Enum
from typing import List, Tuple

import numpy as np

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
    initialize(width: int, height: int, brickCollection: LegoBrickCollection):
        LegoBrickLayout instance initialization.
        This function should be called once, more calls will be meaningless.
    isInitialized() -> bool:
        Gets the initialization state of the instance.
    copy() -> LegoBrickLayout:
        Gets a LegoBrickLayout instance with the same attributes.
    getCollection() -> LegoBrickCollection:
        Gets the layer brick collection.
    getAreaMatrix() -> np.ndarray:
        Gets a matrix which represents the cover of the layer.
    getAreaBricks() -> List[Tuple[int, int, LegoBrick, LegoBrickLayout.Orientation]]:
        Gets a list of all the bricks in the layer and their location on the layer.
    getCoveredArea() -> int:
        Gets the number of the covered cells in the matrix.
    getWidth() -> int:
        Gets the width of the layer.
    getHeight() -> int:
        Gets the width of the layer.
    validateLayer():
        Validate the layer after changes from outside.
    def tryAddBrick(row: int, column: int, brick: LegoBrick, orientation: LegoBrickLayout.Orientation = None) -> bool:
        Try to add the received brick to a specific place at the layer.
    isSameCoverage(otherLayout: LegoBrickLayout) -> bool:
        Check if the received layer has exactly the same coverage.
    """

    class Orientation(Enum):
        VERTICAL = 1
        HORIZONTAL = 2

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
        self.__layout.sort(key=lambda brickPos: (brickPos[0], brickPos[1]))

    def __tryAdd(self, row: int, column: int, brick: LegoBrick,
                 firstVertical: bool) -> bool:
        if firstVertical:
            if not self.__tryAddVertical(row, column, brick):
                return self.__tryAddHorizontal(row, column, brick)
            else:
                return True
        else:
            if not self.__tryAddHorizontal(row, column, brick):
                return self.__tryAddVertical(row, column, brick)
            else:
                return True

    def __tryAddHorizontal(self, row: int, column: int,
                           brick: LegoBrick) -> bool:
        if column + brick.getWidth() > self.__height or row + brick.getHeight(
        ) > self.__width:
            return False

        for i in range(row, row + brick.getHeight()):
            for j in range(column, column + brick.getWidth()):
                if self.__area[i][j] != 0:
                    return False

        self.__layout.append((row, column, brick,
                              LegoBrickLayout.Orientation.HORIZONTAL))

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

        self.__layout.append((row, column, brick,
                              LegoBrickLayout.Orientation.VERTICAL))

        for i in range(row, row + brick.getWidth()):
            self.__area[i][column:column + brick.getHeight()] = brick.getId()

        self.__coveredArea += brick.getArea()
        return True

    def tryAddBrick(self,
                    row: int,
                    column: int,
                    brick: LegoBrick,
                    orientation: Enum = None) -> bool:
        """
        Try to add the received brick to a specific place at the layer.

         Parameters
        ----------
        row : int
            The row index in the layer.
        column : int
            The column index in the layer.
        brick : LegoBrick
            The brick to add.
        orientation : LegoBrickLayout.Orientation
            default=None.
            If none will try to add vertically and horizontally (random order), else will try to add as required.

        Returns
        -------
        bool
            True if the brick added successfully and false if did not.

        Raises
        ------
        NotInitializedException
            If this method called before initialize() method
        """
        if not self.__initialized:
            raise NotInitializedException(
                "The instance used before calling initialize method")

        if orientation is None:
            firstVertical = bool(random.getrandbits(1))
            return self.__tryAdd(row, column, brick, firstVertical)
        elif orientation is LegoBrickLayout.Orientation.HORIZONTAL:
            return self.__tryAddHorizontal(row, column, brick)
        else:
            return self.__tryAddVertical(row, column, brick)

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
            copy.__layout = [[brick[0], brick[1], brick[2].copy(), brick[3]]
                             for brick in self.__layout]
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

    def getCollection(self) -> LegoBrickCollection:
        """
        Gets the layer brick collection.

        Returns
        -------
        LegoBrickCollection
            layer brick collection.

        Raises
        ------
        NotInitializedException
            If this method called before initialize() method
        """
        if not self.__initialized:
            raise NotInitializedException(
                "The instance used before calling initialize method")
        return self.__brickCollection

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

    def getAreaBricks(self) -> List[Tuple[int, int, LegoBrick, Enum]]:
        """
        Gets a list of all the bricks in the layer and their location on the layer.

        Returns
        -------
        List[Tuple[int, int, LegoBrick, LegoBrickLayout.Orientation]]
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

    def validateLayer(self) -> bool:
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

        try:
            self.__layout.sort(key=lambda brickPos: (brickPos[0], brickPos[1]))

            index = 0
            for x in range(self.__width):
                for y in range(self.__height):
                    if index < len(self.__layout) and self.__layout[index][
                            0] == x and self.__layout[index][1] == y:
                        if self.__layout[index][
                                3] == LegoBrickLayout.Orientation.VERTICAL:
                            for i in range(
                                    x, x + self.__layout[index][2].getWidth()):
                                self.__area[index][
                                    y:y + self.__layout[index][2].getHeight(
                                    )] = self.__layout[index][2].getId()
                        else:
                            for i in range(
                                    x,
                                    x + self.__layout[index][2].getHeight()):
                                self.__area[index][
                                    y:y + self.__layout[index][2].getWidth(
                                    )] = self.__layout[index][2].getId()
                        index += 1
                    else:
                        self.__area[x][y] = 0
        except:
            return False
        return True

    def hasSameCoverage(self, otherLayout) -> bool:
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
        ) or self.__height != otherLayout.getHeight():
            return False

        otherLayout = otherLayout.getAreaBricks()
        if len(self.__layout) != len(otherLayout):
            return False

        for i in range(len(self.__layout)):
            if self.__layout[i][0] != otherLayout[i][0] or self.__layout[
                    i][1] != otherLayout[i][1] or self.__layout[i][2].getWidth(
                    ) != otherLayout[i][2].getWidth() or self.__layout[i][
                        2].getHeight() != otherLayout[i][2].getHeight(
                        ) or self.__layout[i][3] != otherLayout[i][3]:
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
