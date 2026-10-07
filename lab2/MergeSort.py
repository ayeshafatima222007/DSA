import time
import csv
from funcs import RandomArray,MergeSort,Merge

n=30000
array = RandomArray(n)

startTime = time.time()
MergeSort(array,0,n-1)

endTime = time.time()
runtime = endTime-startTime
print(f"runtime of merge sort is: {runtime}")

file = open("SortedMergeSort.csv","w")

for number in array: 
    file.write(str(number) + "\n")
file.close()
 