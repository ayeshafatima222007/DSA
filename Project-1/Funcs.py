#----Insertion Sort----
def InsertionSort(array, start, end):
    for i in range(start + 1, end + 1):
        key = array[i]
        j = i - 1
        while j >= start and array[j] > key:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key
    return array


#----Merge Sort----
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


#----HybridMergeSort----
def HybridMergeSort(array, start, end, threshold):
    size = end - start + 1
    if size <= threshold:
        InsertionSort(array,start,end)
    else:
        mid = (start + end) // 2
        HybridMergeSort(array, start, mid, threshold)
        HybridMergeSort(array, mid+1, end, threshold)
        Merge(array, start, mid, end)



#----Bubble Sort----
def BubbleSort(array,start,end):
    for i in range(start,end):
        for j in range(start,end-i):
            if array[j] > array[j+1]:
                array[j],array[j+1]=array[j+1],array[j]


#----Selection Sort----
def SelectionSort(array, start, end):
    for i in range(start, end):
        mini = i
        for j in range(i+1, end+1):
            if array[j] < array[mini]:
                mini = j
        array[i], array[mini] = array[mini], array[i]

#----Quick Sort----
def Partition(A,p,r):
    x = A[r]
    i = p-1
    for j in range (p,r):
        if A[j] <= x:
            i = i+1
            A[i],A[j] = A[j],A[i]
    A[i+1],A[r] = A[r],A[i+1]
    return i+1

def QuickSort(A,p,r):
    if p < r:
        q = Partition(A,p,r)
        QuickSort(A,p,q-1)
        QuickSort(A,q+1,r)

 
#----Counting Sort----
def counting_sort(arr):
    if not arr:
        return []

    k = max(arr) - min(arr)                      #range of values
    count = [0] * (k + 1)
    output = [0] * len(arr)

    for x in arr:                    #count each value
        count[x - min(arr)] += 1

    for i in range(1, k + 1):        #running total = final positions
        count[i] += count[i - 1]

    for i in range(len(arr) - 1, -1, -1):   #place items, going backwards
        j = arr[i] - min(arr)
        count[j] -= 1
        output[count[j]] = arr[i]

    return output


#----Radix Sort----
def counting_sort_by_digit(arr,a):
    n = len(arr)
    output = [0] * n
    count = [0] * 10                       #digits 0-9

    for x in arr:                       #count each digit
        count[(x // a) % 10] += 1

    for i in range(1, 10):          #running total
        count[i] += count[i - 1]

    for i in range(n - 1, -1, -1):         #place backwards(stable sort)
        d = (arr[i] // a) % 10
        count[d] -= 1
        output[count[d]] = arr[i]

    return output


def radix_sort(arr):
    if not arr:
        return []
    result = list(arr)
    a = 1                     # 1=ones,10=tens,100=hundreds
    biggest = max(result)
    while biggest // a > 0:
        result = counting_sort_by_digit(result, a)
        a *= 10
    return result


#----Bucket Sort----
def insertion_sort(bucket):
    for i in range(1, len(bucket)):
        v = bucket[i]
        j = i - 1
        while j >= 0 and bucket[j] > v:
            bucket[j + 1] = bucket[j]
            j -= 1
        bucket[j + 1] = v
    return bucket


def bucket_sort(arr):
    n = len(arr)
    if n == 0:
        return []

    buckets = [[] for _ in range(n)]       #create n empty buckets

    for x in arr:             #put arr[i] in bucket[n * arr[i]]
        buckets[int(n * x)].append(x)

    for b in buckets:               #sort each bucket (insertion sort)
        insertion_sort(b)

    result = []                            #join all buckets in order
    for b in buckets:
        result.extend(b)
    return result


#----Heap Sort----
def Heapify(array, start, size, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < size and array[start + left] > array[start + largest]:
        largest = left
    if right < size and array[start + right] > array[start + largest]:
        largest = right

    if largest != i:
        array[start + i], array[start + largest] = array[start + largest], array[start + i]
        Heapify(array, start, size, largest)


def HeapSort(array, start, end):
    n = end - start + 1
    for i in range(n // 2 - 1, -1, -1):          #build max heap
        Heapify(array, start, n, i)
    for i in range(n - 1, 0, -1):                #move max to the end, shrink heap
        array[start], array[start + i] = array[start + i], array[start]
        Heapify(array, start, i, 0)


#----Shell Sort----
def ShellSort(array, start, end):
    n = end - start + 1
    gap = n // 2
    while gap > 0:
        for i in range(start + gap, end + 1):
            temp = array[i]
            j = i
            while j - gap >= start and array[j - gap] > temp:
                array[j] = array[j - gap]
                j -= gap
            array[j] = temp
        gap //= 2