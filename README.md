# Skyscrapers puzzle

In a grid of N by N squares you want to place a skyscraper in each square with only some clues:
- The height of the skyscrapers is between 1 and N floors.
- No two skyscrapers in a row or column may have the same number of floors.
- A clue is the number of skyscrapers that you can see in a row or column from the outside.
- Higher skyscrapers block the view of lower skyscrapers located behind them.

## Example with N = 4
To understand how the puzzle works, this is an example of a row with 2 clues.
Seen from the left side there are 4 skyscrapers visible while seen from the right side only 1:  
4 - - - - 1
There is only one way in which the skyscrapers can be placed. From left-to-right all four skyscrapers must be visible and no skyscraper may hide behind another skyscraper:
4 1 2 3 4 1
Example of a 4 by 4 puzzle with the solution:

## The clues  

|   |   |   |   |   |   |
|---|---|---|---|---|---|
|   | 0 | 0 | 1 | 2 |   |
| 0 | - | - | - | - | 0 |
| 0 | - | - | - | - | 2 |
| 1 | - | - | - | - | 0 |
| 0 | - | - | - | - | 0 |
|   | 0 | 0 | 3 | 0 |   |

## The solution  

|   |   |   |   |   |   |
|---|---|---|---|---|---|
|   | 3 | 2 | 1 | 2 |   |
| 2 | 2 | 1 | 4 | 3 | 2 |
| 2 | 3 | 4 | 1 | 2 | 2 |
| 1 | 4 | 2 | 3 | 1 | 0 |
| 3 | 1 | 3 | 2 | 4 | 1 |
|   | 2 | 2 | 3 | 1 |   |

## Usage  

When instanciating the class:  
Pass the size N and the clues in a list of 4N items.  
This list contains the clues around the clock, index:

|    |    |    |    |    |    |
|----|----|----|----|----|----|
|    |  0 |  1 |  2 |  3 |    |
| 15 | -- | -- | -- | -- |  4 |
| 14 | -- | -- | -- | -- |  5 |
| 13 | -- | -- | -- | -- |  6 |
| 12 | -- | -- | -- | -- |  7 |
|    | 11 | 10 |  9 |  8 |    |

If no clue is available, add value `0`
Each puzzle has only one possible solution.
`solve_puzzle()` returns a list of 4 lists, each of 4 integers.
The first indexer is for the row, the second indexer for the column.

## DESIGN CONSIDERATIONS

1. The puzzle resolving follows a human thinking approach.  
   - The first stage, basic resolving from clues is done.  
   - The second stage, we loop through a series of values possibility reduction techniques.  
   - Finally if the puzzle can't be solved we choose a value to start with and try recursively until we find a solution or we explored all of them without success.
2. Other approaches are:  
   - Precomputing all the combinations possible. 576 for a size (4).
   - Going brute force, which is pointless when scaling up.
   - Translating the problem to use a [SAT solver](https://www.cs.ru.nl/bachelors-theses/2022/Laura_Kolijn___1025724___Generating_and_Solving_Skyscrapers_Puzzles_Using_a_SAT_Solver.pdf)

## TESTING

1. This solution uses pytest for testing (which is the only dependency).
2. There is a timing constraint **RESOLUTION_TIME_S** in ./tests/test_skyscrapers.py  
   You might edit it according to your own configuration.
