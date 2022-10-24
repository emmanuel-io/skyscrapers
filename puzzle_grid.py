class PuzzleGrid:
    """
    This class represent a (square) puzzle grid and the methods to access its content
    """

    def __init__(self, size: int = 4, cells: list[list[list[int]]] = None):
        """
        Initialize a puzzle grid instance:

        Parameters
        ----------
        size : int
            The number of cell on each side, it should be superior or equal to 3.
        cells: list[list[int]]
            The intial values to set the cells to as a list (rows) of list (cells) of list (possible values)
        """
        assert size >= 3
        self.size = size
        self.cells = [
            [[(z + 1) for z in range(self.size)] for y in range(self.size)]
            for x in range(self.size)
        ]

    def is_reduced(self) -> bool:
        """
        Check if the puzzle has one value per cell

        Returns
        -------
        bool
            True if solved, else False
        """
        for row in self.cells:
            for cell in row:
                if len(cell) != 1:
                    return False
        return True

    def is_solvable(self) -> bool:
        """
        Check that there are no empty cells in the grid

        Returns
        -------
        bool
            True if it can be solved, else False
        """
        for row in self.cells:
            for cell in row:
                if len(cell) == 0:
                    return False
        return True

    def is_valid(self) -> bool:
        """
        Check if the puzzle has valid values:
        1 of each per line and per row !
        N.B. We assume there is only one value possible per cell !

        Returns
        -------
        bool
            True if valid, else False
        """
        for x in range(self.size):
            col = [self.value_get(x=x, y=y) for y in range(self.size)]
            if (0 in col) or (len(set(col)) != self.size):
                return False
        for y in range(self.size):
            row = [self.value_get(x=x, y=y) for x in range(self.size)]
            if len(set(row)) != self.size:
                return False
        return True

    def value_set(self, x: int, y: int, value: int) -> None:
        """
        Set the value of a cell

        Parameters
        ----------
        x : int
            The abscissa coordinate of the cell
        y : int
            The ordinate coordinate of the cell
        value : int
            The value to which set the cell

        Returns
        -------
        None
            Return nothing
        """
        self.cells[y][x] = [value]

    def value_add(self, x: int, y: int, value: int) -> None:
        """
        Add a value to possible ones to the cell



        Parameters
        ----------
        x : int
            The abscissa coordinate of the cell
        y : int
            The ordinate coordinate of the cell
        value : int
            The value which should be added to the potentiel values of the cell
        """
        if value not in self.cells[y][x]:
            self.cells[y][x].append(value)

    def value_remove(self, x: int, y: int, value: int) -> None:
        """
        Remove a value from the cell

        Parameters
        ----------
        x : int
            The abscissa coordinate of the cell to update
        y : int
            The ordinate coordinate of the cell to update
        value : int
            The value which should be added to the potentiel values of the cell
        """
        values = self.cells[y][x]
        if value in values:
            self.cells[y][x].pop(values.index(value))

    def value_check(self, x: int, y: int, value: int) -> bool:
        """
        Check if a value is in the cell and return True if found, else False

        Parameters
        ----------
        x : int
            The abscissa coordinate of the cell
        y : int
            The ordinate coordinate of the cell

        Returns
        -------
        bool
            Return True is the value is possibly in the cell, else False
        """
        return True if value in self.cells[y][x] else False

    def value_get(self, x: int, y: int) -> int:
        """
        Get the value of the cell, if not sure, return 0

        Parameters
        ----------
        x : int
            The abscissa coordinate of the cell
        y : int
            The ordinate coordinate of the cell

        Returns
        -------
        int
            Return the cell value if there is only one possibility, else 0
        """
        values = self.values_get(x, y)
        if 1 == len(values):
            return values[0]
        else:
            return 0

    def values_get(self, x: int, y: int) -> int:
        """
        Get the possible values of a cell

        Parameters
        ----------
        x : int
            The abscissa coordinate of the cell
        y : int
            The ordinate coordinate of the cell

        Returns
        -------
        int
            Return The value if it is the only possibiitly in the cell, else 0
        """
        return self.cells[y][x]

    def values_clear(self, x: int, y: int) -> None:
        """
        Clear the possible values of a cell

        Parameters
        ----------
        x : int
            The abscissa coordinate of the cell
        y : int
            The ordinate coordinate of the cell
        """
        self.cells[y][x] = []

    def count_reduced_cells(self) -> int:
        """
        Return the number of reduced cells
        """
        count = 0
        for y in range(self.size):
            for x in range(self.size):
                count += 1 if self.value_get(x=x, y=y) != 0 else 0
        return count

    def grid_get(self) -> list[list[list[int]]]:
        """
        Return the grid

        Returns
        -------
        list[list[list[int]]]
            Return the grid
        """
        return self.cells

    def grid_set(self, cells: list[list[list[int]]]) -> None:
        """
        Set the grid content

        Parameters
        ----------
        cells : list[list[list[int]]]
            The grid content as a list of columns of row of possible values
        """
        self.cells = cells

    def __repr__(self):
        if self.is_reduced():
            rows = []
            for row in self.cells[::-1]:
                cols = []
                for col in row:
                    cols.append(str(col[0]))
                rows.append(str(" ".join(cols)))
            return str("\n".join(rows))
        else:
            rows = []
            for row in self.cells[::-1]:
                cols = []
                for col in row:
                    values = ["_" for _i in range(self.size)]
                    for i in col:
                        values[i - 1] = str(i)
                    cols.append(str(" ".join(values)))
                rows.append(str(cols))
            return str("\n".join(rows))
