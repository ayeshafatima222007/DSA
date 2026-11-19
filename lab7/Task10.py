EMPTY = -1
DELETED = -2
SIZE = 11


def name_sum(name):
    total = 0
    for ch in name:
        total += ord(ch)
    return total


class Phonebook:
    def __init__(self, technique):
        self.technique = technique          # 1 = chaining, 2 = linear, 3 = double
        self.collisions = 0
        if technique == 1:
            self.table = [[] for _ in range(SIZE)]
        else:
            self.table = [EMPTY] * SIZE

    def probe_index(self, name, i):
        total = name_sum(name)
        if self.technique == 2:
            return (total % SIZE + i) % SIZE
        step = 8 - (total % 8)
        return (total % SIZE + i * step) % SIZE

    def search(self, name):
        if self.technique == 1:
            for n, phone in self.table[name_sum(name) % SIZE]:
                if n == name:
                    return phone
            return None
        for i in range(SIZE):
            idx = self.probe_index(name, i)
            slot = self.table[idx]
            if slot == EMPTY:
                return None
            if slot != DELETED and slot[0] == name:
                return slot[1]
        return None

    def add(self, name, phone):
        if self.search(name) is not None:
            print(f"Contact '{name}' already exists. Not added.")
            return
        if self.technique == 1:
            chain = self.table[name_sum(name) % SIZE]
            if len(chain) > 0:
                self.collisions += 1
            chain.append((name, phone))
            print(f"Added {name}.")
            return
        for i in range(SIZE):
            idx = self.probe_index(name, i)
            slot = self.table[idx]
            if slot == EMPTY or slot == DELETED:
                self.table[idx] = (name, phone)
                print(f"Added {name} at index {idx}.")
                return
            if i == 0:
                self.collisions += 1
        print(f"Table is full. Cannot add '{name}'.")

    def delete(self, name):
        if self.technique == 1:
            chain = self.table[name_sum(name) % SIZE]
            for item in chain:
                if item[0] == name:
                    chain.remove(item)
                    print(f"Deleted {name}.")
                    return
            print(f"'{name}' not found.")
            return
        for i in range(SIZE):
            idx = self.probe_index(name, i)
            slot = self.table[idx]
            if slot == EMPTY:
                break
            if slot != DELETED and slot[0] == name:
                self.table[idx] = DELETED
                print(f"Deleted {name}.")
                return
        print(f"'{name}' not found.")

    def display(self):
        for i in range(SIZE):
            slot = self.table[i]
            if self.technique == 1:
                items = "".join(f"({n}, {p}) -> " for n, p in slot)
                print(f"{i}: {items}None")
            elif slot == EMPTY:
                print(f"{i}: -")
            elif slot == DELETED:
                print(f"{i}: X")
            else:
                print(f"{i}: {slot[0]} - {slot[1]}")


print("Choose collision technique:")
print("1) Chaining  2) Linear Probing  3) Double Hashing")
choice = input("Choice: ")
while choice not in ("1", "2", "3"):
    choice = input("Enter 1, 2 or 3: ")
book = Phonebook(int(choice))

if input("Load the 10 test contacts? (y/n): ").lower() == "y":
    test = ["Ali", "Sara", "Usman", "Ayesha", "Hamza",
            "Fatima", "Bilal", "Zainab", "Hassan", "Maryam"]
    for number, nm in enumerate(test, start=1):
        book.add(nm, f"0300-{number:07d}")

while True:
    print("\n1) Add contact  2) Search contact  3) Delete contact")
    print("4) Display table  5) Show total collisions  6) Exit")
    c = input("Enter choice: ")
    if c == "1":
        nm = input("Name: ")
        ph = input("Phone: ")
        book.add(nm, ph)
    elif c == "2":
        nm = input("Name: ")
        phone = book.search(nm)
        print(f"{nm}: {phone}" if phone is not None else f"{nm}: Not found")
    elif c == "3":
        book.delete(input("Name: "))
    elif c == "4":
        book.display()
    elif c == "5":
        print("Total collisions:", book.collisions)
    elif c == "6":
        print("Exiting...")
        break
    else:
        print("Invalid choice")