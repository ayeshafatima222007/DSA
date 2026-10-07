import time
import csv
from funcs import RandomArray,InsertionSort

n=30000
array = RandomArray(n)

startTime = time.time()

array1 = InsertionSort(array,0,n-1)
endTime = time.time()
runtime = endTime-startTime
print(f"runtime of insertion sort is: {runtime}")

file = open("SortedInsertionSort.csv","w")

for number in array1: 
    file.write(str(number) + "\n")
file.close()
 