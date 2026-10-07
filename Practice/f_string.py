latter="My name is {} and i live in {}"
name="Ayesha"
country="Pakistan"

print("----Way 1----")
print(latter.format(name,country))
print(latter.format(country,name))
print(latter.format("name","country"))
print(latter.format("",""))

print("----Way 2----")
latter2="My name is {1} and i live in {0}"
print(latter2.format(country,name))

print("----Way 3----")
latter3="My name is {0} and i live in {1}"
print(latter3.format(name,country))

print("--------f string--------")
print(f"My name is {name} and i live in {country}")