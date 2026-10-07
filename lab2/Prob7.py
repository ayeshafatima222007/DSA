from funcs import RandomArray, InsertionSort, MergeSort, HybridMergeSort,BubbleSort, SelectionSort
import time
import csv

file = open("Nvalues.txt", "r")
Nvalues = []
for number in file:
    num = int(number)
    Nvalues.append(num)
file.close()

results = []
threshold = 15

for n in Nvalues:
    array = RandomArray(n)     #making random array

    InsertionCopy = array[:]   #making copies for each sorting
    MergeCopy = array[:]
    BubbleCopy = array[:]
    SelectionCopy = array[:]
    HybridCopy = array[:]


    #--Insertion Sort--
    IstartTime = time.time() 
    InsertionSort(InsertionCopy,0,n-1)
    IendTime = time.time()
    Insertruntime = IendTime-IstartTime
    print(f"runtime of insertion sort is: {Insertruntime} ")


    #--Merge Sort--
    MstartTime = time.time()
    MergeSort(MergeCopy,0,n-1)
    MendTime = time.time()
    Mergeruntime = MendTime-MstartTime
    print(f"runtime of Merge sort is: {Mergeruntime} ")

    #--Hybrid Merge Sort--
    HstartTime = time.time()
    HybridMergeSort(HybridCopy,0,n-1,threshold)
    HendTime = time.time()
    Hybridruntime = HendTime-HstartTime
    print(f"runtime of hybrid merge sort is: {Hybridruntime} ")


    #--Selection Sort--
    SstartTime = time.time()
    SelectionSort(SelectionCopy,0,n-1)
    SendTime = time.time()
    Selectionruntime = SendTime-SstartTime
    print(f"runtime of selection sort is: {Selectionruntime}")

    #--Bubble Sort--
    BstartTime = time.time()
    BubbleSort(BubbleCopy,0,n-1)
    BendTime = time.time()
    Bubbleruntime = BendTime-BstartTime
    print(f"runtime of bubble sort is: {Bubbleruntime}\n")

       
    results.append([n, Insertruntime, Mergeruntime, Hybridruntime , Selectionruntime, Bubbleruntime])

file = open("RunTime.csv", "w", newline="")
writer = csv.writer(file)
writer.writerow(["n", "Insertion Sort", "Merge Sort", "Hybrid Merge Sort" , "Selection Sort" , "Bubble Sort"])
for row in results:
    writer.writerow(row)
file.close()
    
