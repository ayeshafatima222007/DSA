l=[ 2  , 3 ,  4 , 5 ]
#  [0]  [1]  [2]  [3]      positive indexing
#  [-4] [-3] [-2] [1]      positive indexing
print(l)
print(type(l))
print(sum(l))

#-----list indexing-----
print(l[0])
print(l[1])
print(l[2])
print(l[3])
#print(l[4])   gives error

list2=[1,2,"Ayesha",True] #we can add anything means of any datatype in list
print(list2)

#------------List functions----------
print("--Printing List--")
f1=[10,9,3,8,5]
print(f1)

print("--List Indexing--")
f1.index(5)
print(f1)

print("--Append in List--")
f1.append(6)   #append function add new member at the end of list
print(f1)

print("--Insert in List--")
f1.insert(1,7)
print(f1)

print("--Count in List--")
print(f1.count(5))

print("--Reverse in List--")
f1.reverse()   #reverse the array
print(f1)

print("--Sort in List--")
f1.sort()    #sort list in assending order
print(f1)

print("--Sorted and reversed in List--")
f1.sort(reverse=True) #sort and then reverse the list makes it in descending order
print(f1)

print("--Copy Function in List--")
f2=f1.copy()
f2[0]=3
print(f2)

f3=[100,200,86]
print(f3)
f1.extend(f3)    #open f1 and insert f3 on the end of f1
print(f1)
