import time
import csv
from funcs import RandomArray, BubbleSort

n = 30000
array = RandomArray(n)

startTime = time.time()
BubbleSort(array,0,n-1)
endTime = time.time()
runtime = endTime-startTime
print(f"The runtime for bubble sort is: {runtime}")

file = open("SortedBubbleSort.csv","w")

for number in array: 
    file.write(str(number) + "\n")
file.close()