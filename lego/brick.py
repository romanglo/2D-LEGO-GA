# brick.py


class LegoBrick(object):
    """
    A class used to represent a Lego brick.

    Methods
    -------
    setId(width: int)
        Sets the ID of the Lego brick.
    getId() -> int:
        Gets the ID of the LEGO brick.
    setWidth(width: int)
        Sets the width of the Lego brick.
    getWidth() -> int:
        Gets the width of the LEGO brick.
    setHeight(height: int)
        Sets the height of the Lego brick.
    getHeight() -> int:
        Gets the height of the LEGO brick.
    getArea() -> int:
        Gets the area of the LEGO brick,
        area calculation is with width * height.
    copy() -> LegoBrick :
        Gets a LegoBrick instance with the same attributes.
    """

    NONE_ID = -1

    def __init__(self, width: int, height: int, id: int = NONE_ID):
        """
        LegoBrick constuctor.

        Parameters
        ----------
        width : int
            The brick width.
        height : int
            The brick height.

        Raises
        ------
        ValueError
            If the width or the height isn't bigger then 0.
        """
        self.setWidth(width)
        self.setHeight(height)
        self.__id = id

    def setId(self, id: int):
        """
        Sets the id of the Lego brick.

        Parameters
        ----------
        id : int
            The brick ID.

        """
        self.__id = id

    def getId(self) -> int:
        """
        Gets the ID of the LEGO brick.

        Returns
        -------
        int
            the ID of the LEGO brick.
        """
        return self.__id

    def setWidth(self, width: int):
        """
        Sets the width of the Lego brick.

        Parameters
        ----------
        width : int
            The brick width.

        Raises
        ------
        ValueError
            If the width isn't bigger then 0.
        """
        if (width < 1):
            raise ValueError("width must be bigger then 1!")
        self.__width = width

    def getWidth(self) -> int:
        """
        Gets the width of the LEGO brick.

        Returns
        -------
        int
            the width of the LEGO brick.
        """
        return self.__width

    def setHeight(self, height: int):
        """
        Sets the height of the Lego brick.

        Parameters
        ----------
        height : int
            The brick width.

        Raises
        ------
        ValueError
            If the height isn't bigger then 0.
        """
        if (height < 1):
            raise ValueError("height must be bigger then 1!")
        self.__height = height

    def getHeight(self) -> int:
        """
        Gets the height of the LEGO brick.

        Returns
        -------
        int
            the height of the LEGO brick.
        """
        return self.__height

    def getArea(self) -> int:
        """
        Gets the area of the LEGO brick,
        area calculation is with width * height.

        Returns
        -------
        int
            the area of the LEGO brick.
        """
        return self.__height * self.__width

    def copy(self):
        """
        Gets a LegoBrick instance with the same attributes.

        Returns
        -------
        LegoBrick
            copied instance.
        """
        return LegoBrick(self.__width, self.__height, self.__id)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return self.__toString()

    def __repr__(self):
        return self.__toString()

    def __toString(self) -> str:
        return "LegoBrick[id=%d, width=%d, height=%d, area=%d]" % (
            self.getId(), self.getWidth(), self.getHeight(), self.getArea())
