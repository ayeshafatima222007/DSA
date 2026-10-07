#---Pronlem 1---
def SearchA(Arr,x):
    result =[]
    for i in range(len(Arr)):
        if Arr[i] == x:
            result.append(i)
    return result


#---Pronlem 2---
def SearchB(Arr,x):
    result = []
    for i in range(len(Arr)):
        if Arr[i] == x:
            result.append(i)
        elif Arr[i] < x:
            continue
        elif Arr[i] > x:
            break
    return result


#---Pronlem 3---
def Minimum(Arr,starting,ending):
    minIndex = starting
    for i in range(starting+1,ending+1):
        if Arr[i] < Arr [minIndex]:
            minIndex = i
    return minIndex


#---Pronlem 4---
def Sort4(Arr):
    n=len(Arr)
    for i in range(n-1):
        mini = i
        for j in range(i+1,n):
            if Arr[j] < Arr[mini]:
                mini = j
                Arr[i],Arr[mini] = Arr[mini],Arr[i]


#---Pronlem 5---
def StringReverse(str,starting,ending):
    s=str[starting:ending+1]
    return s[::-1]


#---Pronlem 6---
def SumIterative(x):
    total=0
    while x>0 :
        lastDigit = x % 10
        total+=lastDigit
        x = x // 10
    return total

def SumRecursive(x):
    if x==0:
        return 0
    else:
        lastDigit = x % 10
    return lastDigit + SumRecursive(x // 10)


#---Pronlem 7---
def RowWiseSum(Mat):
    result =[]
    for row in Mat:
        result.append(sum(row))
    return result

def ColumnWiseSum(Mat):
    result = []
    for j in range(len(Mat[0])):
        total = 0
        for i in range(len(Mat)):
            total += Mat[i][j]
        result.append(total)
    return result


#---Pronlem 8---
def SortedMerge(arr1, arr2):
    result = []
    i = j = 0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1
    result.extend(arr1[i:])
    result.extend(arr2[j:])
    return result


#---Pronlem 9---
def PalindromRecursive(s):
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return PalindromRecursive(s[1:-1])


#---Pronlem 10---
def Sort10(arr):
    arr.sort()                                # built-in ascending sort
    neg = [x for x in arr if x < 0]
    pos = [x for x in arr if x >= 0]
    result = []
    for i in range(max(len(neg), len(pos))):
        if i < len(neg): result.append(neg[i])
        if i < len(pos): result.append(pos[i])
    return result