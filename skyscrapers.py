"""
To optimize, each cell is a list of all possible values, if its length is one, we know it's the right value !

Basic clues solving when in front of a line:
If the clue is 1, set the value in front to the max and remove its possibility from others cells in the cline
Else, if the clue is the max value, set all cells in the columns in an ascending order
Else remove the max value from appropriate cells

"""

import time
import logging
from copy import deepcopy
from puzzle_grid import PuzzleGrid


class Skyscrapers:
    """
    This class represent a Skyscraper puzzle with the methods to solve itself
    """

    def __init__(self, size: int = 4, clues: list[int] = []):
        """
        Initialize a skyscrapers puzzle instance:

        Parameters
        ----------
        size : int
            The number of cell on each side, it should be superior or equal to 3.
        clues: list[int]
            The clues seen when looking at the grid, starting from top left corner
             and counted clockwise, if no clues, it is 0
        """
        assert size >= 3
        assert len(clues) == size * 4
        self.size = size
        self.clues_top = clues[0 : self.size]
        self.clues_right = clues[(self.size * 1) : (self.size * 2)][::-1]
        self.clues_bottom = clues[(self.size * 2) : (self.size * 3)][::-1]
        self.clues_left = clues[(self.size * 3) : (self.size * 4)]
        self.grid = PuzzleGrid(size=self.size)
        self.grids = []

    def __solve_basic_clues_top(self) -> None:
        """
        Solve top clues, left to right
        """
        for index, clue in enumerate(self.clues_top):
            if clue == 1:
                self.grid.value_set(x=index, y=(self.size - 1), value=self.size)
                for i in range(self.size - 1):
                    self.grid.value_remove(x=index, y=i, value=self.size)
            elif clue == self.size:
                for i in range(self.size - 1, -1, -1):
                    self.grid.value_set(x=index, y=i, value=(self.size - i))
            elif clue != 0:
                for i in range(self.size - 1, self.size - clue, -1):
                    self.grid.value_remove(x=index, y=i, value=self.size)

    def __solve_basic_clues_bottom(self) -> None:
        """Solve bottom clues, left to right"""
        for index, clue in enumerate(self.clues_bottom):
            if clue == 1:
                self.grid.value_set(x=index, y=0, value=self.size)
                for i in range(1, self.size):
                    self.grid.value_remove(x=index, y=i, value=self.size)
            elif clue == self.size:
                for i in range(self.size):
                    self.grid.value_set(x=index, y=i, value=(i + 1))
            elif clue != 0:
                for i in range(clue - 1):
                    self.grid.value_remove(x=index, y=i, value=self.size)

    def __solve_basic_clues_right(self) -> None:
        """Solve right clues, bottom to top"""
        for index, clue in enumerate(self.clues_right):
            if clue == 1:
                self.grid.value_set(x=(self.size - 1), y=index, value=self.size)
                for i in range(self.size - 1):
                    self.grid.value_remove(x=i, y=index, value=self.size)
            elif clue == self.size:
                for i in range(self.size - 1, -1, -1):
                    self.grid.value_set(x=i, y=index, value=(self.size - i))
            elif clue != 0:
                for i in range(self.size - 1, self.size - clue, -1):
                    self.grid.value_remove(x=i, y=index, value=self.size)

    def __solve_basic_clues_left(self) -> None:
        """Solve left clues, bottom to top"""
        for index, clue in enumerate(self.clues_left):
            if clue == 1:
                self.grid.value_set(x=0, y=index, value=self.size)
                for i in range(1, self.size):
                    self.grid.value_remove(x=i, y=index, value=self.size)
            elif clue == self.size:
                for i in range(self.size):
                    self.grid.value_set(x=i, y=index, value=(i + 1))
            elif clue != 0:
                for i in range(clue - 1):
                    self.grid.value_remove(x=i, y=index, value=self.size)

    def __solve_rows_first(self) -> bool:
        """
        Solve automatically by checking if a value is unique in a row,
        remove it from other places in the same column

        Returns
        -------
        bool
            True if solved something, else False
        """
        solved = False
        for value in range(1, self.size + 1):
            for y in range(self.size):
                row_checks = [
                    self.grid.value_check(x=x, y=y, value=value)
                    for x in range(self.size)
                ]
                if sum(row_checks) == 1:
                    pos_x = row_checks.index(1)
                    col_checks = [
                        self.grid.value_check(x=pos_x, y=y, value=value)
                        for y in range(self.size)
                    ]
                    if sum(col_checks) > 1:
                        solved = True
                        indices = [i for i in range(self.size) if i != y]
                        for pos_y in indices:
                            self.grid.value_remove(x=pos_x, y=pos_y, value=value)
        return solved

    def __solve_cols_first(self) -> bool:
        """
        Solve automatically by checking if a value is unique in a column,
        remove it from other places in the same row

        Returns
        -------
        bool
            True if solved something, else False
        """
        solved = False
        for value in range(1, self.size + 1):
            for x in range(self.size):
                col_checks = [
                    self.grid.value_check(x=x, y=y, value=value)
                    for y in range(self.size)
                ]
                if sum(col_checks) == 1:
                    pos_y = col_checks.index(1)
                    row_checks = [
                        self.grid.value_check(x=x, y=pos_y, value=value)
                        for x in range(self.size)
                    ]
                    if sum(row_checks) > 1:
                        solved = True
                        indices = [i for i in range(self.size) if i != x]
                        for pos_x in indices:
                            self.grid.value_remove(x=pos_x, y=pos_y, value=value)
        return solved

    def __solve_rows_values(self) -> bool:
        """
        Solve automatically by checking if a value is found only once in a row,
        remove all possible values from this cell

        Returns
        -------
        bool
            True if solved something, else False
        """
        solved = False
        for y in range(self.size):
            values_indices = [[] for _i in range(self.size)]
            for x in range(self.size):
                values = self.grid.values_get(x=x, y=y)
                for value in values:
                    values_indices[value - 1].append(x)
            for x in range(self.size):
                if len(values_indices[x]) != 1:
                    continue
                elif 1 == len(self.grid.values_get(x=values_indices[x][0], y=y)):
                    continue
                else:
                    self.grid.value_set(x=values_indices[x][0], y=y, value=(x + 1))
                    solved = True
        return solved

    def __solve_cols_values(self) -> bool:
        """
        Solve automatically by checking if a value is found only once in a column,
        remove all possible values from this cell

        Returns
        -------
        bool
            True if solved something, else False
        """
        solved = False
        for x in range(self.size):
            values_indices = [[] for _i in range(self.size)]
            for y in range(self.size):
                values = self.grid.values_get(x=x, y=y)
                for value in values:
                    values_indices[value - 1].append(y)
            for y in range(self.size):
                if len(values_indices[y]) != 1:
                    continue
                elif 1 == len(self.grid.values_get(x=x, y=values_indices[y][0])):
                    continue
                else:
                    self.grid.value_set(x=x, y=values_indices[y][0], value=(y + 1))
                    solved = True
        return solved

    def __line_values_combine(self, line: list[list[int]]) -> list[int]:
        """From line values return all possible lines combinations"""
        lines_nb = 1
        values_counts = []
        for cell in line:
            values_counts.append(len(cell))
            lines_nb *= len(cell)
        indices = [0] * self.size
        for y in range(lines_nb):
            carry = 1
            for i in range(self.size):
                indices[i] = indices[i] + carry
                if indices[i] == values_counts[i]:
                    indices[i] = 0
                    carry = 1
                else:
                    carry = 0
            temp_line = [line[i][indices[i]] for i in range(self.size)]
            if self.size == len(set(temp_line)):
                yield temp_line

    def __get_skyscrapers_seen(self, values) -> int:
        """From a list of values, return how many skyscrapers are seen"""
        skyscrapers_seen = 0
        height_max = 0
        for height in values:
            if height > height_max:
                skyscrapers_seen += 1
                height_max = height
        return skyscrapers_seen

    def __get_skyscrapers_seen_reverse(self, values) -> int:
        """From a list of values, return how many skyscrapers are seen"""
        skyscrapers_seen = 0
        height_max = 0
        for height in values[::-1]:
            if height > height_max:
                skyscrapers_seen += 1
                height_max = height
        return skyscrapers_seen

    def __reduce_rows_clues(self) -> bool:
        """Solve rows clues, bottom to top"""
        solved = False
        for y in range(self.size):
            clue_left = self.clues_left[y]
            clue_right = self.clues_right[y]
            if (
                (clue_left != 0)
                and (clue_left != self.size)
                or (clue_right != 0)
                and (clue_right != self.size)
            ):
                row = []
                for x in range(self.size):
                    row.append(self.grid.values_get(x=x, y=y))
                # lines = self.line_values_to_lines(row)
                good_values = [[] for _ in range(self.size)]
                for line in self.__line_values_combine(row):
                    check_left = (
                        clue_left == self.__get_skyscrapers_seen(line)
                        if clue_left != 0
                        else True
                    )
                    check_right = (
                        clue_right == self.__get_skyscrapers_seen_reverse(line)
                        if clue_right != 0
                        else True
                    )
                    if check_left and check_right:
                        for j in range(self.size):
                            if line[j] not in good_values[j]:
                                good_values[j].append(line[j])
                for x in range(self.size):
                    self.grid.values_clear(x=x, y=y)
                    for value in good_values[x]:
                        self.grid.value_add(x=x, y=y, value=value)
                    if set(row[x]) != set(self.grid.values_get(x=x, y=y)):
                        solved = True
        return solved

    def __reduce_cols_clues(self) -> bool:
        """Solve columns clues, left to right"""
        solved = False
        for x in range(self.size):
            clue_bottom = self.clues_bottom[x]
            clue_top = self.clues_top[x]
            if (
                (clue_bottom != 0)
                and (clue_bottom != self.size)
                or (clue_top != 0)
                and (clue_top != self.size)
            ):
                col = []
                for y in range(self.size):
                    col.append(self.grid.values_get(x=x, y=y))
                good_values = [[] for _ in range(self.size)]
                for line in self.__line_values_combine(col):
                    check_bottom = (
                        clue_bottom == self.__get_skyscrapers_seen(line)
                        if clue_bottom != 0
                        else True
                    )
                    check_top = (
                        clue_top == self.__get_skyscrapers_seen_reverse(line)
                        if clue_top != 0
                        else True
                    )
                    if check_bottom and check_top:
                        for j in range(self.size):
                            if line[j] not in good_values[j]:
                                good_values[j].append(line[j])
                for y in range(self.size):
                    self.grid.values_clear(x=x, y=y)
                    for value in good_values[y]:
                        self.grid.value_add(x=x, y=y, value=value)
                    if set(col[y]) != set(self.grid.values_get(x=x, y=y)):
                        solved = True
        return solved

    def __check_rows_clues(self) -> bool:
        """Check if row clues are satisfied, bottom to top"""
        for y in range(self.size):
            row = [self.grid.value_get(x=x, y=y) for x in range(self.size)]
            if len(row) != len(set(row)):
                if not self.__get_skyscrapers_seen_reverse(row):
                    return False
            elif self.clues_left[y] != 0:
                if not self.__get_skyscrapers_seen(row):
                    return False
            elif self.clues_right[y] != 0:
                if not self.__get_skyscrapers_seen_reverse(row):
                    return False
        return True

    def __check_cols_clues(self) -> bool:
        """Check if row clues are satisfied, bottom to top"""
        for x in range(self.size):
            col = [self.grid.value_get(x=x, y=y) for y in range(self.size)]
            if len(col) != len(set(col)):
                if not self.__get_skyscrapers_seen_reverse(col):
                    return False
            elif self.clues_bottom[x] != 0:
                if not self.__get_skyscrapers_seen(col):
                    return False
            if self.clues_top[x] != 0:
                if not self.__get_skyscrapers_seen_reverse(col):
                    return False
        return True

    def __solve_by_deduction(self) -> bool:
        """
        Solve automatically by applying multiple logic deduction in a loop

        Returns
        -------
        bool
            True if solved something, else False
        """
        i = 0
        while True:
            t0 = time.time()
            i += 1
            debug_msg = ""
            if self.__solve_rows_values():
                debug_msg = "Solved some rows"
            elif self.__solve_cols_values():
                debug_msg = "Solved some columns"
            elif self.__solve_rows_first():
                debug_msg = "Found a row"
            elif self.__solve_cols_first():
                debug_msg = "Found a column"
            elif self.__reduce_rows_clues():
                debug_msg = "Reduced some rows"
            elif self.__reduce_cols_clues():
                debug_msg = "Reduced some columns"
            else:
                break
            logging.debug(
                f"Loop {i} {debug_msg} in {time.time() - t0} s, {self.grid.count_reduced_cells()} cases reduced."
            )

        if not self.grid.is_solvable():
            logging.debug("Not solvable")
            return False
        elif not self.grid.is_reduced():
            logging.debug("Not reduced")
            return False
        elif not self.__check_rows_clues():
            logging.debug("Rows clues not verified")
            return False
        elif not self.__check_cols_clues():
            logging.debug("Columns clues not verified")
            return False
        else:
            return True

    def __solve_recursive(self, index: int = 0) -> bool:
        """
        Solve by recursively trying with a possible value as long as needed
        Do this until all cells have been tried as a possible start 'bet'

        Returns
        -------
        bool
            True if a solution was found, else False
        """
        logging.debug(f"ENTERING RECURSION {(index + 1)}")
        if self.grid.is_reduced():
            logging.debug("Grid is solved")
            return True

        x = (self.size - 1) - int(index % self.size)
        y = (self.size - 1) - int(index / self.size)

        self.grids.append(deepcopy(self.grid.grid_get()))
        values = self.grid.values_get(x=x, y=y)
        logging.debug(f"Recursion {(index + 1)} => x,y ({x},{y}) values: {values}")

        for value in values:
            self.grid.grid_set(deepcopy(self.grids[index]))
            self.grid.value_set(x=x, y=y, value=value)
            logging.debug(f"Recursion {(index + 1)} => x,y ({x},{y}) value: {value}")
            if self.__solve_by_deduction():
                logging.debug(f"Recursion {(index + 1)} solved by deduction")
                return True
            elif not self.grid.is_solvable():
                logging.debug(f"Recursion {(index + 1)} not solvable")
            elif self.__solve_recursive(index=index + 1):
                logging.debug(f"Recursion {(index + 1)} solved")
                return True

        if ((self.size * self.size) - 1) != index:
            self.__solve_recursive(index=index + 1)
        else:
            logging.debug(f"Recursions failed after all tries")
            return None

    def solve(self) -> bool:
        """
        Solve the puzzle

        Returns
        -------
        bool
            True if a solution was found, else False
        """
        self.__solve_basic_clues_top()
        self.__solve_basic_clues_bottom()
        self.__solve_basic_clues_right()
        self.__solve_basic_clues_left()
        if self.__solve_by_deduction():
            return True
        return self.__solve_recursive()

    def values(self) -> list[list[int]]:
        """
        Return a list (rows) of list (columns) of int

        Returns
        -------
        list[list[int]]
            The values found
        """
        return [
            [self.grid.value_get(x=x, y=y) for x in range(self.size)]
            for y in range(self.size)
        ]

    def __repr__(self):
        return str(self.grid)
