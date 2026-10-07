print("--Iterative--")
sum = 0  
for i in range (11): 
    sum += i 
print(sum) 

print("--Recursion--")
def sum(n):
    if n==0:
        return n
    else:
        return n + sum(n-1)
print(sum(10))