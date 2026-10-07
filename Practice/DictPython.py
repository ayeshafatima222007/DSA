#Creating a dictionary
info = {'name':'Karan', 'age':19, 'eligible':True}
print(info)
print(info['name'])
print(info.get('name'))

# print(info['name2'])   #shows error
print(info.get('name2'))   #shows null

print("------CRUD Operations------")
print("--Create--")
student = {
    "name": "Ali",
    "age": 21,
    "department": "CS"
}

print(student)

#accessing specific value
print("\n--Read--")
print(f"The accessed name from dictionary is {student["name"]}")
print(student.values())

#Adding a new item to dictionary
print("\n--Adding new item--")
student["city"] = "Lahore"
print(f"The new inserted value in dictionary is {student}")

#updating student in dictionary
print("\n--Update--")
student["age"] = 22
print(f"The age is updated {student}")

"""
#deleting student in dictionary
print("\n--Delete--")
del student["age"]
print(student)
"""

#loop through dictionary
student = {
    "name": "Ali",
    "age": 21,
    "city": "Lahore"
}
print("\n--Looping in dictionary(printing key only)--")
for key in student:
    print(key)

print("\n--Looping in dictionary(printing key and values)--")
for key, value in student.items():
    print(key, ":", value)

print("\n--Dictionary Methods--")
print(f"Key dictionary method used-Returns all the keys: {student.keys()}")

print(f"Value dictionary method used-Returns all the values: {student.values()}")

print(f"Items dictionary method used-Returns all key-value pairs as tuples: {student.items()}")

print(f"Get dictionary method used-Returns the value of the specified key: {student.get("name")}")

print(f"Pop dictionary method used-Removes the specified key-value pair and returns its value.: {student.pop("age")}")
print(student)
#pop() also returns the removed value
#--removed = student.pop("age")
#--print(removed)
print(student)


#copying the student dictionary to new one
student2 = student.copy()
print(f"student dictionary is copied to student2{student2}")

print(f"student dictionary is sorted alphabetically {sorted(student)}")

print("--Comparison in dictionaries")
print(f"Student 1: {student}")
print(f"Student 2: {student2}")
# Compare values
print("Are both dictionaries equal?", student == student2)