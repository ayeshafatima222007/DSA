import random

guess_num = int(input("Guess the number: "))

if guess_num.isdigit():
    guess_num = int(guess_num)

    if guess_num <= 0:
        print("Please enter a number greater than 0.")
        quit()
else:
    print("Please enter a number.")
    quit()

random_number=random.randrange(0,guess_num)    #generate random number upto 11
print(random_number)
#r = random.randrange(-1,10)   #generate -1 to 10,but not 10
#print(r)