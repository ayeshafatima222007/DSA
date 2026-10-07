#Time complexity = O(n)
import sys    
import time 

sys.setrecursionlimit(3000)

def factorial(n): 
    if(n==0): 
        return 1 
    else:  
        return n * factorial(n-1) 
 
startTime = time.time() 
n = 1500 
ans= factorial(n) 
endTime = time.time() 
runtime = endTime - startTime 
print("Runtime of factorial at",n,"is",runtime,"seconds")