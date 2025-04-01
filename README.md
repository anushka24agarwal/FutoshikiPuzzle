# Futoshiki Puzzle Solver

## Overview

This project implements a solver for the Futoshiki puzzle using the Backtracking Algorithm. Futoshiki is a logic puzzle game played on an NxN grid, similar to Sudoku, but with inequality constraints between some cells.

## Features

- Solves Futoshiki puzzles of any size (NxN grid)

- Implements the Backtracking Algorithm for constraint satisfaction

- Ensures valid solutions that satisfy both unique row/column constraints and given inequalities

- Can be extended to include heuristics for optimization

## How It Works

1. The puzzle is represented as an NxN grid.

2. Given numbers are pre-filled, and inequality constraints are recorded.

3. The solver uses backtracking to try different numbers in empty cells while respecting:
- Row and column uniqueness
- Inequality constraints

4. If a conflict arises, the algorithm backtracks and tries a different number.

5. The process repeats until a valid solution is found.
