import time
import csv
from funcs import RandomArray, HybridMergeSort, InsertionSort, Merge

n = 30000
array = RandomArray(n)
threshold = 15
startTime = time.time()
HybridMergeSort(array,0,n-1,threshold)
endTime = time.time()
runtime = endTime-startTime

print(f"Runtime of hybrid merge sort is: {runtime}")

file = open("SortedHybridSort.csv","w")

for number in array: 
    file.write(str(number) + "\n")
file.close()