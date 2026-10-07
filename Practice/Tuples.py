"""
#printing full tuple
tup1 = (1,2,3,4,5,6,7,8)
print(tup1)
tup2 = ("Ayesha","Abdullah","Huzaifa","Hamza")
print(tup2)

#printing thing from tuple at specific location
print(tup1[2:6])
print(f"My brothers are {tup2[1:4]}")


#-------Packing and unpacking a tuple--------
x = ("Moosa","Haroon","Fatima")  #packing
(Eldest,Middle,Youngest)=x     #unpacking
print(x)
print(Eldest)
print(Middle)
print(Youngest)


#------Comparison in tuples-------
print("--Question 1--")
a = (5, 6)
b = (1, 4)
print(a > b)

print("--Question 2--")
a = (2, 100)
b = (5, 1)
print(a > b)

print("--Question 3--")
a = (5, 2)
b = (5, 7)
print(a < b)

print("--Question 4--")
a = (5, 10)
b = (5, 3)
print(a > b)

print("--Question 5--")
a = (2, 5, 10)
b = (2, 5, 8)
print(a > b)

print("--Question 6--")
a = (4, 8, 9)
b = (4, 8, 15)
print(a < b)

print("--Question 7--")
a = (1, 1000)
b = (2, 1)
print(a < b)

print("--Question 8--")
a = ("apple", "cat")
b = ("banana", "ant")
print(a < b)

print("--Question 9--")
a = ("cat", 5)
b = ("cat", 3)
print(a > b)

print("--Question 10--")
a = (3, 7)
b = (3, 7)
print(a == b)


#------Deleting a tuple------
#we can not delete a single element from tuple,ratrher we can delete a whole tuple,if want change there are 2 ways
student = ("Ayesha", 20, "CS")
print(student)

#del student
#print(student)

#Method 1:Delete the whole tuple and make a new one without adding unwanted element

#Method 2:Convert the tuple into list,then remove from list and then convert it back
numbers = (10, 20, 30, 40)
temp = list(numbers)
temp.remove(20)
numbers = tuple(temp)
print(numbers)


#------Slicing the tuple-----
print("\n--Slicing Question 1--")
numbers = (10, 20, 30, 40, 50, 60)
print(numbers[1:4])

print("\n--Slicing Question 2(slicing from begining)--")
print(numbers[:3])

print("\n--Slicing Question 3(slicing till end)--")
print(numbers[2:])

print("\n--Slicing Question 4(copy entire tuple)--")
print(numbers[:])

print("\n--Slicing Question 5(steping in tuple)--")
print(numbers[::2])    #every 2nd element
print(numbers[::3])    #every 3rd element

print("\n--Slicing Question 6(Reversing the tuple)--")
print(numbers[::-1])

print("\n--Slicing Question 7(Negative indexing)--")
print(numbers[-4:-1])

print("\n--Slicing Question 8(For string elements)--")
names = ("Ali", "Sara", "Ahmed", "Ayesha", "Fatima")
print(names[1:4])
print(names[-3:])

"""
#------Built-in functions in tuple---------
#1.len to count total number of elements in tuple
numbers = (30, 10, 40, 20, 50)
print(f"Total number of elements in numbers tuple {len(numbers)}")

#2.Return the largest element
print(f"Largest element in numbers tuple {max(numbers)}\n")

#2.Return the smallest element
print(f"Smallest element in numbers tuple {min(numbers)}\n")

#3.sum of all elements
print(f"Sum of all the elements in numbers tuple {sum(numbers)}\n")

#4.sort the elements
print(f"Elements sorted in numbers tuple {sorted(numbers)}\n")

#5.any() use for any true value
values = (0, False, 5)
print(f"Return if any one of the value is TRUE in tuple {any(values)}\n")

#6.returns true if all values are true
num = (1, 2, 3)
print(f"Return if any all the valus is TRUE in tuple [num]{any(values)}\n")
print(f"Return if any all the valus is TRUE in tuple [values]{any(values)}\n")

# 7.reversing the tuple
print(f"Reversing the tuple {tuple(reversed(numbers))}")

#---------Count method-built in-------
numbert = (10, 20, 10, 30, 10)
print(f"Counting how many times a number repeat in tuple {numbert.count(10)}")

# 1. Using slicing (Most common)
#t[::-1]

# 2. Using reversed() function
# tuple(reversed(t))

# 3. Convert tuple to list, use reverse(), then convert back to tuple
# temp = list(t)
# temp.reverse()
# t = tuple(temp)

# 4. Using a loop to create a new reversed tuple
# for i in range(len(t)-1, -1, -1):
#     reversed_tuple += (t[i],)
