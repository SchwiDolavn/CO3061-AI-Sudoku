from queue import Queue
import copy
import heapq
from state_and_node import Node

def is_goal(matrix):
    for row in matrix:
        if 0 in row:
            return False
    return True

class Problem:
    def __init__(self, initial):
        self.initial = [[cell if cell is not None else 0 for cell in row] for row in initial]
        self.size = len(self.initial)
        self.block_size = int(self.size ** 0.5)

    def get_possible_moves(self, matrix):
        n = self.size
        for i in range(n):
            for j in range(n):
                if matrix[i][j] == 0:
                    possible = set(range(1, n + 1))
                    # Loại bỏ số đã xuất hiện trong hàng i
                    for k in range(n):
                        if matrix[i][k] in possible:
                            possible.remove(matrix[i][k])
                    # Loại bỏ số đã xuất hiện trong cột j
                    for k in range(n):
                        if matrix[k][j] in possible:
                            possible.remove(matrix[k][j])
                    # Loại bỏ số đã xuất hiện trong block
                    br = (i // self.block_size) * self.block_size
                    bc = (j // self.block_size) * self.block_size
                    for r in range(br, br + self.block_size):
                        for c in range(bc, bc + self.block_size):
                            if matrix[r][c] in possible:
                                possible.remove(matrix[r][c])
                    return i, j, list(possible)
        return None, None, []

    def result(self, matrix, action):
        row, col, digit = action
        new_matrix = copy.deepcopy(matrix)
        new_matrix[row][col] = digit
        return new_matrix

def BFS(problem: Problem):
    """
    Thực hiện tìm kiếm theo BFS cho Sudoku.
    Trả về (solution_node, expansions_per_step).
    expansions_per_step là list, index = step, value = số node được lấy ra khỏi frontier ở step đó.
    """
    root = Node(problem.initial)
    if is_goal(root.state):
        return root, [1]

    frontier = Queue()
    frontier.put(root)
    visited = set()

    expansions_per_step = []

    while not frontier.empty():
        node = frontier.get()
        # Bảo đảm expansions_per_step đủ độ dài
        while len(expansions_per_step) <= node.step:
            expansions_per_step.append(0)
        expansions_per_step[node.step] += 1

        state_tuple = tuple(tuple(row) for row in node.state)
        if state_tuple in visited:
            continue
        visited.add(state_tuple)

        if is_goal(node.state):
            return node, expansions_per_step

        row, col, moves = problem.get_possible_moves(node.state)
        for digit in moves:
            action = (row, col, digit)
            new_matrix = problem.result(node.state, action)
            child = Node(new_matrix, previous=node, action=action)
            frontier.put(child)

    return None, expansions_per_step

def bfs_sudoku(board):
    problem = Problem(board)
    return BFS(problem)  # trả về (solution_node, expansions_per_step)

def heuristic(matrix):
    return sum(row.count(0) for row in matrix)

def greedy_sudoku(board):
    """
    Trả về (solution_node, expansions_per_step) tương tự BFS.
    expansions_per_step[step] = số node được lấy ra khỏi frontier ở step.
    """
    from state_and_node import Node

    problem = Problem(board)
    root = Node(problem.initial)
    expansions_per_step = []

    frontier = []
    counter = 0
    heapq.heappush(frontier, (heuristic(root.state), counter, root))
    visited = set()

    while frontier:
        h_val, _, node = heapq.heappop(frontier)
        while len(expansions_per_step) <= node.step:
            expansions_per_step.append(0)
        expansions_per_step[node.step] += 1

        if is_goal(node.state):
            return node, expansions_per_step

        state_tuple = tuple(tuple(row) for row in node.state)
        if state_tuple in visited:
            continue
        visited.add(state_tuple)

        row, col, moves = problem.get_possible_moves(node.state)
        for digit in moves:
            counter += 1
            action = (row, col, digit)
            new_matrix = problem.result(node.state, action)
            child = Node(new_matrix, previous=node, action=action)
            heapq.heappush(frontier, (heuristic(child.state), counter, child))

    return None, expansions_per_step
