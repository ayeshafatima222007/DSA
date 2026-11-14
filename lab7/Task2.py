class ChainHash:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash_fn(self, k):
        return k % self.size

    def insert(self, k):
        # Ex 4: reject duplicates
        if self.search(k):
            print(f"{k} already exists, not inserted")
            return False
        self.table[self.hash_fn(k)].append(k)
        return True

    def search(self, k):
        return k in self.table[self.hash_fn(k)]

    def remove(self, k):
        chain = self.table[self.hash_fn(k)]
        if k in chain:
            chain.remove(k)
            print(f"{k} deleted")
        else:
            print(f"{k} not found")

    def display(self):
        for i, chain in enumerate(self.table):
            items = "".join(f"{x} -> " for x in chain)
            print(f"{i}: {items}None")

    def total_keys(self):
        return sum(len(chain) for chain in self.table)

    # Ex 2: print length of every chain
    def print_chain_lengths(self):
        for i, chain in enumerate(self.table):
            print(f"Chain {i}: length {len(chain)}")

    # Ex 3: longest chain length
    def longest_chain(self):
        return max(len(chain) for chain in self.table)


# ---------- Reference demo (table size 10) ----------
demo = ChainHash(10)
for k in [15, 25, 35, 12, 22, 7]:
    demo.insert(k)
demo.display()
print("Search 25:", demo.search(25))
demo.remove(25)
demo.display()

# ---------- Ex 2 and 3: 20 keys in a table of size 7 ----------
h = ChainHash(7)
keys20 = [15, 22, 29, 36, 8, 13, 41, 50, 63, 70,
          77, 84, 91, 98, 5, 19, 26, 33, 47, 54]
for k in keys20:
    h.insert(k)

print("\nTable after 20 keys:")
h.display()
print("\nLength of every chain:")
h.print_chain_lengths()
print("Longest chain length:", h.longest_chain())
# Ideal length = 20/7 ~ 3. A much longer chain means the hash function
# spreads keys unevenly, so search degrades from O(1) toward O(n).

# ---------- Ex 4: duplicate test ----------
h.insert(15)   # prints "15 already exists, not inserted"

# ---------- Ex 1: Menu ----------
while True:
    print("\n--- Menu For Hash Table ---")
    print("1) Insert")
    print("2) Search")
    print("3) Delete")
    print("4) Display")
    print("5) Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        h.insert(int(input("Enter key to insert: ")))
    elif choice == "2":
        k = int(input("Enter key to search: "))
        print(k, "Found" if h.search(k) else "Not found")
    elif choice == "3":
        h.remove(int(input("Enter key to delete: ")))
    elif choice == "4":
        h.display()
    elif choice == "5":
        print("Exiting...")
        break
    else:
        print("Invalid choice")