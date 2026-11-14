EMPTY = -1
KEYS = [23, 43, 13, 27, 33, 53, 63, 14, 24, 34]


def linear(k, i):
    return k % 10 + i


def quadratic(k, i):
    return k % 10 + i * i


def double(k, i):
    return k % 11 + i * (8 - k % 8)


def chaining(keys, size=10):
    table = [[] for _ in range(size)]
    collisions = 0
    steps = 0
    failures = 0
    for k in keys:
        chain = table[k % size]
        if len(chain) > 0:
            collisions += 1
        steps += len(chain)          # nodes walked to reach the end
        chain.append(k)
    return collisions, steps, failures


def open_addr(keys, size, probe):
    table = [EMPTY] * size
    collisions = 0
    steps = 0
    failures = 0
    for k in keys:
        placed = False
        for i in range(size):
            idx = probe(k, i) % size
            steps += 1
            if table[idx] == EMPTY:
                table[idx] = k
                placed = True
                break
            if i == 0:
                collisions += 1      # first slot was occupied
        if not placed:
            failures += 1
    return collisions, steps, failures


def show(name, result, extra):
    print(f"{name:<18}{result[0]:<12}{result[1]:<14}{result[2]:<10}{extra}")


def run_all():
    print(f"{'Technique':<18}{'Collisions':<12}{'Total Probes':<14}{'Failures':<10}Extra Space")
    show("Chaining", chaining(KEYS), "Yes")
    show("Linear Probing", open_addr(KEYS, 10, linear), "No")
    show("Quadratic Probing", open_addr(KEYS, 10, quadratic), "No")
    show("Double Hashing", open_addr(KEYS, 11, double), "No")


while True:
    print("\n1) Chaining  2) Linear  3) Quadratic  4) Double  5) Compare all  6) Exit")
    choice = input("Choice: ")
    if choice == "1":
        print(chaining(KEYS))
    elif choice == "2":
        print(open_addr(KEYS, 10, linear))
    elif choice == "3":
        print(open_addr(KEYS, 10, quadratic))
    elif choice == "4":
        print(open_addr(KEYS, 11, double))
    elif choice == "5":
        run_all()
    elif choice == "6":
        break
    else:
        print("Invalid choice")