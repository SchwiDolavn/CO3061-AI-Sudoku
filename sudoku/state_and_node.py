import copy
import math

class State:
    def __init__(self, matrix: list) -> None:
        # Lưu trữ ma trận dưới dạng copy để không làm thay đổi gốc
        self.matrix = copy.deepcopy(matrix)
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, State):
            return self.matrix == other.matrix
        return False

    def __str__(self) -> str:
        s = ""
        for row in self.matrix:
            s += " ".join(str(x) for x in row) + "\n"
        return s

class Node:
    def __init__(self, state: State, previous=None, action=None) -> None:
        """
        state: Một đối tượng State chứa ma trận Sudoku (2D list)
        previous: Node cha (để truy vết chuỗi các bước)
        action: Tuple (row, col, digit) thể hiện hành động điền số vào ô (row, col)
        """
        self.state = state
        self.previous = previous
        self.action = action
        self.step = 0 if previous is None else previous.step + 1

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Node):
            return self.state == other.state
        return False

    def __bool__(self) -> bool:
        return bool(self.state.matrix)

    def get_possible(self, row: int, col: int) -> list:
        """
        Trả về danh sách các số hợp lệ để điền vào ô (row, col) dựa theo quy tắc Sudoku:
         - Không trùng số trong hàng, cột và khối vuông.
        """
        matrix = self.state.matrix
        n = len(matrix)  # Với Sudoku chuẩn, n = 9
        possible = set(range(1, n+1))
        # Loại bỏ số đã xuất hiện trong hàng row
        for j in range(n):
            if matrix[row][j] in possible:
                possible.remove(matrix[row][j])
        # Loại bỏ số đã xuất hiện trong cột col
        for i in range(n):
            if matrix[i][col] in possible:
                possible.remove(matrix[i][col])
        # Loại bỏ số đã xuất hiện trong khối vuông
        block_size = int(math.sqrt(n))
        start_row = (row // block_size) * block_size
        start_col = (col // block_size) * block_size
        for i in range(start_row, start_row + block_size):
            for j in range(start_col, start_col + block_size):
                if matrix[i][j] in possible:
                    possible.remove(matrix[i][j])
        return list(possible)

    def expand(self) -> list:
        """
        Sinh các Node con từ node hiện tại bằng cách:
         1. Tìm ô trống đầu tiên (ô có giá trị 0) trong ma trận.
         2. Với ô đó, duyệt các số hợp lệ (theo get_possible).
         3. Với mỗi số, tạo một ma trận mới, điền số đó vào ô và tạo Node con.
        Trả về danh sách các Node con.
        """
        children = []
        matrix = self.state.matrix
        n = len(matrix)
        found = False
        for i in range(n):
            for j in range(n):
                if matrix[i][j] == 0:
                    row, col = i, j
                    found = True
                    break
            if found:
                break
        if not found:
            return []  # Board đã đầy

        possible_digits = self.get_possible(row, col)
        for digit in possible_digits:
            new_matrix = copy.deepcopy(matrix)
            new_matrix[row][col] = digit
            child_state = State(new_matrix)
            child_node = Node(child_state, previous=self, action=(row, col, digit))
            children.append(child_node)
        return children
