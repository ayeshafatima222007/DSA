
#------ Basic idea of local and global variable
x=4
y=5
print(x)
print(y)

def variables():
    x=10
    y=20
    print(x)
    print(y)
    print(f"Local variables are {x} and {y} and their sum is {x+y}")

variables()
print(f"Global variables are {x} and {y} and their sum is {x+y}")


a=3
b=5
print(f"First declared variable are {a} and {b}")
def changeVariable():
    global a
    a = 30  #I can also change global variable if it is int to string here or any datatype
    b=12
    print(f"Local Variable b is {b}")

changeVariable()
print(f"Changed a varaible in functionn{a}")

"""
#--------Deleting a variable------
g=10
print(g)
del g
print(g)
"""