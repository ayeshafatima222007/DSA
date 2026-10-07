import random 

arr = []
min=0
max=20
n=5

for i in range (0,n):
    num = random.randint(min,max)
    arr.append(num)

print(arr)

print("--TO Do--")
import numpy as np
arr2=np.random.randint(min,max+1,n)
print(arr2)

#random distinct number
#arr=np.random.choice(np.arange(min,max+1), n, replace=False)
#print(arr)