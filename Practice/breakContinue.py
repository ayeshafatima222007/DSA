#--------------Break-------------
#-------Example 1--------      Stops the loop immediately
for i in range(1, 11):
    if i == 5:
        break
    print(i)

#-------Example 2--------
students = ["Ali", "Ahmed", "Ayesha", "Fatima"]
for student in students:
    if student == "Ayesha":
        print("Student Found!")
        break

#-------Example 3--------
password = "python123"
while True:
    user = input("Enter password: ")
    if user == password:
        print("Access Granted")
        break
    print("Wrong Password")

#-------Example 4--------
i = 1
while i <= 10:
    if i == 6:
        break
    print(i)
    i += 1

#-----------Continue----------
#-------Example 5--------
for i in range(1, 11):
    if i == 5:
        continue
    print(i)

#-------Example 6--------
fruits = ["Apple", "Banana", "Mango", "Orange"]
for fruit in fruits:
    if fruit == "Mango":
        continue
    print(fruit)

#-------Example 7--------
for i in range(1, 11):
    if i % 2 == 0:
        continue
    print(i)

#-------Example 7--------
i = 0
while i < 5:
    i += 1
    if i == 3:
        continue
    print(i)