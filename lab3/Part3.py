#---Task 1---
def printMatrix(A, starting_index, rows, columns):
    r0, c0 = starting_index
    for i in range(r0, r0 + rows):
        line = ''
        for j in range(c0, c0 + columns):
            line += str(A[i][j]) + ' '
        print(line.rstrip())

A = [[1, 2, 3, 4, 5, 6, 7],
     [8, 9, 1, 2, 3, 4, 5],
     [6, 7, 8, 9, 3, 4, 5],
     [2, 4, 6, 8, 2, 5, 7]]

printMatrix(A, (2, 4), 2, 3)

#---Task 2---
def MatAdd(A, B):
    rows = len(A)
    cols = len(A[0])
    C = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(A[i][j] + B[i][j])
        C.append(row)
    return C 

X = [[1, 2, 3],
     [4, 5, 6]]
Y = [[5, 6, 7],
     [1, 2, 3]]

printMatrix(MatAdd(X, Y), (0, 0), 2, 3)

#---Task 3---
def MatAddPartial(A, B, start, size):
    x, y = start
    C = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(A[x + i][y + j] + B[x + i][y + j])
        C.append(row)
    return C

A = [[1, 2, 3, 4, 5],
     [6, 7, 8, 9, 1],
     [2, 3, 4, 5, 6],
     [7, 8, 9, 1, 2]]

B = [[1, 1, 1, 1, 1],
     [2, 2, 2, 2, 2],
     [3, 3, 3, 3, 3],
     [4, 4, 4, 4, 4]]

printMatrix(MatAddPartial(A, B, (2, 3), 2), (0, 0), 2, 2)


#---Task 4---
def MatMul(A, B):
    n = len(A)        # A ki rows
    k = len(B)        # A ke columns = B ki rows
    m = len(B[0])     # B ke columns
    C = []
    for i in range(n):
        row = []
        for j in range(m):
            total = 0
            for t in range(k):
                total += A[i][t] * B[t][j]
            row.append(total)
        C.append(row)
    return C

A = [[1, 2],
     [3, 4]]
B = [[5, 6],
     [7, 8]]

printMatrix(MatMul(A, B), (0, 0), 2, 2)

#---Task 5---
def getSubMatrix(matrix, start_row, start_col, size):
    # Extract the size x size block that starts at (start_row, start_col)
    sub_matrix = []
    for i in range(size):
        sub_matrix.append(matrix[start_row + i][start_col:start_col + size])
    return sub_matrix


def placeSubMatrix(result, sub_matrix, start_row, start_col):
    # Copy the block into result, starting at (start_row, start_col)
    for i in range(len(sub_matrix)):
        for j in range(len(sub_matrix)):
            result[start_row + i][start_col + j] = sub_matrix[i][j]


def MatMulRecursive(A, B):
    size = len(A)

    # Base case: a single number, so multiply directly
    if size == 1:
        return [[A[0][0] * B[0][0]]]

    half = size // 2

    # Split A into 4 blocks
    A_top_left = getSubMatrix(A, 0, 0, half)
    A_top_right = getSubMatrix(A, 0, half, half)
    A_bottom_left = getSubMatrix(A, half, 0, half)
    A_bottom_right = getSubMatrix(A, half, half, half)

    # Split B into 4 blocks
    B_top_left = getSubMatrix(B, 0, 0, half)
    B_top_right = getSubMatrix(B, 0, half, half)
    B_bottom_left = getSubMatrix(B, half, 0, half)
    B_bottom_right = getSubMatrix(B, half, half, half)

    # Each block of the result = sum of 2 smaller multiplications (8 in total)
    result_top_left = MatAdd(MatMulRecursive(A_top_left, B_top_left),
                             MatMulRecursive(A_top_right, B_bottom_left))
    result_top_right = MatAdd(MatMulRecursive(A_top_left, B_top_right),
                              MatMulRecursive(A_top_right, B_bottom_right))
    result_bottom_left = MatAdd(MatMulRecursive(A_bottom_left, B_top_left),
                                MatMulRecursive(A_bottom_right, B_bottom_left))
    result_bottom_right = MatAdd(MatMulRecursive(A_bottom_left, B_top_right),
                                 MatMulRecursive(A_bottom_right, B_bottom_right))

    # Join the 4 result blocks into the full result matrix
    result = [[0] * size for _ in range(size)]
    placeSubMatrix(result, result_top_left, 0, 0)
    placeSubMatrix(result, result_top_right, 0, half)
    placeSubMatrix(result, result_bottom_left, half, 0)
    placeSubMatrix(result, result_bottom_right, half, half)
    return result

printMatrix(MatMulRecursive(A, B), (0, 0), 2, 2)


#---Task 6---
def MatSub(A, B):
    # Subtract B from A, element by element
    rows = len(A)
    cols = len(A[0])
    C = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(A[i][j] - B[i][j])
        C.append(row)
    return C

def MatMulStrassen(A, B):
    size = len(A)

    # Base case: a single number, so multiply directly
    if size == 1:
        return [[A[0][0] * B[0][0]]]

    half = size // 2

    # Split A into 4 blocks
    A_top_left = getSubMatrix(A, 0, 0, half)
    A_top_right = getSubMatrix(A, 0, half, half)
    A_bottom_left = getSubMatrix(A, half, 0, half)
    A_bottom_right = getSubMatrix(A, half, half, half)

    # Split B into 4 blocks
    B_top_left = getSubMatrix(B, 0, 0, half)
    B_top_right = getSubMatrix(B, 0, half, half)
    B_bottom_left = getSubMatrix(B, half, 0, half)
    B_bottom_right = getSubMatrix(B, half, half, half)

    # Only 7 multiplications (the normal recursive method needs 8)
    product_1 = MatMulStrassen(MatAdd(A_top_left, A_bottom_right), MatAdd(B_top_left, B_bottom_right))
    product_2 = MatMulStrassen(MatAdd(A_bottom_left, A_bottom_right), B_top_left)
    product_3 = MatMulStrassen(A_top_left, MatSub(B_top_right, B_bottom_right))
    product_4 = MatMulStrassen(A_bottom_right, MatSub(B_bottom_left, B_top_left))
    product_5 = MatMulStrassen(MatAdd(A_top_left, A_top_right), B_bottom_right)
    product_6 = MatMulStrassen(MatSub(A_bottom_left, A_top_left), MatAdd(B_top_left, B_top_right))
    product_7 = MatMulStrassen(MatSub(A_top_right, A_bottom_right), MatAdd(B_bottom_left, B_bottom_right))

    # Combine the 7 products into the 4 blocks of the result
    result_top_left = MatAdd(MatSub(MatAdd(product_1, product_4), product_5), product_7)
    result_top_right = MatAdd(product_3, product_5)
    result_bottom_left = MatAdd(product_2, product_4)
    result_bottom_right = MatAdd(MatSub(MatAdd(product_1, product_3), product_2), product_6)

    # Join the 4 result blocks into the full result matrix
    result = [[0] * size for _ in range(size)]
    placeSubMatrix(result, result_top_left, 0, 0)
    placeSubMatrix(result, result_top_right, 0, half)
    placeSubMatrix(result, result_bottom_left, half, 0)
    placeSubMatrix(result, result_bottom_right, half, half)
    return result

printMatrix(MatMulStrassen(A,B), (0, 0), 2, 2)