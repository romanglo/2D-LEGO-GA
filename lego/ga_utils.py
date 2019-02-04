# ga_utils.py

from enum import Enum
from typing import List, Tuple

import numpy as np

import lego.utils as Utils
from lego.layout import LegoBrickLayout
from lego.utils import Rectangle


class Mutations(Enum):
    """
    Mutation is an enum Which represents the possible mutations.
    You can cancel the use of certain mutations by changing the list MutationsList.
    """
    CHANGE = 1
    ADD = 2
    REMOVE = 3
    MOVE = 4


MutationsList = list(Mutations)
"""
MutationList is the list of possible mutation during evolution.
Change this list will effect evolve() method.
"""


class __Directions(Enum):
    LEFT = 1
    UP = 2
    RIGHT = 3
    DOWN = 4


def evolve(
        firstParent: LegoBrickLayout, secondParent: LegoBrickLayout,
        mutationThreshold: float) -> Tuple[LegoBrickLayout, LegoBrickLayout]:
    """
    The method evolve 2 LegoBrickLayout (parents) using crossover and mutation.

    Parameters
    ----------
    firstParent : LegoBrickLayout
        First layer to evolve.
    secondParent : LegoBrickLayout
        Second layer to evolve.
    mutationThreshold : float
        The probability of a mutation occurring, in range [0.0, 1.0]

    Returns
    -------
    Tuple[LegoBrickLayout, LegoBrickLayout]
        The 2 evolved LegoBrickLayout (children) or None if an error occurred
    """
    children = crossover(firstParent, secondParent)

    if children is None:
        return None

    if MutationsList is not None and len(MutationsList) > 0:
        tryMutate(mutationThreshold, children[0])
        tryMutate(mutationThreshold, children[1])

    return children


def crossover(firstParent: LegoBrickLayout, secondParent: LegoBrickLayout
              ) -> Tuple[LegoBrickLayout, LegoBrickLayout]:
    """
    The method crossover 2 LegoBrickLayout.

    Parameters
    ----------
    firstParent : LegoBrickLayout
        First layer to crossover.
    secondParent : LegoBrickLayout
        Second layer to crossover.

    Returns
    -------
    Tuple[LegoBrickLayout, LegoBrickLayout]
        The 2 crossovers children (LegoBrickLayout) or None if the operation did not succeed
    """
    firstChild = None
    secondChild = None

    i = 0
    firstChild = firstParent.copy()
    secondChild = secondParent.copy()

    while True:
        width = min(firstParent.getWidth(), secondParent.getWidth())
        height = min(firstParent.getHeight(), secondParent.getHeight())

        crossWidth = np.random.randint(2, width)
        crossHeight = np.random.randint(2, height)

        points = np.random.choice(width - crossWidth, 2)

        firstChildCross, firstChildConstraints = getCrossAndConstraints(
            (points[0], points[0] + crossWidth - 1),
            (points[0], points[0] + crossHeight - 1), firstChild)
        secondChildCross, secondChildConstraints = getCrossAndConstraints(
            (points[0], points[0] + crossWidth - 1),
            (points[0], points[0] + crossHeight - 1), secondChild)

        if len(firstChildCross) == 0 and len(secondChildCross) == 0:
            continue

        if validateCrossAndConstaints2(firstChildCross, firstChildConstraints,
                                       secondChildCross,
                                       secondChildConstraints):
            break

        i += 1
        if i == 100:
            return None

    firstChildBricks = firstChild.getAreaBricks()
    for brick in firstChildCross:
        firstChildBricks.remove(brick)
    secondChildBricks = secondChild.getAreaBricks()
    for brick in secondChildCross:
        secondChildBricks.remove(brick)

    # Safe add but not efficient at all:
    firstChild.validateLayer()
    secondChild.validateLayer()

    for brick in firstChildCross:
        if not secondChild.tryAddBrick(brick[0], brick[1], brick[2], brick[3]):
            # should not happend!
            return None
        secondChild.validateLayer()
    for brick in secondChildCross:
        if not firstChild.tryAddBrick(brick[0], brick[1], brick[2], brick[3]):
            # should not happend!
            return None
        firstChild.validateLayer()

    return (firstChild, secondChild)


def validateCrossAndConstaints(
        firstChildCross: List, firstChildConstraints: List,
        secondChildCross: List, secondChildConstraints: List) -> bool:
    if len(secondChildConstraints) != 0:
        for cross in firstChildCross:
            crossRect = __getBrickRectangle(cross)
            for constraint in secondChildConstraints:
                constraintRect = __getBrickRectangle(constraint)
                if Utils.rectangleOverlappedArea(crossRect, constraintRect):
                    return False
    if len(firstChildConstraints) != 0:
        for cross in secondChildCross:
            crossRect = __getBrickRectangle(cross)
            for constraint in firstChildConstraints:
                constraintRect = __getBrickRectangle(constraint)
                if Utils.rectangleOverlappedArea(crossRect, constraintRect):
                    return False
    return True


def validateCrossAndConstaints2(
        firstChildCross: List, firstChildConstraints: List,
        secondChildCross: List, secondChildConstraints: List) -> bool:
    dirty = True
    while dirty:
        dirty = False

        if len(secondChildConstraints) != 0:
            toRemoveFromFirstCross = []
            for cross in firstChildCross:
                crossRect = __getBrickRectangle(cross)
                for constraint in secondChildConstraints:
                    constraintRect = __getBrickRectangle(constraint)
                    if Utils.rectangleOverlappedArea(crossRect,
                                                     constraintRect) != 0:
                        firstChildConstraints.append(cross)
                        toRemoveFromFirstCross.append(cross)
                        dirty = True
                        break
            for toRemove in toRemoveFromFirstCross:
                firstChildCross.remove(toRemove)

        if len(firstChildConstraints) != 0:
            toRemoveFromSecondCross = []
            for cross in secondChildCross:
                crossRect = __getBrickRectangle(cross)
                for constraint in firstChildConstraints:
                    constraintRect = __getBrickRectangle(constraint)
                    if Utils.rectangleOverlappedArea(crossRect,
                                                     constraintRect) != 0:
                        secondChildConstraints.append(cross)
                        toRemoveFromSecondCross.append(cross)
                        dirty = True
                        break
            for toRemove in toRemoveFromSecondCross:
                secondChildCross.remove(toRemove)

    return len(firstChildCross) != 0 or len(secondChildCross) != 0


def __getBrickRectangle(brick) -> Rectangle:
    if brick[3] == LegoBrickLayout.Orientation.HORIZONTAL:
        return Rectangle(brick[1], brick[0], brick[1] + brick[2].getWidth(),
                         brick[0] + brick[2].getHeight())
    else:
        return Rectangle(brick[1], brick[0], brick[1] + brick[2].getHeight(),
                         brick[0] + brick[2].getWidth())


def getCrossAndConstraints(
        xRange: Tuple[int, int],
        yRange: Tuple[int, int],
        layout: LegoBrickLayout,
        stopOnOneConstaint: bool = False) -> Tuple[List, List]:
    """
    The method finds the bricks that are fully within the range and partially within the area.

    Parameters
    ----------
    xRange : List[int]
        X range for check
    yRange : List[int]
        y range for check
    layout : LegoBrickLayout
        The layout to check
    stopOnOneConstaint : bool
        If true will stop searching once finding brick that is partially within the range.

    Returns
    -------
    Tuple[List, List]
        2 lists, the first one is list of the bricks in cross area and the second one is list of the constraints.
    """
    layoutBricks = layout.getAreaBricks()
    cross = []
    constraints = []

    crossRect = Rectangle(xRange[0], yRange[0], xRange[1] + 1, yRange[1] + 1)
    for brick in layoutBricks:
        isCross = False
        if brick[3] == LegoBrickLayout.Orientation.HORIZONTAL:
            if brick[1] >= xRange[0] and brick[0] >= yRange[0] and brick[
                    1] + brick[2].getWidth() - 1 <= xRange[1] and brick[
                        0] + brick[2].getHeight() - 1 <= yRange[1]:
                # all the brick in crossover area
                cross.append(brick)
                isCross = True
        else:
            if brick[1] >= xRange[0] and brick[0] >= yRange[
                    0] and brick[1] + brick[2].getHeight() - 1 <= xRange[
                        1] and brick[0] + brick[2].getWidth() - 1 <= yRange[1]:
                cross.append(brick)
                isCross = True
        if not isCross:
            brickRect = __getBrickRectangle(brick)
            if Utils.rectangleOverlappedArea(crossRect, brickRect) > 0:
                constraints.append(brick)
                if (stopOnOneConstaint):
                    break
    return cross, constraints


def tryMutate(mutationThreshold: float, layer: LegoBrickLayout) -> None:
    """
    The method try to perform a random mutation on a layer.
    The method chose a mutation from MutationsList.

    Parameters
    ----------
    mutationThreshold : float
        The probability of a mutation occurring, in range [0.0, 1.0]
    layout : LegoBrickLayout
        The layout to mutate

    """
    rndValue = np.random.rand()
    if rndValue > mutationThreshold:
        return
    mutationType = np.random.choice(MutationsList, size=1, replace=False)[0]

    if mutationType == Mutations.CHANGE:
        changeMutation(layer)
    elif mutationType == Mutations.ADD:
        addMutation(layer)
    elif mutationType == Mutations.REMOVE:
        removeMutation(layer)
    elif mutationType == Mutations.MOVE:
        moveMutation(layer)


def changeMutation(layer: LegoBrickLayout) -> bool:
    """
    The method try to perform a change mutation on a layer.

    Parameters
    ----------
    layout : LegoBrickLayout
        The layout to mutate

    Returns
    ----------
    bool
        true if the mutation succeed
    """
    if layer.getCollection().getAmountOfAvailableBricks() == 0:
        # There are no more bricks to add
        return False
    if (len(layer.getAreaBricks()) == 0):
        # There are no more bricks to remove
        return False
    indexToRemove = np.random.randint(len(layer.getAreaBricks()))
    brickToRemove = layer.getAreaBricks()[indexToRemove]
    layer.getAreaBricks().remove(brickToRemove)
    layer.validateLayer()

    randomBrick = layer.getCollection().getRandomBrick()
    if randomBrick.getHeight() == brickToRemove[2].getHeight(
    ) or randomBrick.getWidth() == brickToRemove[2].getWidth():
        if not layer.tryAddBrick(brickToRemove[0], brickToRemove[1],
                                 brickToRemove[2], brickToRemove[3]):
            # Should never happen
            layer.getCollection().returnBrick(brickToRemove[2])
        else:
            layer.validateLayer()

    if layer.tryAddBrick(brickToRemove[0], brickToRemove[1], randomBrick):
        layer.getCollection().returnBrick(brickToRemove[2])
        layer.validateLayer()
        return True
    else:
        layer.getCollection().returnBrick(randomBrick)
        if not layer.tryAddBrick(brickToRemove[0], brickToRemove[1],
                                 brickToRemove[2], brickToRemove[3]):
            # Should never happen
            layer.getCollection().returnBrick(brickToRemove[2])
        else:
            layer.validateLayer()
        return False


def addMutation(layer: LegoBrickLayout) -> bool:
    """
    The method try to perform an add mutation on a layer.

    Parameters
    ----------
    layout : LegoBrickLayout
        The layout to mutate

    Returns
    ----------
    bool
        true if the mutation succeed
    """
    if layer.getCollection().getAmountOfAvailableBricks() == 0:
        # There are no more bricks to add
        return False

    emptyPlaces = np.where(layer.getAreaMatrix() == 0)
    if len(emptyPlaces[0]) == 0:
        return False

    rndIndex = np.random.randint(len(emptyPlaces[0]))

    brick = layer.getCollection().getRandomBrick()
    if layer.tryAddBrick(emptyPlaces[0][rndIndex], emptyPlaces[1][rndIndex],
                         brick):
        layer.validateLayer()
        return True
    else:
        layer.getCollection().returnBrick(brick)
        return False


def removeMutation(layer: LegoBrickLayout) -> bool:
    """
    The method try to perform a remove mutation on a layer.

    Parameters
    ----------
    layout : LegoBrickLayout
        The layout to mutate

    Returns
    ----------
    bool
        true if the mutation succeed
    """
    if (len(layer.getAreaBricks()) == 0):
        # There are no more bricks to remove
        return False
    indexToRemove = np.random.randint(len(layer.getAreaBricks()))
    brickToRemove = layer.getAreaBricks()[indexToRemove]
    layer.getAreaBricks().remove(brickToRemove)
    layer.getCollection().returnBrick(brickToRemove[2])
    layer.validateLayer()
    return True


def moveMutation(layer: LegoBrickLayout) -> bool:
    """
    The method try to perform a move mutation on a layer.

    Parameters
    ----------
    layout : LegoBrickLayout
        The layout to mutate

    Returns
    ----------
    bool
        true if the mutation succeed
    """
    if (len(layer.getAreaBricks()) == 0):
        # There are no more bricks to move
        return False

    indexToRemove = np.random.randint(len(layer.getAreaBricks()))
    brickToRemove = layer.getAreaBricks()[indexToRemove]
    layer.getAreaBricks().remove(brickToRemove)
    layer.validateLayer()

    DirectionsList = list(__Directions)
    np.random.shuffle(DirectionsList)
    for direction in DirectionsList:
        added = False
        if direction == __Directions.LEFT:
            added = layer.tryAddBrick(brickToRemove[0] - 1, brickToRemove[1],
                                      brickToRemove[2], brickToRemove[3])
        elif direction == __Directions.UP:
            added = layer.tryAddBrick(brickToRemove[0], brickToRemove[1] - 1,
                                      brickToRemove[2], brickToRemove[3])
        elif direction == __Directions.RIGHT:
            added = layer.tryAddBrick(brickToRemove[0] + 1, brickToRemove[1],
                                      brickToRemove[2], brickToRemove[3])
        elif direction == __Directions.DOWN:
            added = layer.tryAddBrick(brickToRemove[0], brickToRemove[1] + 1,
                                      brickToRemove[2], brickToRemove[3])
        if added:
            layer.validateLayer()
            return True

    if not layer.tryAddBrick(brickToRemove[0], brickToRemove[1],
                             brickToRemove[2], brickToRemove[3]):
        # Should never happen
        layer.getCollection().returnBrick(brickToRemove[2])
    else:
        layer.validateLayer()

    return False
