import math
import sys
import traceback
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import colors

from lego.brick import LegoBrick
from lego.collection import LegoBrickCollection
from lego.ga import LegoBrickGA
from lego.layout import LegoBrickLayout

DEFAULT_WIDTH = 50
DEFAULT_HEIGHT = 50
DEFAULT_NUMBER_OF_BRICKS_TYPES = 10
DEFAULT_MAX_BRICK_RIB_SIZE = 7
DEFAULT_GENERATIONS = 10
DEFAULT_POPULATION_SIZE = 20
DEFAULT_MUTATION_THRESHOLD = 0.0
DEFAULT_VERBOSE = True


def readArguments(argv):
    # TODO ROMAN: read arguments from command
    width = DEFAULT_WIDTH
    height = DEFAULT_HEIGHT
    numberOfBricksTypes = DEFAULT_NUMBER_OF_BRICKS_TYPES
    maxBrickRibSize = DEFAULT_MAX_BRICK_RIB_SIZE
    populationSize = DEFAULT_POPULATION_SIZE
    generations = DEFAULT_GENERATIONS
    mutationThreshold = DEFAULT_MUTATION_THRESHOLD
    verbose = DEFAULT_VERBOSE

    print("\Arguments:")
    print("-----------")
    print("width=", width)
    print("height=", height)
    print("number of bricks types=", numberOfBricksTypes)
    print("max brick rib size=", maxBrickRibSize)
    print("population size=", populationSize)
    print("generations=", generations)
    print("mutation threshold=", mutationThreshold)
    print("verbose=", verbose)

    return width, height, numberOfBricksTypes, maxBrickRibSize, populationSize, generations, mutationThreshold, verbose


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

    print("\nSelected Bricks:")
    for i in range(len(bricks)):
        print("%d - %s" % (i + 1, str(bricks[i])))
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


class GaResultHandler(LegoBrickGA.GaResultHandler):
    def __init__(self):
        super().__init__()
        self.sum = []
        self.average = []
        self.median = []
        self.max = []
        self.min = []
        self.area = 0
        self.generations = -1

    def onGaResult(self, generation: int, population: List[LegoBrickLayout]):

        covered = np.array([layout.getCoveredArea() for layout in population],
                           dtype=np.int32)

        covered = np.sort(covered)

        self.generations = max(self.generations, generation)
        self.sum.append(np.sum(covered))
        self.average.append(np.average(covered))
        self.median.append(np.median(covered))
        self.max.append(covered[len(covered) - 1])
        self.min.append(covered[0])


def drawStatisticsPlot(gaResultHandler: GaResultHandler):
    df = pd.DataFrame({
        "generation": range(gaResultHandler.generations + 1),
        "max": gaResultHandler.max,
        "min": gaResultHandler.min,
        "avg": gaResultHandler.average,
        "median": gaResultHandler.median,
        "sum": gaResultHandler.sum
    })

    labels = [
        "Max Coverage", "Min Coverage", "Average Coverage", "Median Coverage",
        "Total Coverage"
    ]

    # Initialize the figure
    plt.style.use("seaborn-darkgrid")

    palette = plt.get_cmap("Set1")

    num = 0
    for column in df.drop("generation", axis=1):

        plt.subplot(2, 3, num + 1)

        # Plot the lineplot
        plt.plot(
            df["generation"],
            df[column],
            marker="o",
            color=palette(num),
            linewidth=2,
            alpha=0.9,
            label=labels[num])

        # Add title
        plt.title(
            labels[num],
            loc="center",
            fontsize=12,
            fontweight=0,
            color=palette(num))

        num += 1

    plt.suptitle(
        "2D-LEGO Coverage Problem Genetic Algorithm Solution Statistics",
        fontsize=16,
        color="black",
    )

    plt.text(0.4, 0.05, "Generations", ha="center")

    try:
        # will work only on windows
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
    except:
        pass  # ignored


def drawResultPlot(result: LegoBrickLayout):

    area = result.getAreaMatrix()
    maxId = area.max()
    # create discrete colormap
    cmap = colors.ListedColormap(['red', 'blue'])
    bounds = [-1, 0.1, maxId + 1]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    fig, ax = plt.subplots()

    ax.imshow(result.getAreaMatrix(), cmap=cmap, norm=norm)

    ax.set_xticks(np.arange(start=0, stop=result.getWidth(), step=1))
    ax.set_yticks(np.arange(start=0, stop=result.getHeight(), step=1))
    # draw gridlines
    ax.grid(
        which='major', axis='both', linestyle='-', color='k', linewidth=0.5)

    plt.suptitle(
        "2D-LEGO Coverage Problem Genetic Algorithm Solution\n\nCoverage %d/%d"
        % (result.getCoveredArea(), (result.getWidth() * result.getHeight())),
        fontsize=16,
        color="black",
    )
    try:
        # will work only on windows
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
    except:
        pass  # ignored


def main(argv):
    try:
        width, height, numberOfBricksTypes, maxBrickRibSize, populationSize, generations, mutationThreshold, verbose = readArguments(
            argv)
        bricks = generateBricks(width, height, numberOfBricksTypes,
                                maxBrickRibSize)
        collection = generateCollection(width, height, bricks)
        ga = generateGa(width, height, collection, populationSize,
                        mutationThreshold)
        resultHandler = GaResultHandler()

        result = ga.evolveGeneration(
            nTimes=generations, generationResultHandler=resultHandler)

        print("Best layer cover %d from %d" %
              (result.getCoveredArea(),
               (result.getWidth() * result.getHeight())))

        drawStatisticsPlot(resultHandler)
        drawResultPlot(result)
        plt.show()

    except Exception as e:
        print("Some error occurred during the running! Process aborted..")
        if (verbose):
            print("\nError:", str(e))
            traceback.print_tb(e.__traceback__)


# Run the program
if __name__ == "__main__":
    main(sys.argv[1:])
