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