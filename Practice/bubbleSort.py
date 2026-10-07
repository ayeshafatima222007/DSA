Arr1 = [30,20,10,40,15]

def Bubble(X):
    #n=len(X)
    for i in range(len(X)):       #for i in range(n):       
        
        swapped = False

        for j in range(0,len(X)-i-1):        #for j in range(0,n-i-1):
            if X[j]>X[j+1]:
                X[j],X[j+1]=X[j+1],X[j]
                swapped = True

        if not swapped:
            break

Bubble(Arr1)
print(Arr1)