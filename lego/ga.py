# ga.py

from abc import ABC, abstractmethod
from typing import List

import numpy as np

from lego.brick import LegoBrick
from lego.collection import LegoBrickCollection
from lego.exceptions import NotInitializedException
from lego.layout import LegoBrickLayout


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

    def evaluateGeneration(self,
                           nTimes=1,
                           generationResultHandler: GaResultHandler = None
                           ) -> LegoBrickLayout:
        population = self.__generatePopulations()
        self.__invokeHandler(generationResultHandler, population)

        for i in range(nTimes):
            population = self.__evaluate(population)
            self.__invokeHandler(generationResultHandler, population)

        return max(population, key=lambda item: item.getCoveredArea())

    def __invokeHandler(self,
                        generationResultHandler: GaResultHandler,
                        population: List[LegoBrickLayout],
                        async: bool = False):
        if generationResultHandler is not None:
            bestItem = max(population, key=lambda item: item.getCoveredArea())
            populationValue = np.sum(
                [item.getCoveredArea() for item in population])
            generationResultHandler.onGaResult(0, populationValue, bestItem)

    def __generatePopulations(self) -> List[LegoBrickLayout]:
        population = []
        while len(population) < self.__populationSize:
            bricks = self.__brickCollection.copy()
            layout = LegoBrickLayout()
            layout.initialize(self.__width, self.__height, bricks)
            if not layout.isInitialized():
                raise NotInitializedException(
                    "Failed on try to initialize LegoBrickLayout")
            population.append(layout)
        return population

    def __evaluate(self,
                   population: List[LegoBrickLayout]) -> List[LegoBrickLayout]:
        populationValue = np.sum(
            [item.getCoveredArea() for item in population])
        probabilities = []
        for item in population:
            probabilities.append(item.getCoveredArea() / populationValue)

        newPopulation = []
        while (len(newPopulation) < len(population)):
            select = np.random.choice(
                population, 2, replace=False, p=probabilities)
            children = self.__crossover(select[0], select[1])
            mutatedChildren = self.__mutate(children[0], children[1])

            value = [
                select[0], select[1], mutatedChildren[0], mutatedChildren[1]
            ].sort(
                key=lambda item: item.getCoveredArea(), reverse=True)
            # TODO ROMAN: continue ga algorithm
            break

        return population

    def __crossover(self, firstParent: LegoBrickLayout,
                    secondParent: LegoBrickLayout) -> List[LegoBrickLayout]:
        return [firstParent, secondParent]

    def __mutate(self, firstChild: LegoBrickLayout,
                 secondChild: LegoBrickLayout) -> List[LegoBrickLayout]:
        return [firstChild, secondChild]
