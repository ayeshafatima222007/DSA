SIZE = 10
EMPTY = -1
DELETED = -2
table = [EMPTY] * SIZE


def hash_function(key):
    return key % SIZE


def insert_key(key):
    for i in range(SIZE):
        index = (hash_function(key) + i * i) % SIZE
        if table[index] == EMPTY or table[index] == DELETED:
            table[index] = key
            return True
    return False


def search_key(key):
    for i in range(SIZE):
        index = (hash_function(key) + i * i) % SIZE
        if table[index] == EMPTY:
            return -1
        if table[index] == key:
            return index
        # other key or DELETED: keep probing
    return -1


def delete_key(key):
    index = search_key(key)
    if index == -1:
        return False
    table[index] = DELETED
    return True


def display():
    for i in range(SIZE):
        if table[i] == EMPTY:
            value = "-"
        elif table[i] == DELETED:
            value = "X"
        else:
            value = table[i]
        print(f"{i}: {value}")


def show_visited(hash_index, size):
    visited = [(hash_index + i * i) % size for i in range(size)]
    print(f"Table Size: {size}, Hash Index: {hash_index}")
    print("Probe Sequence:", visited)
    print("Visited Indexes:", sorted(set(visited)))
    print("Never Visited Indexes:", [x for x in range(size) if x not in visited])


# ---------- Ex 1: verify dry run ----------
print("=== Ex 1: Insert 12, 22, 32, 42 ===")
for key in [12, 22, 32, 42]:
    insert_key(key)
display()
print("Search 32:", search_key(32))
print("Delete 22:", delete_key(22))
print("Search 32 after deletion:", search_key(32))
display()

# ---------- Ex 2: visited indexes (size 10, H(K) = 0) ----------
print("\n=== Ex 2: H(K) = 0, size 10 ===")
show_visited(0, 10)

# ---------- Ex 3: insert fails although table is not full ----------
print("\n=== Ex 3: size 10 ===")
table = [EMPTY] * SIZE
for index, key in [(0, 10), (1, 11), (4, 14), (5, 15), (6, 16), (9, 19)]:
    table[index] = key
display()
print("Insert 20 (H=0):", insert_key(20), "-> fails, 4 slots still empty")

# ---------- Ex 4: prime size 11 ----------
print("\n=== Ex 4: size 11 ===")
show_visited(0, 11)

SIZE = 11
table = [EMPTY] * SIZE
for index, key in [(0, 11), (1, 12), (3, 14), (4, 15), (5, 16), (9, 20)]:
    table[index] = key
display()
print("Insert 22 (H=0):", insert_key(22), "-> still fails, 5 slots empty")