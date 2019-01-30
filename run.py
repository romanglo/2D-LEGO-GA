import math
import sys
from typing import List

import numpy as np

from lego.brick import LegoBrick
from lego.collection import LegoBrickCollection
from lego.ga import LegoBrickGA
from lego.layout import LegoBrickLayout

DEFAULT_WIDTH = 10
DEFAULT_HEIGHT = 10
DEFAULT_NUMBER_OF_BRICKS_TYPES = 5
DEFAULT_MAX_BRICK_RIB_SIZE = 7
DEFAULT_GENERATIONS = 10
DEFAULT_POPULATION_SIZE = 10
DEFAULT_MUTATION_THRESHOLD = 0.1


def readArguments(argv):
    return DEFAULT_WIDTH, DEFAULT_HEIGHT, DEFAULT_NUMBER_OF_BRICKS_TYPES, DEFAULT_MAX_BRICK_RIB_SIZE, DEFAULT_POPULATION_SIZE, DEFAULT_GENERATIONS, DEFAULT_MUTATION_THRESHOLD


def generateBricks(width: int, height: int, numberOfBricksTypes: int,
                   maxBrickRibSize: int) -> List[LegoBrick]:
    maxBrickSize = maxBrickRibSize + 1
    bricks = []
    while len(bricks) < numberOfBricksTypes:
        width = np.random.randint(1, maxBrickSize)
        height = np.random.randint(1, maxBrickSize)
        if width > height:
            temp = height
            height = width
            width = temp
        brick = LegoBrick(width, height)
        if brick not in bricks:
            bricks.append(brick)

    return bricks


def generateCollection(width: int, height: int,
                       bricks: List[LegoBrick]) -> LegoBrickCollection:
    brickCollection = LegoBrickCollection()
    brickCollection.initialize(width * height, bricks, uniform=True)
    assert brickCollection.isInitialized()
    return brickCollection


def generateGa(width: int,
               height: int,
               bricksCollection: LegoBrickCollection,
               populationSize=int,
               mutationThreshold=float) -> LegoBrickGA:
    ga = LegoBrickGA(width, height, bricksCollection, populationSize,
                     mutationThreshold)
    return ga


def main(argv):
    try:
        width, height, numberOfBricksTypes, maxBrickRibSize, populationSize, generations, mutationThreshold = readArguments(
            argv)
        bricks = generateBricks(width, height, numberOfBricksTypes,
                                maxBrickRibSize)
        collection = generateCollection(width, height, bricks)
        ga = generateGa(width, height, collection, populationSize,
                        mutationThreshold)

        class GaResultHandler(LegoBrickGA.GaResultHandler):
            def onGaResult(self, generation: int, populationValue: int,
                           mustValuedItem: LegoBrickLayout):
                print(
                    "Generations %d: Population Value = %d, Max Coverage = %d/%d"
                    %
                    (generation, populationValue,
                     mustValuedItem.getCoveredArea(),
                     (mustValuedItem.getHeight() * mustValuedItem.getWidth())))

        ga.evaluate(
            nTimes=generations, generationResultHandler=GaResultHandler())
    except:
        print("Some error occurred during the running! Process aborted..")


# Run the program
if __name__ == "__main__":
    main(sys.argv[1:])
