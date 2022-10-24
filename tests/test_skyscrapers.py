import json
import time
from skyscrapers import Skyscrapers

# Maximum time for puzzle solving, adjust to your own configuration !
RESOLUTION_TIME_S = 30.0


def test_skyscrapers():

    with open("./tests/test_data.json", "r") as test_file:
        test_json = json.load(test_file)
    for test_data in test_json:
        puzzle = Skyscrapers(size=test_data["size"], clues=test_data["clues"])
        print(f"Puzzle top clues left to right:    {puzzle.clues_top}")
        print(f"Puzzle bottom clues left to right: {puzzle.clues_bottom}")
        print(f"Puzzle right clues bottom to top:  {puzzle.clues_right}")
        print(f"Puzzle left clues bottom to top:   {puzzle.clues_left}")
        t0 = time.time()
        solved = puzzle.solve()
        resolution_time = time.time() - t0
        if solved:
            print(f"\nPuzzle solved in {resolution_time} s")
        else:
            print(f"\nPuzzle failed in {resolution_time} s")

        print(f"Puzzle final state :\n{puzzle.values()}\n")

        assert test_data["solution"] == puzzle.values()
        assert resolution_time < RESOLUTION_TIME_S
