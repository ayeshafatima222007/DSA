print("--Iterative--")
num = 2 
power = 5 
result = 1 
for i in range(power): 
    result = result * num 
print(result)


print("--Recursion--")
def power (n, k): 
    if k == 1: 
        return n 
    else: 
        return n * power (n, k-1)  
print(power(2,3))