import tkinter as tk
from tkinter import messagebox
from collections import deque


class PuzzleSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver")
        self.start_grid = []
        self.goal_grid = []
        self.grid_entries = []
        self.solution = []

        self.setup_ui()

    def setup_ui(self):
        # Title labels
        tk.Label(self.root, text="Enter Start State").grid(row=0, column=0, columnspan=3)
        tk.Label(self.root, text="Enter Goal State").grid(row=0, column=3, columnspan=3)

        # Grid entries for Start and Goal states
        self.grid_entries = [[tk.Entry(self.root, width=3, font=("Arial", 18)) for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.grid_entries[i][j].grid(row=i + 1, column=j)
        self.goal_entries = [[tk.Entry(self.root, width=3, font=("Arial", 18)) for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.goal_entries[i][j].grid(row=i + 1, column=j + 3)

        # Solve button
        tk.Button(self.root, text="Solve Puzzle", command=self.solve_puzzle).grid(row=4, column=0, columnspan=6)

        # Reset button
        tk.Button(self.root, text="Reset", command=self.reset_ui).grid(row=5, column=0, columnspan=6)

    def parse_grid(self, entries):
        grid = []
        used_numbers = set()
        try:
            for row in entries:
                grid_row = []
                for cell in row:
                    num = int(cell.get())
                    if num < 0 or num > 8 or num in used_numbers:
                        raise ValueError
                    used_numbers.add(num)
                    grid_row.append(num)
                grid.append(grid_row)
            if len(used_numbers) != 9:
                raise ValueError
            return grid
        except ValueError:
            messagebox.showerror("Error", "Invalid grid input. Ensure numbers 0-8 are used exactly once.")
            return None

    def solve_puzzle(self):
        self.start_grid = self.parse_grid(self.grid_entries)
        self.goal_grid = self.parse_grid(self.goal_entries)

        if not self.start_grid or not self.goal_grid:
            return

        if not self.is_solvable(self.start_grid, self.goal_grid):
            messagebox.showerror("Unsolvable", "The puzzle configuration is unsolvable. Modify the inputs.")
            return

        self.solution = self.solve_game_bfs(self.start_grid, self.goal_grid)
        if self.solution:
            messagebox.showinfo("Solution", f"Solution found! Steps: {len(self.solution)}")
            self.show_solution()
        else:
            messagebox.showerror("Error", "No solution found.")

    def reset_ui(self):
        for row in self.grid_entries + self.goal_entries:
            for cell in row:
                cell.delete(0, tk.END)

    def is_solvable(self, start, goal):
        def count_inversions(state):
            flat_list = [num for row in state for num in row if num != 0]
            inversions = sum(1 for i in range(len(flat_list)) for j in range(i + 1, len(flat_list)) if flat_list[i] > flat_list[j])
            return inversions

        start_inversions = count_inversions(start)
        goal_inversions = count_inversions(goal)
        return start_inversions % 2 == goal_inversions % 2

    def solve_game_bfs(self, start, goal):
        start = tuple(tuple(row) for row in start)
        goal = tuple(tuple(row) for row in goal)

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        queue = deque([(start, [])])
        visited = set()
        visited.add(start)

        while queue:
            current, path = queue.popleft()

            if current == goal:
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

        return None

    def show_solution(self):
        for step, (zr, zc, nr, nc) in enumerate(self.solution, 1):
            self.start_grid[zr][zc], self.start_grid[nr][nc] = self.start_grid[nr][nc], self.start_grid[zr][zc]
            self.update_ui(self.start_grid)
            self.root.update()
            self.root.after(500)

    def update_ui(self, grid):
        for i, row in enumerate(grid):
            for j, value in enumerate(row):
                self.grid_entries[i][j].delete(0, tk.END)
                self.grid_entries[i][j].insert(0, value)


if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleSolverApp(root)
    root.mainloop()
