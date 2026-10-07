array = 0 * 10  # array of length 10 having all zeros
print(array)
#2D array having all zeros
array1 = [[0 for x in range(4)] for y in range(3)]
print(array1)

print("--To Do--")

import numpy as np
array2 = np.zeros((10),dtype=int)
print(array2)

array3 = np.zeros((3,4),dtype=int)
print(array3)