import math
import sys
from typing import List

import numpy as np

from lego.brick import LegoBrick
from lego.collection import LegoBrickCollection
from lego.ga import LegoBrickGA
from lego.layout import LegoBrickLayout

DEFALT_WIDTH = 31
DEFALT_HEIGHT = 47
DEFALT_NUMBER_OF_BRICKS_TYPES = 20
DEFAULT_GENERATIONS = 10
DEFAULT_POPULATION_SIZE = 10
DEFAULT_MUTATION_THRESHOLD = 0.1


def readArguments(argv):
    return DEFALT_WIDTH, DEFALT_HEIGHT, DEFALT_NUMBER_OF_BRICKS_TYPES, DEFAULT_POPULATION_SIZE, DEFAULT_GENERATIONS, DEFAULT_MUTATION_THRESHOLD


def generateBricks(width: int, height: int,
                   numberOfBricksTypes: int) -> List[LegoBrick]:
    maxBrickSize = round(math.sqrt(min(width, height)))
    if (maxBrickSize * maxBrickSize) / 2 < numberOfBricksTypes:
        # the maximum permutation
        numberOfBricksTypes = int((maxBrickSize * maxBrickSize) / 2)
    maxBrickSize += 1
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
    brickCollection.initialize(71 * 163, bricks, uniform=True)
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
        width, height, numberOfBricksTypes, populationSize, generations, mutationThreshold = readArguments(
            argv)
        bricks = generateBricks(width, height, numberOfBricksTypes)
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
                # print res matrix:
                # resMat = mustValuedItem.getAreaMatrix()
                # for i in range(mustValuedItem.getWidth()):
                #     print("".join(("%5d" % x) for x in resMat[i]))

        ga.evaluate(
            nTimes=generations, generationResultHandler=GaResultHandler())
    except:
        print("Some error occurred during the running! Process aborted..")


# Run the program
if __name__ == "__main__":
    main(sys.argv[1:])
