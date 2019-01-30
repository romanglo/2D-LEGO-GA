# ga_utils.py

from enum import Enum
from typing import Tuple

import numpy as np

from lego.layout import LegoBrickLayout


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

    if MutationsList is not None and len(MutationsList) > 0:
        tryMutate(mutationThreshold, children[0])
        tryMutate(mutationThreshold, children[1])

    return children


def crossover(firstParent: LegoBrickLayout, secondParent: LegoBrickLayout):
    return (firstParent, secondParent)


def tryMutate(mutationThreshold: float, layer: LegoBrickLayout) -> None:
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
