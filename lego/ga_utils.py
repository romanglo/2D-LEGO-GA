# ga_utils.py

from enum import Enum
from typing import List, Tuple

import numpy as np

import lego.utils as Utils
from lego.layout import LegoBrickLayout
from lego.utils import Rectangle


class Mutations(Enum):
    CHANGE = 1
    ADD = 2
    REMOVE = 3
    MOVE = 4


MutationsList = list(Mutations)
"""
MutationList is the list of possible mutation during evolution.
Change this list will effect evolve() method.
"""


class Directions(Enum):
    LEFT = 1
    UP = 2
    RIGHT = 3
    DOWN = 4


def evolve(
        firstParent: LegoBrickLayout, secondParent: LegoBrickLayout,
        mutationThreshold: float) -> Tuple[LegoBrickLayout, LegoBrickLayout]:
    children = crossover(firstParent, secondParent)

    if children is None:
        return None

    if MutationsList is not None and len(MutationsList) > 0:
        tryMutate(mutationThreshold, children[0])
        tryMutate(mutationThreshold, children[1])

    return children


def crossover(firstParent: LegoBrickLayout, secondParent: LegoBrickLayout):
    firstChild = firstParent.copy()
    secondChild = secondParent.copy()
    width = min(firstParent.getWidth(), secondParent.getWidth())
    height = min(firstParent.getHeight(), secondParent.getHeight())

    xPoints = np.sort(np.random.choice(width, 2, False))
    while xPoints[1] - xPoints[0] <= 1:
        xPoints = np.sort(np.random.choice(width, 2, False))
    yPoints = np.sort(np.random.choice(height, 2, False))
    while yPoints[1] - yPoints[0] <= 1:
        yPoints = np.sort(np.random.choice(height, 2, False))

    firstChildCross, firstChildConstraints = __getCrossAndConstraints(
        xPoints, yPoints, firstChild)
    secondChildCross, secondChildConstraints = __getCrossAndConstraints(
        xPoints, yPoints, secondChild)

    if len(firstChildCross) == 0 and len(secondChildCross) == 0:
        return (firstChild, secondChild)

    __validateCrossData(firstChildCross, firstChildConstraints,
                        secondChildCross, secondChildConstraints)

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
            # FIXME ROMAN: should not happend!"
            return None
        secondChild.validateLayer()
    for brick in secondChildCross:
        if not firstChild.tryAddBrick(brick[0], brick[1], brick[2], brick[3]):
            # FIXME ROMAN: should not happend!"
            return None
        firstChild.validateLayer()

    # TODO ROMAN: add this instead the code above, this is unsafe but more efficient add
    # for brick in firstChildCross:
    #     secondChildBricks.append(brick)
    # for sec in secondChildCross:
    #     firstChildBricks.append(brick)
    # return (firstChild, secondChild)
    # firstChild.validateLayer()
    # secondChild.validateLayer()

    return (firstChild, secondChild)


def __validateCrossData(firstCross, firstConstraints, secondCross,
                        secondConstraints):

    dirty = True
    while dirty:
        dirty = False
        for crossBrick in list(firstCross):
            crossBrickRec = __getBrickRectangle(crossBrick)
            for constarintBrick in secondConstraints:
                constarintBrickRec = __getBrickRectangle(crossBrick)
                if Utils.rectangleOverlappedArea(crossBrickRec,
                                                 constarintBrickRec) != 0:
                    dirty = True
                    firstCross.remove(crossBrick)
                    firstConstraints.append(crossBrick)
                    break
        for crossBrick in list(secondCross):
            crossBrickRec = __getBrickRectangle(crossBrick)
            for constarintBrick in firstConstraints:
                constarintBrickRec = __getBrickRectangle(crossBrick)
                if Utils.rectangleOverlappedArea(crossBrickRec,
                                                 constarintBrickRec) != 0:
                    dirty = True
                    secondCross.remove(crossBrick)
                    secondConstraints.append(crossBrick)
                    break


def __getBrickRectangle(brick) -> Rectangle:
    if brick[3] == LegoBrickLayout.Orientation.HORIZONTAL:
        return Rectangle(brick[0], brick[1], brick[0] + brick[2].getWidth(),
                         brick[1] + brick[2].getHeight())
    else:
        return Rectangle(brick[0], brick[1], brick[0] + brick[2].getHeight(),
                         brick[1] + brick[2].getWidth())


def __getCrossAndConstraints(xRange: List[int], yRange: List[int],
                             layout: LegoBrickLayout) -> Tuple[List, List]:
    layoutBricks = layout.getAreaBricks()
    cross = []
    constraints = []

    for brick in layoutBricks:
        if brick[3] == LegoBrickLayout.Orientation.HORIZONTAL:
            if brick[0] > xRange[0] and brick[1] > yRange[
                    0] and brick[0] + brick[2].getWidth() < xRange[
                        1] and brick[1] + brick[2].getHeight() < yRange[1]:
                # all the brick in crossover area
                cross.append(brick)
            elif (brick[0] > xRange[0] and brick[0] < xRange[1]
                  and brick[1] > yRange[0] and brick[1] < yRange[1]):
                # (x,y) in the crossover area
                constraints.append(brick)
            elif (brick[0] + brick[2].getWidth() > xRange[0]
                  and brick[0] + brick[2].getWidth() < xRange[1]
                  and brick[1] > yRange[0] and brick[1] < yRange[1]):
                # (x+ brick_width,y) in the crossover area
                constraints.append(brick)
            elif (brick[0] > xRange[0] and brick[0] < xRange[1]
                  and brick[1] + brick[2].getHeight() > yRange[0]
                  and brick[1] + brick[2].getHeight() < yRange[1]):
                # (x,y + brick_height) in the crossover area
                constraints.append(brick)
            elif (brick[0] + brick[2].getWidth() > xRange[0]
                  and brick[0] + brick[2].getWidth() < xRange[1]
                  and brick[1] + brick[2].getHeight() > yRange[0]
                  and brick[1] + brick[2].getHeight() < yRange[1]):
                # (x+ brick_width,y + brick_height) in the crossover area
                constraints.append(brick)
        else:
            if brick[0] > xRange[0] and brick[1] > yRange[
                    0] and brick[0] + brick[2].getHeight() < xRange[
                        1] and brick[1] + brick[2].getWidth() < yRange[1]:
                cross.append(brick)
            elif (brick[0] > xRange[0] and brick[0] < xRange[1]
                  and brick[1] > yRange[0] and brick[1] < yRange[1]):
                # (x,y) in the crossover area
                constraints.append(brick)
            elif (brick[0] + brick[2].getHeight() > xRange[0]
                  and brick[0] + brick[2].getHeight() < xRange[1]
                  and brick[1] > yRange[0] and brick[1] < yRange[1]):
                # (x+ brick_height,y) in the crossover area
                constraints.append(brick)
            elif (brick[0] > xRange[0] and brick[0] < xRange[1]
                  and brick[1] + brick[2].getWidth() > yRange[0]
                  and brick[1] + brick[2].getWidth() < yRange[1]):
                # (x,y + brick_width) in the crossover area
                constraints.append(brick)
            elif (brick[0] + brick[2].getHeight() > xRange[0]
                  and brick[0] + brick[2].getHeight() < xRange[1]
                  and brick[1] + brick[2].getWidth() > yRange[0]
                  and brick[1] + brick[2].getWidth() < yRange[1]):
                # (x+ brick_height,y + brick_width) in the crossover area
                constraints.append(brick)
    return cross, constraints


def tryMutate(mutationThreshold: float, layer: LegoBrickLayout) -> None:
    rndValue = np.random.rand()
    if rndValue > mutationThreshold:
        return
    mutationType = np.random.choice(MutationsList, size=1, replace=False)[0]

    res = False
    if mutationType == Mutations.CHANGE:
        res = changeMutation(layer)
    elif mutationType == Mutations.ADD:
        res = addMutation(layer)
    elif mutationType == Mutations.REMOVE:
        res = removeMutation(layer)
    elif mutationType == Mutations.MOVE:
        res = moveMutation(layer)


def changeMutation(layer: LegoBrickLayout) -> bool:
    if layer.getCollection().getAmountOfAvailableBricks() == 0:
        # There are no more bricks to change
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
    if layer.getCollection().getAmountOfAvailableBricks() == 0:
        # There are no more bricks to add
        return False

    emptyPlaces = np.where(layer.getAreaMatrix() == 0)
    if emptyPlaces == 0:
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
    if (len(layer.getAreaBricks()) == 0):
        # There are no more bricks to move
        return False

    indexToRemove = np.random.randint(len(layer.getAreaBricks()))
    brickToRemove = layer.getAreaBricks()[indexToRemove]
    layer.getAreaBricks().remove(brickToRemove)
    layer.validateLayer()

    DirectionsList = list(Directions)
    np.random.shuffle(DirectionsList)
    for direction in DirectionsList:
        added = False
        if direction == Directions.LEFT:
            added = layer.tryAddBrick(brickToRemove[0] - 1, brickToRemove[1],
                                      brickToRemove[2], brickToRemove[3])
        elif direction == Directions.UP:
            added = layer.tryAddBrick(brickToRemove[0], brickToRemove[1] - 1,
                                      brickToRemove[2], brickToRemove[3])
        elif direction == Directions.RIGHT:
            added = layer.tryAddBrick(brickToRemove[0] + 1, brickToRemove[1],
                                      brickToRemove[2], brickToRemove[3])
        elif direction == Directions.DOWN:
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
