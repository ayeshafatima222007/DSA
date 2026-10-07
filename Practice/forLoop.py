#-------Example 1---------
name = "Ayesha"
for letter in name:
    print(letter)

#-------Example 2---------
fruits = ["Apple", "Banana", "Mango"]     #loop through list
for fruit in fruits:
    print(fruit)

#-------Example 3---------
colors = ("Red", "Green", "Blue")      #loop through tuple
for color in colors:
    print(color)

#-------Example 4---------
numbers = {10, 20, 30, 40}    #loop through set
for num in numbers:
    print(num)

#-------Example 5---------
students = ["Ali", "Ahmed"]     #nested for loop
subjects = ["Math", "Physics"]

for student in students:
    for subject in subjects:
        print(student, "-", subject)

#-------------------For loop with range----------
#-------Example 6---------
for i in range(1, 6):
    print(i)

#-------Example 7---------
for i in range(5):
    print("Hello")

#-------Example 8---------
for i in range(2, 11, 2):
    print(i)

#-------Example 9---------
name = "Python"
for letter in name:
    print(letter)

#---------Example 10 (Multiplication table)----------
num = 7
for i in range(1, 11):
    print(num, "x", i, "=", num * i)