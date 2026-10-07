#-------Example 1--------
def greet():
    print("Hello, Welcome to Python!")

greet()

#-------Example 2--------
def greet(name):
    print("Hello", name)

greet("Ayesha")

#-------Example 3--------
def add(a, b):
    print("Sum =", a + b)

add(10, 20)

#-------Example 4--------     Value returning function
def square(num):
    return num * num

result = square(5)
print(result)

#-------Example 5--------     to find the largest number
def largest(a, b):
    if a > b:
        return a
    else:
        return b

print(largest(10, 25))

#-------Example 6-------- i can't make an empty body function so if i want to make funtion but not wanted to make it body yet then i use pass
def calculate_salary():
    pass

print("Salary function will be added later.")

#-----------Way to pass arguments----------
#-------Example 7--------
def average(a=9, b=1):
    print("The average is ", (a+b)/2)

average(4, 6)
average(a=2)
average(b=9)
average()

#-------Example 8--------
def name(fname, mname = "Jhon", lname = "Whatson"):
    print("Hello,", fname, mname, lname)

name("Amy", "Agarwal", "Jain")

#-------Example 9--------
def average(*numbers):         #*number is used if we want to pass no. of arguments like in tuple and we also don't know
    # print(type(numbers))
    sum = 0
    for i in numbers:
        sum = sum + i
    print("Average is: ", sum / len(numbers))
# average(4, 6)
# average(b=9)
average(5, 6, 7, 1)

#-------Example 10--------    use for dictionaries
def name(**name):
    print("Hello,", name["fname"], name["mname"], name["lname"])
name(mname = "Buchanan", lname = "Barnes", fname = "James")