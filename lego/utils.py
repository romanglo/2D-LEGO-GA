from collections import namedtuple

Rectangle = namedtuple("Rectangle", "xMin yMin xMax yMax")


def rectangleOverlappedArea(firstRec: Rectangle, secondRec: Rectangle):
    """
    Calculate the overlapped area between two rectangle.

    Parameters:
    -----------
    firstRec : Rectangle
        the first rectangle
    secondRec : Rectangle
        the second rectangle

    Returns:
    --------
    The overlapped area between the received rectangles,
    0 if there is no overlapping area or one of the rectangles is None.
    """
    dx = min(firstRec.xMax, secondRec.xMax) - max(firstRec.xMin,
                                                  secondRec.xMin)
    dy = min(firstRec.yMax, secondRec.yMax) - max(firstRec.yMin,
                                                  secondRec.yMin)
    if (dx >= 0) and (dy >= 0):
        return dx * dy
    return 0


def printProgressBar(iteration: int,
                     total: int,
                     prefix: str = "",
                     suffix: str = "",
                     decimals: int = 1,
                     length: int = 100,
                     fill: str = "█") -> None:
    """
    Call in a loop to create terminal progress bar

    Parameters:
    -----------
    iteration : int
        number of current iteration.
    total : int
        number of total iterations.
    prefix : str [default = empty string]
        prefix string.
    suffix : str [default = empty string]
        suffix string.
    decimals : int [default = 1]
        positive number of decimals in percent complete.
    length : int [default = 100]
        character length of bar.
    fill : str [default = \"█\"]
         bar fill character.
    """

    # return

    percent = ("{0:." + str(decimals) + "f}").format(
        100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + "-" * (length - filledLength)
    print("\r%s |%s| %s%% %s" % (prefix, bar, percent, suffix), end="\r")
    # Print New Line on Complete
    if iteration == total:
        print()
