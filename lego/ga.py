# ga.py

import time
from abc import ABC, abstractmethod
from typing import List

import numpy as np

import lego.ga_utils as GaUtils
import lego.utils as Utils
from lego.brick import LegoBrick
from lego.collection import LegoBrickCollection
from lego.exceptions import NotInitializedException
from lego.layout import LegoBrickLayout


class LegoBrickGA(object):
    class GaResultHandler(ABC):
        def __init__(self):
            super(LegoBrickGA.GaResultHandler, self).__init__()

        @abstractmethod
        def onGaResult(self, generation: int,
                       population: List[LegoBrickLayout]):
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

    def evolveGeneration(self,
                         nTimes=1,
                         generationResultHandler: GaResultHandler = None
                         ) -> LegoBrickLayout:
        population = self.__generatePopulations()

        print("\nStarting genetic algorithm..")
        self.__invokeHandler(generationResultHandler, 0, population)

        Utils.printProgressBar(
            0,
            nTimes,
            prefix="Progress",
            suffix="of generations have evolved",
            fill='#')

        for i in range(nTimes):
            if population[0].getCoveredArea(
            ) == population[0].getWidth() * population[1].getHeight():
                # found optimal solution
                return population[0]
            population = self.__evolve(population)
            Utils.printProgressBar(
                i + 1,
                nTimes,
                prefix="Progress",
                suffix="of generations have evolved",
                fill='#')
            self.__invokeHandler(generationResultHandler, i + 1, population)

        result = max(population, key=lambda item: item.getCoveredArea())
        print("Genetic algorithm finished!")
        return result

    def __invokeHandler(self, generationResultHandler: GaResultHandler,
                        generation: int, population: List[LegoBrickLayout]):
        if generationResultHandler is not None:
            generationResultHandler.onGaResult(generation, population)

    def __generatePopulations(self) -> List[LegoBrickLayout]:
        print("\nGenerating population..")

        Utils.printProgressBar(
            0,
            self.__populationSize,
            prefix="Progress",
            suffix="of population have created",
            fill='#')

        population = []
        while len(population) < self.__populationSize:
            bricks = self.__brickCollection.copy()
            layout = LegoBrickLayout()
            layout.initialize(self.__width, self.__height, bricks)
            if not layout.isInitialized():
                raise NotInitializedException(
                    "Failed on try to initialize LegoBrickLayout")
            toAdd = True
            for layoutInPopulation in population:
                if (layoutInPopulation.hasSameCoverage(layout)):
                    toAdd = False
                    break
            if not toAdd:
                continue
            population.append(layout)
            Utils.printProgressBar(
                len(population),
                self.__populationSize,
                prefix="Progress",
                suffix="of population have created",
                fill='#')

        population.sort(key=lambda item: item.getCoveredArea(), reverse=True)
        print("A population of", len(population), "was created.")
        return population

    def __evolve(self,
                 population: List[LegoBrickLayout]) -> List[LegoBrickLayout]:
        newPopulation = []

        newPopulation.append(population[0])
        newPopulation.append(population[1])

        populationValue = np.sum(
            [item.getCoveredArea() for item in population])
        probabilities = []
        for item in population:
            probabilities.append(item.getCoveredArea() / populationValue)

        while (len(newPopulation) < len(population)):
            select = np.random.choice(
                population, 2, replace=False, p=probabilities)

            children = GaUtils.evolve(select[0], select[1],
                                      self.__mutationThreshold)
            if children is None:
                continue
            value = [select[0], select[1], children[0], children[1]]
            value.sort(key=lambda item: item.getCoveredArea(), reverse=True)

            potentialToAdd = []

            for generateLayout in value:
                toAdd = True
                for populationLayout in newPopulation:
                    if populationLayout.hasSameCoverage(generateLayout):
                        toAdd = False
                        break
                if toAdd:
                    potentialToAdd.append(generateLayout)
                if len(potentialToAdd) == 2:
                    break

            if len(potentialToAdd) < 2:
                continue

            newPopulation.append(potentialToAdd[0])
            newPopulation.append(potentialToAdd[1])

        newPopulation.sort(
            key=lambda item: item.getCoveredArea(), reverse=True)

        return newPopulation
