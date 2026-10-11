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
print(fr"Output: {radix_sort(arr)}")   

 