# Genetic Algorithm Solution to 2D-LEGO Coverage Problem
The project suggests a solution to 2D-LEGO brick layout problem using genetic algorithm.

In general, 2D-LEGO brick layout problem is a combinatoric optimization problem with the following details:<br>
When given a layer with the size WxH and a bag of LEGO bricks, we want to find the optimal arrangement of the bricks on a paper to receive a maximum coverage.<br> 

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

TODO Add description how to run the tests

### Running the project

The entry point of the project is located in root directory.
To run the program with default configuration using: 
```
python run.py
```
In order to change the default configuration, you can use the following helping arguments:
```
Genetic Algorithm Solution to 2D-LEGO Brick Layout Problem:
              --help        : help string
              --width       : The width of the surface of the problem [default=25]
              --height      : The height of the surface of the problem [default=25]
              --types_num   : The amount of different bricks that will be used to solve the problem,
                              -1 for default bricks set [default=-1]
              --max_brick   : The maximum size of a brick rib [default='4']
                              it's irrelevant if the default set is selected in '-types'
              --population  : The size of the population [default='100']
              --generations : The amount of the generations [default='100']
              --mutation    : The mutation chance, in the range [0.0, 1.0].
                              0 will prevent the mutation [default='0.2']
              --verbose     : 0 for minimum prints and 1 for more prints [default='1']
              --color       : 1 for discrete coloring style, 2 for gradient coloring style [default='2']
```
For example, 
```
python run.py --width 100 --height 100 --types_num 8 --max_brick 7 --population 200 --generations 1000 --mutation 0.3 --verbose 0 --color 1
```
## Results

TODO show example

## Extra details about the algorithm

### Overview

![Overview of the algorithm](https://github.com/romanglo/2D-LEGO-GA/blob/master/images/overview.png)

### Crossover
This process selects a random two different point which represent a recangle.
Then, swaps between all the possible bricks inside the rectangle.
To explain the crossover process, we use the following example:
For the next two layers, randomize two points (2,2) and (7,7):
<br>
![Selection before crossover](https://github.com/romanglo/2D-LEGO-GA/blob/master/images/before_crossover.png.jpg)
<br>Then, swap the possible bricks: 
red, green and blue in first selection with grey, purple and beige from the second selection.
<br>
The orange and navy bricks could not swap with the black one from the other layer, because they are located partly outside of the layer.
<br>
![Selection before crossover](https://github.com/romanglo/2D-LEGO-GA/blob/master/images/after_crossover.png.jpg)

### Mutation

There are several mutations we use:
1. Swith a random brick with another one with different size.
1. Add a random brick to a random empty location.
1. Delete a random brick.
1. Move a random brick to a random direction (left, right, bottom or up).

## Authors

* **Roman Glozman** - [romanglo](https://github.com/romanglo)
* **Yoni Shpund** - [ShpundYoni](https://github.com/ShpundYoni)
* **Ariel Ya'akov** - [ariel3081](https://github.com/ariel3081)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

