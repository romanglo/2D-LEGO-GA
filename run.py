import getopt
import math
import sys
import traceback
from typing import List

import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

from lego.brick import LegoBrick
from lego.collection import LegoBrickCollection
from lego.ga import LegoBrickGA
from lego.layout import LegoBrickLayout

DEFAULT_WIDTH = 25
DEFAULT_HEIGHT = 25
DEFAULT_NUMBER_OF_BRICKS_TYPES = -1
DEFAULT_MAX_BRICK_RIB_SIZE = 4
DEFAULT_GENERATIONS = 100
DEFAULT_POPULATION_SIZE = 100
DEFAULT_MUTATION_THRESHOLD = 0.2
DEFAULT_VERBOSE = True
DEFAULT_COLOR_TYPE = 2

HELP = """\nGenetic Algorithm Solution to 2D-LEGO Brick Layout Problem:
              --help        : help description
              --width       : The width of surface of the problem [default=%d]
              --height      : The height of surface of the problem [default=%d]
              --types_num   : The number of different bricks that will be used to solve the problem,
                              -1 for default bricks set [default=%d]
              --max_brick   : The maximum size of a brick rib [default='%d']
                              this is irrelevant if the default set is selected in '--types_num'
              --population  : The size of population [default='%d']
              --generations : The amount of generations [default='%d']
              --mutation    : The mutation chance, in the range [0.0, 1.0].
                              0 will prevent the mutation [default='%f']
              --verbose     : 0 for minimum prints and 1 for more prints [default='%d']
              --color       : 1 for discrete coloring style, 2 for gradient coloring style [default='%d']
           """ % (
    DEFAULT_WIDTH, DEFAULT_HEIGHT, DEFAULT_NUMBER_OF_BRICKS_TYPES,
    DEFAULT_MAX_BRICK_RIB_SIZE, DEFAULT_GENERATIONS, DEFAULT_POPULATION_SIZE,
    DEFAULT_MUTATION_THRESHOLD, DEFAULT_VERBOSE, DEFAULT_COLOR_TYPE)

HELP_ON_ERROR = "\nIncorrect command!\n" + HELP


def readArguments(argv):
    width = DEFAULT_WIDTH
    height = DEFAULT_HEIGHT
    numberOfBricksTypes = DEFAULT_NUMBER_OF_BRICKS_TYPES
    maxBrickRibSize = DEFAULT_MAX_BRICK_RIB_SIZE
    populationSize = DEFAULT_POPULATION_SIZE
    generations = DEFAULT_GENERATIONS
    mutationThreshold = DEFAULT_MUTATION_THRESHOLD
    verbose = DEFAULT_VERBOSE
    colorType = DEFAULT_COLOR_TYPE
    try:
        opts, args = getopt.getopt(argv, None, [
            "help", "width=", "height=", "types_num=", "max_brick=",
            "population=", "generations=", "mutation=", "verbose=", "color="
        ])
        for opt, arg in opts:
            if opt == "--help":
                print(HELP)
                sys.exit()
            elif opt == "--width":
                width = int(arg)
            elif opt == "--height":
                height = int(arg)
            elif opt == "--types_num":
                numberOfBricksTypes = int(arg)
            elif opt == "--max_brick":
                numberOfBricksTypes = int(arg)
            elif opt == "--population":
                populationSize = int(arg)
            elif opt == "--generations":
                generations = int(arg)
            elif opt == "--mutation":
                mutationThreshold = float(arg)
            elif opt == "--verbose":
                verbose = int(arg)
            elif opt == "--color":
                colorType = int(arg)
    except getopt.GetoptError:
        print(HELP_ON_ERROR)
        sys.exit()

    print("\nArguments:")
    print("width =", width)
    print("height =", height)
    if numberOfBricksTypes == -1:
        print("number of bricks types = default")
    else:
        print("number of bricks types =", numberOfBricksTypes)
    print("max brick rib size =", maxBrickRibSize)
    print("population size =", populationSize)
    print("generations =", generations)
    print("mutation threshold =", mutationThreshold)
    if verbose == 1:
        print("verbose = true")
    else:
        print("verbose = false")
    if colorType == 1:
        print("Color type = discrete")
    else:
        print("color type = gradient")

    return width, height, numberOfBricksTypes, maxBrickRibSize, populationSize, generations, mutationThreshold, verbose, colorType


def generateBricks(width: int, height: int, numberOfBricksTypes: int,
                   maxBrickRibSize: int) -> List[LegoBrick]:
    bricks = []
    if numberOfBricksTypes == -1:
        bricks.append(LegoBrick(1, 1))
        bricks.append(LegoBrick(2, 1))
        bricks.append(LegoBrick(3, 1))
        bricks.append(LegoBrick(4, 1))
        bricks.append(LegoBrick(5, 1))
        bricks.append(LegoBrick(8, 1))
        bricks.append(LegoBrick(2, 2))
        bricks.append(LegoBrick(3, 2))
        bricks.append(LegoBrick(4, 2))
        bricks.append(LegoBrick(5, 2))
        bricks.append(LegoBrick(8, 2))
    else:
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
        "Statistics of Genetic Algorithm Solution to 2D-LEGO Brick Layout Problem ",
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


def drawResultPlot(drawType: int, data: np.ndarray, covered: int):

    nx, ny = data.shape
    indx, indy = np.arange(nx), np.arange(ny)
    x, y = np.meshgrid(indx, indy)

    fig, ax = plt.subplots()

    if drawType == 1:
        maxId = data.max()
        # create discrete colormap
        cmap = colors.ListedColormap(["red", "blue"])
        bounds = [-1, 0.1, maxId + 1]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        ax.imshow(data.T, cmap=cmap, norm=norm)
    else:
        # plot grid values
        ax.imshow(data.T, interpolation="nearest", cmap=cm.YlGn)

    cond = nx <= 25 and ny <= 25

    for xval, yval in zip(x.flatten(), y.flatten()):
        zval = data[xval, yval]
        if zval == 0 or cond:
            t = "%d" % (zval, )  # format value with 1 decimal point
            c = "w" if zval > 0.75 else "k"  # if dark-green, change text color to white
            ax.text(xval, yval, t, color=c, va="center", ha="center")

    ax.set_xticks(indx + 0.5)
    ax.set_yticks(indy + 0.5)
    ax.xaxis.tick_top()

    for a, ind in zip((ax.xaxis, ax.yaxis), (indx, indy)):
        a.set_major_formatter(ticker.NullFormatter())
        a.set_minor_locator(ticker.FixedLocator(ind))

    # draw gridlines
    ax.grid(
        which="major", axis="both", linestyle="-", color="w", linewidth=0.5)

    ax.set_xlabel(
        "\nNote!\nInside the cells, there is the brick ID (to identify their shapes), where 0 is uncovered place.\nThe IDs appear only in matrices smaller than 25x25, you can identify uncovered places by their white color.",
        position=(0., 1e6),
        horizontalalignment='left')

    plt.suptitle(
        "Genetic Algorithm Solution to 2D-LEGO Brick Layout Problem\n\nCoverage %d/%d"
        % (covered, (nx * ny)),
        fontsize=16,
        color="black",
    )

    # font = {
    #     'family': 'serif',
    #     'color': 'darkred',
    #     'weight': 'normal',
    #     'size': 12,
    # }

    # plt.text(
    #     1,
    #     0.2,
    #     ,
    #     fontdict=font)

    try:
        # will work only on windows
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
    except:
        pass  # ignored


def main(argv):
    width, height, numberOfBricksTypes, maxBrickRibSize, populationSize, generations, mutationThreshold, verbose, dispayType = readArguments(
        argv)
    try:

        bricks = generateBricks(width, height, numberOfBricksTypes,
                                maxBrickRibSize)
        collection = generateCollection(width, height, bricks)
        ga = generateGa(width, height, collection, populationSize,
                        mutationThreshold)
        resultHandler = GaResultHandler()

        result = ga.evolveGeneration(
            nTimes=generations, generationResultHandler=resultHandler)

        if result.getCoveredArea() == result.getWidth() * result.getHeight():
            print("\nFound an optimal solution, a full coverage after",
                  resultHandler.generations, " generations!")
        print("\nBest layer cover %d from %d after %d generations" %
              (result.getCoveredArea(),
               (result.getWidth() * result.getHeight()),
               resultHandler.generations))

        # decrease the IDs to display:
        resMat = result.getAreaMatrix()
        index = 50
        mapping = {}
        for i in range(resMat.shape[0]):
            for j in range(resMat.shape[1]):
                if resMat[i][j] == 0:
                    continue
                mapped = mapping.get(resMat[i][j])
                if mapped is None:
                    mapping[resMat[i][j]] = index
                    resMat[i][j] = index
                    index += 1
                else:
                    resMat[i][j] = mapped

        if (verbose):
            print("\nBest Coverage:")
            for i in range(result.getWidth()):
                print("".join(("%5d" % x) for x in resMat[i]))

        drawStatisticsPlot(resultHandler)
        drawResultPlot(dispayType, resMat, result.getCoveredArea())
        plt.show()

    except Exception as e:
        print(
        )  # There is a chance that there was a exception in the middle of progress bar
        print("Some error occurred during the running! Process aborted..")
        if (verbose):
            print("\nError:", str(e))
            traceback.print_tb(e.__traceback__)
        else:
            print(
                "For more details, it is recommended to run with the verbose on option."
            )


# Run the program
if __name__ == "__main__":
    main(sys.argv[1:])
