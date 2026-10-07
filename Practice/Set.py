fruits = {"apple", "banana", "mango"}
print(fruits)

print("--Empty set--")
empty = set()
print(type(empty))

numbers = {1, 2, 3, 2, 1, 4, 5}   #remove duplicate valuesa
print(numbers)

colors = {"red", "blue"}   #add an element
colors.add("green")
print(colors)

colors = {"red", "blue"}     #add multiple elements
colors.update(["green", "yellow"])
print(colors)

animals = {"cat", "dog", "lion"}     #remove an element
animals.remove("dog")
print(animals)

animals = {"cat", "dog"}
animals.discard("tiger")   # No error
print(animals)


letters = {"A", "B", "C"}      #remove a random element
removed = letters.pop()
print("Removed:", removed)
print(letters)

print("--Union--")
A = {1, 2, 3}
B = {3, 4, 5}
print(A.union(B))

print("--Intersection--")
print(A.intersection(B))

print("--Difference--")
print(A.difference(B))

print("--Symmetric Difference--")
print(A.symmetric_difference(B))

print("--Check if an element exist in set--")
fruits = {"apple", "banana", "mango"}
if "banana" in fruits:
    print("Found")

print("--Loop through set--")
fruits = {"apple", "banana", "mango"}
for fruit in fruits:
    print(fruit)

print("--Length of set--")
numbers = {10, 20, 30, 40}
print(len(numbers))

print("--Subset--")
A = {1, 2, 3}
B = {1, 2, 3, 4, 5}
print(A.issubset(B))
print(A <= B)

print("--Superset--")
A = {1, 2, 3, 4, 5}
B = {1, 2, 3}
print(A.issuperset(B))
print(A >= B)

print("--Proper set--")
A = {1, 2, 3}
B = {1, 2, 3, 4}
print(A < B)