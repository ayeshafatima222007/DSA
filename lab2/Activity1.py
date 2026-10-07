import time
import csv
from funcs import RandomArray, InsertionSort, MergeSort

n = 500000    #change for every value
array = RandomArray(n)
arrayCopy = array[:]

IstartTime = time.time()
InsertionSort(array,0,n-1)
IendTime = time.time()
Insertruntime = IendTime-IstartTime
print(f"runtime of insertion sort is: {Insertruntime}")

 
MstartTime = time.time()
MergeSort(arrayCopy,0,n-1)
MendTime = time.time()
Mergeruntime = MendTime-MstartTime
print(f"runtime of Merge sort is: {Mergeruntime}")