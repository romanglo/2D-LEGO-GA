import numpy as np

from lego.brick import LegoBrick
from lego.collection import LegoBrickCollection
from lego.exceptions import NotInitializedException
from lego.layout import LegoBrickLayout

from abc import ABC, abstractmethod


class LegoBrickGA(object):
    class GaResultHandler(ABC):
        def __init__(self):
            super(LegoBrickGA.GaResultHandler, self).__init__()

        @abstractmethod
        def onGaResult(self, generation: int, populationValue: int,
                       mustValuedItem: LegoBrickLayout):
            pass

    def __init__(self,
                 width: int,
                 height: int,
                 brickCollection: LegoBrickCollection,
                 populationSize: int,
                 mutationThreshold=float):
        self.__validateInitParameters(width, height, brickCollection,
                                      populationSize, mutationThreshold)
        self.__generatePopulations()
        pass

    def __validateInitParameters(self,
                                 width: int,
                                 height: int,
                                 brickCollection: LegoBrickCollection,
                                 populationSize: int,
                                 mutationThreshold=float):
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
        self.__brickCollection = brickCollection
        if populationSize < 1:
            raise ValueError("population size must be bigger then 1!")
        if populationSize % 2 != 0:
            populationSize += 1
        self.__populationSize = populationSize
        if mutationThreshold < 0.0 or mutationThreshold > 1.0:
            raise ValueError("mutation threshold must be in range [0.0,1.0]!")
        self.__mutationThreshold = mutationThreshold

    def __generatePopulations(self):
        population = []
        while len(population) < self.__populationSize:
            bricks = self.__brickCollection.copy()
            layout = LegoBrickLayout()
            layout.initialize(self.__width, self.__height, bricks)
            if not layout.isInitialized():
                raise NotInitializedException(
                    "Failed on try to initialize LegoBrickLayout")
            population.append(layout)
        self.__population = population

    def evaluate(self,
                 nTimes=1,
                 generationResultHandler: GaResultHandler = None
                 ) -> LegoBrickLayout:

        populationValue = np.sum(
            [item.getCoveredArea() for item in self.__population])
        probabilities = []
        for item in self.__population:
            probabilities.append(item.getCoveredArea() / populationValue)

        bestItem = max(
            self.__population, key=lambda item: item.getCoveredArea())
        if generationResultHandler is not None:
            generationResultHandler.onGaResult(1, populationValue, bestItem)
        return bestItem
