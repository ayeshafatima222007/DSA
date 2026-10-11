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

print(f"Output: {counting_sort(arr)}")    