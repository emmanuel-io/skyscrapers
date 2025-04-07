# 🏙️ Skyscrapers Puzzle Solver (Python)

A Python-based solver for the classic **Skyscrapers logic puzzle** using human-like reasoning strategies and constraint reduction techniques.

---

## 🧠 Puzzle Rules Recap

- Each row and column must contain **unique building heights** from 1 to N.  
- **Clues** around the grid show how many skyscrapers are visible from that side.  
- A **taller building hides** shorter ones behind it.  

---

## 🔢 Example (N = 4)

A row:  
Seen from the left (4 visible), right (1 visible):  
```
4 | 1 2 3 4 | 1
```

### The clues  

|   |   |   |   |   |   |
|---|---|---|---|---|---|
|   | 0 | 0 | 1 | 2 |   |
| 0 | - | - | - | - | 0 |
| 0 | - | - | - | - | 2 |
| 1 | - | - | - | - | 0 |
| 0 | - | - | - | - | 0 |
|   | 0 | 0 | 3 | 0 |   |

### The solution  

|   |   |   |   |   |   |
|---|---|---|---|---|---|
|   | 3 | 2 | 1 | 2 |   |
| 2 | 2 | 1 | 4 | 3 | 2 |
| 2 | 3 | 4 | 1 | 2 | 2 |
| 1 | 4 | 2 | 3 | 1 | 0 |
| 3 | 1 | 3 | 2 | 4 | 1 |
|   | 2 | 2 | 3 | 1 |   |


---

## 🚀 Usage

```python
from skyscrapers import Skyscrapers

clues = [
  0, 0, 1, 2,  # top clues (left to right)
  0, 2, 0, 0,  # right clues (top to bottom)
  0, 0, 3, 0,  # bottom clues (right to left)
  0, 1, 0, 0,  # left clues (bottom to top)
]

solver = Skyscrapers(4, clues)
solution = solver.solve_puzzle()
```

- The `clues` list is **4 × N** elements, starting top and going clockwise.
- `solve_puzzle()` returns a 2D list: one row per line, with each cell containing a height from 1 to N.

---

## 🧰 Solver Logic

1. 🔍 **Clue-based deduction**: Starts with direct implications from each clue.  
2. 🧠 **Constraint propagation**: Iteratively eliminates impossible values from the grid.  
3. 🧪 **Backtracking**: If needed, guesses are made and tested recursively.  

Alternatives like brute force, precomputing permutations, or using a SAT solver are discussed in academic references (e.g. [SAT solver paper](https://www.cs.ru.nl/bachelors-theses/2022/Laura_Kolijn___1025724___Generating_and_Solving_Skyscrapers_Puzzles_Using_a_SAT_Solver.pdf)).

---

## ✅ Requirements

- Python 3.8+  
- `pytest` (for tests only)

---

## 🧪 Testing

Run all tests:

```bash
pytest
```

The file `./tests/test_skyscrapers.py` includes a time constraint `RESOLUTION_TIME_S` which you can adjust depending on your system.

---

## 📜 License

This project is open-source under the MIT License.

---

## 👤 Author

**Emmanuel Amadio**  
🌍 [Website](https://emmanuel-io.github.io/en)  
🐙 [GitHub](https://github.com/emmanuel-io)

---

> Inspired by logic puzzle enthusiasts and designed to mimic how a human would approach the game.
