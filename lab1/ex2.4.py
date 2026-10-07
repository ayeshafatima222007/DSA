def fact(num):
    if num<0:
        return -1
    elif num==0 or num == 1:
        return 1
    else:
        return num *fact(num-1)
    
num = int(input("Enter the number: "))
print(f"The factorial of {num} is {fact(num)}")