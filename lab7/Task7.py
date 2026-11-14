def string_hash(name, n):
    total = 0
    for ch in name:
        total += ord(ch)
    return total % n


def weighted_hash(name, n):
    total = 0
    for ch in name:
        total = total * 31 + ord(ch)
    return total % n


students = [(1, "Ali"), (2, "Sara"), (3, "Usman"), (4, "Ayesha"),(5, "Hamza"), (6, "Fatima"), (7, "Bilal"), (8, "Zainab")]


class StringChainHash:
    def __init__(self, size, hash_func):
        self.size = size
        self.hash_func = hash_func
        self.table = [[] for _ in range(size)]

    def insert(self, roll, name):
        self.table[self.hash_func(name, self.size)].append((roll, name))

    def search(self, name):
        for roll, nm in self.table[self.hash_func(name, self.size)]:
            if nm == name:
                return roll
        return None

    def display(self):
        for i, chain in enumerate(self.table):
            items = "".join(f"({r}, {n}) -> " for r, n in chain)
            print(f"{i}: {items}None")

    def collisions(self):
        # keys that landed in a slot that was already occupied
        return sum(len(c) - 1 for c in self.table if len(c) > 1)

    def show_colliding_names(self):
        for i, chain in enumerate(self.table):
            if len(chain) > 1:
                print(f"Index {i}: {[n for r, n in chain]}")


# Ex 1: store and display
h = StringChainHash(7, string_hash)
for roll, name in students:
    h.insert(roll, name)
print("=== Ex 1: ASCII sum, size 7 ===")
h.display()

# Ex 2: search by name
print("\n=== Ex 2: Search ===")
for name in ["Usman", "Zara"]:
    roll = h.search(name)
    print(f"{name}: roll no {roll}" if roll else f"{name}: Not found")

# Ex 3: colliding names
print("\n=== Ex 3: Colliding names ===")
h.show_colliding_names()

# Ex 4: weighted hash comparison
w = StringChainHash(7, weighted_hash)
for roll, name in students:
    w.insert(roll, name)
print("\n=== Ex 4: Weighted sum (x31), size 7 ===")

w.display()
print("\nCollisions -> ASCII sum:", h.collisions(), "| Weighted:", w.collisions())