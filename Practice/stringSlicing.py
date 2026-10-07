#to find the length of string
name="Ayesha"
print(len(name))

fruit="apple"
len1=len(fruit)
print(f"Apple is a {len1} character")

#string slicing
print(len1)
print(fruit[0:3])  #gives first 3 character of string
print(fruit[:3])   #has same meaning as in line 11 as python automatically detect a 0 before :
print(fruit[2:4])  #gives character from 2 to 4 index
print(fruit[2:])   #start from 2 and end at last char
print(fruit[:])    #start from 0 end at last

#--------negative slicing--------
print(fruit[0:-3]) #as len of fruit is 5,so 5-3=2 so it is same as print(fruit[0:2])
print(fruit[0:len(fruit)-3])   #same meaning as above line
print(fruit[:len(fruit)-3])   #same meaning as above line
print(fruit[0:2])  #check of above line

print(fruit[-1:len(fruit)-3])   #5-1=4 : 5-3=2  so it will give empty string
print(fruit[-3:len(fruit)-1])   #5-3=2 : 5-1=4

