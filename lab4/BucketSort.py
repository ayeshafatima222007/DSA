
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