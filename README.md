# Genetic Algorithm Solution to 2D-LEGO Coverage Problem
The project suggests a solution to 2D-LEGO brick layout problem using a genetic algorithm.

In general, 2D-LEGO brick layout problem is a combinatorial optimization problem with the following details:<br>
When given a layer with the size WxH and a bag of LEGO bricks, we want to find the optimal arrangement of the bricks on a paper to receive maximum coverage.<br>

## Getting Started

### Prerequisites

The project was written in Python's version 3.6.8, but there should be no problem with every 3.* version.<br>
You can check your python version using:
```
python -v
```
The project depends on the following packages:
```
matplotlib==3.0.2
pandas==0.23.4
numpy==1.15.4
typing==3.6.6
```

Dependencies can be installed with pip:
```
pip install -r requirements.txt
```

### Running the tests

You can run all tests using:
```
python tests.py
```
in root directory.<br><br>
The script tests the importing of the dependencies and runs unit tests on several key parts in the project.

### Running the project

The entry point of the project is located in root directory.
To run the program with default configuration using:
```
python run.py
```
In order to change the default configuration, you can use the following helping arguments:
```
Genetic Algorithm Solution to 2D-LEGO Brick Layout Problem:
              --help        : help description
              --width       : The width of surface of the problem [default=25]
              --height      : The height of surface of the problem [default=25]
              --types_num   : The number of different bricks that will be used to solve the problem,
                              -1 for default bricks set [default=-1]
              --max_brick   : The maximum size of a brick rib [default='4']
                              this is irrelevant if the default set is selected in '--types_num'
              --population  : The size of population [default='100']
              --generations : The amount of generations [default='100']
              --mutation    : The mutation chance, in the range [0.0, 1.0].
                              0 will prevent the mutation [default='0.200000']
              --verbose     : 0 for minimum prints and 1 for more prints [default='1']
              --color       : 1 for discrete coloring style, 2 for gradient coloring style [default='2']
```
For example,
```
python run.py --width 100 --height 100 --types_num 8 --max_brick 7 --population 200 --generations 1000 --mutation 0.3 --verbose 0 --color 1
```

**Important Note!** Inserting parameters in the wrong ratio might lead to a situation that the algorithm reaches a "saturation" (can't produce a new generation which is different from the existing one). This situation will significantly slow down the program and might even lead to a complete halt of the algorithm.
Therefore you can abort the program at any time by pressing CTRL+C and observe the solution of the last generation that completed fully.

## Results

As an output, the algorithm presents two windows. The first one demonstrates the result of optimal coverage and the second one displays statistics about the algorithm.<br><br>
For example, we ran the project using the following command:
```
python run.py --population 200 --generations 1000
```
We stopped the process after 1113 generations and got the next result:<br><br>
![Result figure 2](https://github.com/romanglo/2D-LEGO-GA/blob/master/images/res_figure_2.png)
<br>
![Result figure 1](https://github.com/romanglo/2D-LEGO-GA/blob/master/images/res_figure_1.png)

## Extra details about the algorithm

### Overview

![Overview of the algorithm](https://github.com/romanglo/2D-LEGO-GA/blob/master/images/overview.png)

### Crossover
This process selects a random two different point which represent a rectangle.
Then, swaps between all the possible bricks inside the rectangle.
To explain the crossover process, we use the following example:
For the next two layers, randomize two points (2,2) and (7,7):
<br>
![Selection before crossover](https://github.com/romanglo/2D-LEGO-GA/blob/master/images/before_crossover.jpg)
<br>Then, swap the possible bricks:
red, green and blue in first selection with grey, purple and beige from the second selection.
<br>
The orange and navy bricks could not swap with the black one from the other layer, because they are located partly outside of the layer.
<br>
![Selection before crossover](https://github.com/romanglo/2D-LEGO-GA/blob/master/images/after_crossover.jpg)

### Mutation

There are several mutations we use:
1. Switch a random brick with another one with different size.
1. Add a random brick to a random empty location.
1. Delete a random brick.
1. Move a random brick to a random direction (left, right, bottom or up).

## Authors

* **Roman Glozman** - [romanglo](https://github.com/romanglo)
* **Yoni Shpund** - [YoniShpund](https://github.com/YoniShpund)
* **Ariel Ya'akov** - [ariel3081](https://github.com/ariel3081)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

