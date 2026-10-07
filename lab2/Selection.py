import time
import csv
from funcs import RandomArray,SelectionSort

n=30000
array = RandomArray(n)

startTime = time.time()
SelectionSort(array,0,n-1)

endTime = time.time()
runtime = endTime-startTime
print(f"runtime of selection sort is: {runtime}")

file = open("SortedSelectionSort.csv","w")

for number in array: 
    file.write(str(number) + "\n")
file.close()
 