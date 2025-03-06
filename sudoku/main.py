import tracemalloc
import time
from puzzle import SudoPuzzle
from ui import SudokuUI
from search import bfs_sudoku, greedy_sudoku

def measure_algorithm_run(algorithm, board):
    """
    Đo thời gian chạy và bộ nhớ tiêu thụ khi thực hiện algorithm(board).
    Trả về (elapsed_time, peak_memory, solution_node, expansions_per_step).
    """
    tracemalloc.start()
    start_time = time.time()
    solution_node, expansions = algorithm(board)  # BFS/Greedy đã trả về (node, expansions)
    elapsed_time = time.time() - start_time
    current, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return elapsed_time, peak_memory, solution_node, expansions


if __name__ == '__main__':
    pick_one = input("Solve by BFS or Greedy Search? (1: BFS, 2: Greedy Search): ")

    # Nhập độ khó cho puzzle từ terminal (giá trị từ 0 đến 1)
    try:
        difficulty = float(input("Enter difficulty level for UI (0-1): "))
        if not (0 <= difficulty <= 1):
            print("Difficulty must be between 0 and 1. Using default 0.5")
            difficulty = 0.5
    except ValueError:
        print("Invalid input. Using default difficulty 0.5")
        difficulty = 0.5

    # Khởi tạo puzzle
    sudoku_puzzle = SudoPuzzle(difficulty)
    board = sudoku_puzzle.puzzle.board  # Bảng đề

    # Đo thời gian và bộ nhớ tiêu thụ cho giải thuật
    if pick_one == "1":
        print("Measuring BFS...")
        elapsed, memory, solution_node, expansions = measure_algorithm_run(bfs_sudoku, board)
    elif pick_one == "2":
        print("Measuring Greedy Search...")
        elapsed, memory, solution_node, expansions = measure_algorithm_run(greedy_sudoku, board)
    else:
        print("Invalid option. Defaulting to BFS.")
        elapsed, memory, solution_node, expansions = measure_algorithm_run(bfs_sudoku, board)

    # Gán dataForPlot và solution_path cho puzzle
    sudoku_puzzle.dataForPlot = expansions
    if solution_node is not None:
        path = []
        node = solution_node
        while node is not None:
            path.insert(0, node.state)
            node = node.previous
        sudoku_puzzle.solution_path = path
        print("Solution found! Path length =", len(sudoku_puzzle.solution_path))
    else:
        print("No solution found!")
        sudoku_puzzle.solution_path = [board]

    # Khởi chạy giao diện UI
    sudoku_ui = SudokuUI(sudoku_puzzle)
    sudoku_ui.running()  # Kết thúc khi cửa sổ pygame bị đóng

    # Sau khi tắt UI, in thời gian và bộ nhớ tiêu thụ
    print("\n=== ALGORITHM STATISTICS ===")
    print(f"Elapsed time: {elapsed:.4f} seconds")
    print(f"Peak memory usage: {memory} bytes")
    num_states = sum(sudoku_puzzle.dataForPlot)
    print(f"Number of states: {num_states}")

    # Hỏi người dùng có muốn hiển thị 
    if len(sudoku_puzzle.dataForPlot) > 0:
        t = input("Shall we show statistics about heuristic searching?? (Y: Yes, other: No) ")
        if t.upper() == 'Y':
            sudoku_puzzle.simulatePlot()
