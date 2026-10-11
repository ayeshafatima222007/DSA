#---Counting Sort---

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


arr = [-5, -10, 0, -3, 8, 5,  -1, 10] 
print(f"Input: {arr}")
print(f"Output: {counting_sort(arr)}\n")    

#---Radix Sort---
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


arr = [110, 45, 65, 50, 90, 602, 24, 2, 66]
print(f"Input: {arr}")
print(f"Output: {radix_sort(arr)}\n")   


#---Bucket Sort---
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


arr = [0.897, 0.565, 0.656, 0.1234, 0.665, 0.3434]
print(f"Input: {arr}")
print(fr"Output: {bucket_sort(arr)}") 