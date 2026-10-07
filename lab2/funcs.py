#---Problem 1---
import random
def RandomArray(size):
    Arr = []
    for i in range(size):
        Arr.append(random.randint(1, 100))
    return Arr

#---Problem 2---
def InsertionSort(array, start, end):
    for i in range(start + 1, end + 1):
        key = array[i]
        j = i - 1
        while j >= start and array[j] > key:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key
    return array


#---Problem 3---
def MergeSort(array,start,end):
    if start<end:
        mid=(start+end)//2

        MergeSort(array,start,mid)
        MergeSort(array,mid+1,end)

        Merge(array, start, mid, end)


def Merge(array,start,mid,end):
    left = array[start:mid+1]
    right = array [mid+1:end+1]
    new= []
    i, j = 0, 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            new.append(left[i])
            i += 1
        else:
            new.append(right[j])
            j += 1

    new.extend(left[i:])
    new.extend(right[j:])

    for k in range(len(new)):
        array[start + k] = new[k]


#---Problem 4---
def HybridMergeSort(array, start, end, threshold):
    size = end - start + 1
    if size <= threshold:
        InsertionSort(array,start,end)
    else:
        mid = (start + end) // 2
        HybridMergeSort(array, start, mid, threshold)
        HybridMergeSort(array, mid+1, end, threshold)
        Merge(array, start, mid, end)



#---Problem 5---
def BubbleSort(array,start,end):
    for i in range(start,end):
        for j in range(start,end-i):
            if array[j] > array[j+1]:
                array[j],array[j+1]=array[j+1],array[j]


#---Problem 6---
def SelectionSort(array, start, end):
    for i in range(start, end):
        mini = i
        for j in range(i+1, end+1):
            if array[j] < array[mini]:
                mini = j
        array[i], array[mini] = array[mini], array[i]


#---Problem 8---
def ShuffleArray(array, start, end):
    for i in range(end, start, -1):
        j = random.randint(start, i)
        array[i], array[j] = array[j], array[i]