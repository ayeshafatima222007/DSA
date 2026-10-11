import random

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

#Create an array of random size
A = [random.randint(1,100) for _ in range(10)]

print(f"Original Array: {A}")

#Applying quick sort
QuickSort(A,0,len(A)-1)
print(f"Sorted Array: {A}")