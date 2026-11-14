SIZE = 10
EMPTY = -1
DELETED = -2
table = [EMPTY] * SIZE

def reset():
    global table
    table = [EMPTY] * SIZE

def h(k):
    return k % SIZE

def insert_key(k):
    """Returns (success, probes). Probes = number of indexes checked."""
    probes = 0
    for i in range(SIZE):
        idx = (h(k) + i) % SIZE
        probes += 1
        if table[idx] == EMPTY or table[idx] == DELETED:
            table[idx] = k
            return True, probes
    return False, probes          # table is full

def search_key(k):
    for i in range(SIZE):
        idx = (h(k) + i) % SIZE
        if table[idx] == k:
            return idx
        if table[idx] == EMPTY:   # chain ends here
            return -1
        # DELETED: keep probing
    return -1

def delete_key(k, marker=DELETED):
    idx = search_key(k)
    if idx != -1:
        table[idx] = marker
        return True
    return False

def display():
    for i in range(SIZE):
        if table[i] == EMPTY:
            value = "-"
        elif table[i] == DELETED:
            value = "X"
        else:
            value = table[i]
        print(f"{i}: {value}")

# ---------- Ex 1 + Ex 3: insert test keys, count probes ----------
print("=== Ex 1 & 3: Insert 23, 43, 13, 27, 33 ===")
keys = [23, 43, 13, 27, 33]
total_probes = 0
for k in keys:
    ok, p = insert_key(k)
    total_probes += p
    print(f"Insert {k}: probes = {p}")
display()
print(f"Average probes per insert = {total_probes / len(keys):.2f}")
print("Search 13 ->", search_key(13))
print("Search 99 ->", search_key(99))

# ---------- Ex 2: deletion problem ----------
print("\n=== Ex 2a: delete 43 with EMPTY marker, then search 13 ===")
reset()
for k in keys:
    insert_key(k)
delete_key(43, marker=EMPTY)
display()
print("Search 13 ->", search_key(13), "(-1 means NOT FOUND, wrong!)")

print("\n=== Ex 2b: delete 43 with DELETED marker, then search 13 ===")
reset()
for k in keys:
    insert_key(k)
delete_key(43, marker=DELETED)
display()
print("Search 13 ->", search_key(13), "(found at index 5, correct)")

# ---------- Ex 4: fill the table, then insert one more ----------
print("\n=== Ex 4: fill the table, then insert one more ===")
reset()
for k in range(10, 20):           # 10 keys fill all 10 slots
    insert_key(k)
display()
ok, p = insert_key(20)
if not ok:
    print("Insert 20 failed: Table is full")