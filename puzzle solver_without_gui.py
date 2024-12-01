from tkinter import messagebox
import tkinter as tk
from collections import deque

game = []
goal = []

def print_game_state(state):
    for row in state:
        print(" ".join(map(str, row)))
    print("\n")

def count_inversions(state):
    flat_list = [num for row in state for num in row if num != 0]
    inversions = 0
    for i in range(len(flat_list)):
        for j in range(i + 1, len(flat_list)):
            if flat_list[i] > flat_list[j]:
                inversions += 1
    return inversions

def is_solvable(start, goal):
    start_inversions = count_inversions(start)
    goal_inversions = count_inversions(goal)
    return start_inversions % 2 == goal_inversions % 2

def solve_game_bfs(start, goal):
    start = tuple(tuple(row) for row in start)
    goal = tuple(tuple(row) for row in goal)

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = deque([(start, [])])
    visited = set()
    visited.add(start)
    state = 1

    while queue:
        current, path = queue.popleft()

        print("Current State:", state)
        print_game_state(current)
        state += 1

        if current == goal:
            print("Goal State Reached:")
            print_game_state(current)
            return path

        zero_row, zero_col = [(r, c) for r in range(3) for c in range(3) if current[r][c] == 0][0]

        for dr, dc in directions:
            new_row, new_col = zero_row + dr, zero_col + dc

            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_state = [list(row) for row in current]
                new_state[zero_row][zero_col], new_state[new_row][new_col] = (
                    new_state[new_row][new_col],
                    new_state[zero_row][zero_col],
                )
                new_state = tuple(tuple(row) for row in new_state)

                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, path + [(zero_row, zero_col, new_row, new_col)]))

    print("No solution found.")
    return None

def get_valid_grid_input(grid, prompt):
    while True:
        print(f"Enter numbers from 1 to 8 and 0 for the null space (only one 0 allowed): [{prompt}]")
        temp_grid = []
        nums_used = set()

        for i in range(3):
            row = []
            for j in range(3):
                while True:
                    for r in temp_grid:
                        print(r)
                    num = input(f"Enter number for position ({i + 1}, {j + 1}): ")

                    if num.isdigit() and int(num) in range(0, 9):
                        num = int(num)

                        if num in nums_used:
                            print(f"The number {num} has already been used. Try again.")
                        else:
                            nums_used.add(num)
                            row.append(num)
                            break
                    else:
                        print("Invalid input. Please enter a number between 0 and 8.")
            temp_grid.append(row)

        # Check if all numbers 0-8 are used exactly once
        if set(nums_used) == set(range(9)):
            return temp_grid
        else:
            print("Invalid grid. Please ensure all numbers from 0 to 8 are used exactly once.")

# Input start and goal grids
game = get_valid_grid_input(game, "START")
goal = get_valid_grid_input(goal, "GOAL")

print("\nFinal Initial 3x3 grid:")
for r in game:
    print(r)

print("\nFinal Goal 3x3 grid:")
for r in goal:
    print(r)

input("Press Enter to continue...")

if is_solvable(game, goal):
    solution = solve_game_bfs(game, goal)
    if solution:
        print("Solution found!")
    else:
        print("Unexpected: No solution found.")
else:
    print("The puzzle is not solvable.")

root = tk.root()
root.withdraw()
messagebox.showinfo("Solution", "Solution found!")