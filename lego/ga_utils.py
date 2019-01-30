# ga_utils.py

from enum import Enum
from typing import Tuple

import numpy as np

from lego.layout import LegoBrickLayout


class Mutation(Enum):
    CHANGE = 1
    ADD = 2
    REMOVE = 3
    MOVE = 4


MutationList = list(Mutation)


def evaluate(firstParent: LegoBrickLayout, secondParent: LegoBrickLayout,
             mutationRate: float):

    pass


def crossover(firstParent: LegoBrickLayout, secondParent: LegoBrickLayout):
    pass


def mutate(mutationRate: float, child: LegoBrickLayout) -> None:
    rndValue = np.random.rand()
    if rndValue < mutationRate:
        return
    mutationType = np.random.choice(MutationList, size=1, replace=False)[0]

    if mutationType == Mutation.CHANGE:
        changeMutation(LegoBrickLayout)
    elif mutationType == Mutation.ADD:
        addMutation(LegoBrickLayout)
    elif mutationType == Mutation.REMOVE:
        removeMutation(LegoBrickLayout)
    elif mutationType == Mutation.MOVE:
        moveMutation(LegoBrickLayout)


def changeMutation(child: LegoBrickLayout) -> bool:
    pass


def addMutation(child: LegoBrickLayout) -> bool:
    if child.getCollection().getAmountOfAvailableBricks() == 0:
        # There are no more bricks to add
        return False

    emptyPlaces = np.where(child.getAreaMatrix() == 0)
    rndIndex = np.random.randint(len(emptyPlaces[0]))

    brick = child.getCollection().getRandomBrick()
    if child.tryAddBrick(emptyPlaces[0][rndIndex], emptyPlaces[1][rndIndex],
                         brick):
        child.validateLayer()
        return True
    else:
        child.getCollection().returnBrick(brick)
        return False


def removeMutation(child: LegoBrickLayout) -> bool:
    if (len(child.getAreaBricks()) == 0):
        return False
    indexToRemove = np.random.randint(len(child.getAreaBricks()))
    child.getAreaBricks().remove(child.getAreaBricks()[indexToRemove])
    child.validateLayer()
    return True


def moveMutation(child: LegoBrickLayout) -> bool:
    pass
