# ga.py

import time
from abc import ABC, abstractmethod
from typing import List

import numpy as np

import _thread
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
                         ) -> List[LegoBrickLayout]:
        population = self.__generatePopulations()

        print("\nStarting genetic algorithm..")
        self.__invokeHandler(generationResultHandler, 0, population, True)

        Utils.printProgressBar(
            0,
            nTimes,
            prefix="Progress",
            suffix="of generations have evolved")

        for i in range(nTimes):
            population = self.__evolve(population)
            Utils.printProgressBar(
                i + 1,
                nTimes,
                prefix="Progress",
                suffix="of generations have evolved",
                fill='#')
            self.__invokeHandler(generationResultHandler, i + 1, population,
                                 True)

        time.sleep(1)  # To ensure that all GA threads finished their work.

        print("Genetic algorithm finished!")

        return population

    def __invokeHandler(self,
                        generationResultHandler: GaResultHandler,
                        generation: int,
                        population: List[LegoBrickLayout],
                        async: bool = False):
        if(population is None):
            print("Error!")
        if generationResultHandler is not None:
            if async:
                _thread.start_new_thread(generationResultHandler.onGaResult,
                                         (generation, population))
            else:
                generationResultHandler.onGaResult(generation, population)

    def __generatePopulations(self) -> List[LegoBrickLayout]:
        print("\nGenerating population..")

        Utils.printProgressBar(
            0,
            self.__populationSize,
            prefix="Progress",
            suffix="of population have created")

        population = []
        while len(population) < self.__populationSize:
            bricks = self.__brickCollection.copy()
            layout = LegoBrickLayout()
            layout.initialize(self.__width, self.__height, bricks)
            if not layout.isInitialized():
                raise NotInitializedException(
                    "Failed on try to initialize LegoBrickLayout")
            for layoutInPopulation in population:
                if (layoutInPopulation.hasSameCoverage(layout)):
                    break
            population.append(layout)
            Utils.printProgressBar(
                len(population),
                self.__populationSize,
                prefix="Progress",
                suffix="of population have created",
                fill='#')
        print("A population of", len(population), "was created.")
        return population

    def __evolve(self,
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

            children = GaUtils.evolve(select[0], select[1],
                                      self.__mutationThreshold)
            if children is None:
                continue

            newPopulation.append(children[0])
            newPopulation.append(children[1])

            # value = [select[0], select[1], children[0], children[1]].sort(
            # key=lambda item: item.getCoveredArea(), reverse=True)
            # TODO ROMAN: continue ga algorithm

        return newPopulation
