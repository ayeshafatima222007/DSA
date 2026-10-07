"""print("Hello World")
print(3*"My name is Ayesha\n")

print("UET Lahore")
print('UET Lahore')
print("UET Lahore",end="-")
print("Computer Engineering Dept")
print("UET Lahore","Computer Engineering Dept")
print("UET Lahore","Computer Engineering Dept",sep="--")

"""

print("Hello\nworld")
print("First\tSecond\tThird")
print("This is a backslash: \\")
print("She said, \"Hello!\"")
print('He\'s happy')

"""
#starting learning variables
#----------int---------
a=200
print("a")

#----------float---------
b=3.141
print(b)

#----------double---------
pi = 3.14159265358979
print(pi)

#----------string---------
d="Dollar"
print(d)

#----------char---------
char='B'
print(char)

#---------Redeclaring the variable---------
print("----Part 1----")
a="Dollar"
print(a)
a=200
print(a)
print("Both prints\n")

print("----Part 2----")
a="Dollar"
a=200
print(a)
print("Later one prints\n")

print("----Part 3----")
a=200
a="Dollar"
print(a)
print("Later one prints")

#Concatenating string variables
#--------Method 1------------
a='Ayesha'
b='Fatima'
fullname1=a+" "+b
fullname2=a+" ",b
print(a+b)
print(a+" ",b)
print(a+" "+b)
print(fullname1)
print(fullname2)

#Concatenating int variables
c=20
print(c+20)  #if we want to write number with string we have to treat that number also as a string    print(a+str(c))

#-----------Method 2----------
a="Ayesha"
a+=" Fatima"   #or a+ = " Fatima" for spacing
print(a)

#-------Method 3-using join-use for string------------
words = ["I", "love", "Python"]
sentence = " ".join(words)
print(sentence)
"""
#-------Method 4-recommended--------
name = "Ayesha"
age = 20
print(f"My name is {name} and I am {age} years old.")