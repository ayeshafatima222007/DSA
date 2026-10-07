Arr = [10,5,7,12,20]

def Select(Arr):
    n=len(Arr)
    for i in range(n-1):
        mini = i
        for j in range(i+1,n):
            if Arr[j] < Arr[mini]:
                mini = j
                Arr[i],Arr[mini] = Arr[mini],Arr[i]
Select(Arr)
print(Arr)

