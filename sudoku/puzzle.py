from sudoku import Sudoku
from search import bfs_sudoku, greedy_sudoku
import matplotlib.pyplot as plt

class SudoPuzzle:
    def __init__(self, difficulty=0.5):
        self.dataForPlot = []       # Dùng để lưu expansions_per_step
        self.puzzle = Sudoku(3).difficulty(difficulty)
        self.solution_path = []

    def solve(self, pick_one):
        initial_board = self.puzzle.board
        if pick_one == "1":
            print("Solving with BFS...")
            solution_node, expansions = bfs_sudoku(initial_board)
        elif pick_one == "2":
            print("Solving with Greedy Search...")
            solution_node, expansions = greedy_sudoku(initial_board)
        else:
            print("Invalid option. Defaulting to BFS.")
            solution_node, expansions = bfs_sudoku(initial_board)

        # Lưu expansions vào dataForPlot
        self.dataForPlot = expansions

        if solution_node is not None:
            path = []
            node = solution_node
            while node is not None:
                path.insert(0, node.state)
                node = node.previous
            self.solution_path = path
            print("Solution found! Path length =", len(self.solution_path))
        else:
            print("No solution found!")
            self.solution_path = [initial_board]

    def simulatePlot(self):
        """Hiển thị biểu đồ bar chart dựa trên dữ liệu trong dataForPlot."""
        steps = range(len(self.dataForPlot))
        plt.bar(steps, self.dataForPlot)
        plt.title("Statistics")
        plt.xlabel("Number of step")
        plt.ylabel("Number of searching in step")
        plt.show()
