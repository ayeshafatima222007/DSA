arr=[1,2,3,4,5,6,7,8,9,10]

print("--Iterative--")

for i in arr:
    print(i)


print("--Recursion--")

def print_array(arr, index):
    if index == len(arr):
        return
    else:
        print(arr[index])
        print_array(arr, index + 1)


print_array(arr, 0)