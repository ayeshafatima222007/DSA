given_file = open (file = 'test.txt', mode = 'r') 
lines = given_file. read () 
 
numbers = [] 
arr = lines.split() 
for s in arr: 
    num = int(s) 
    numbers.append(num) 
 
print(numbers) 