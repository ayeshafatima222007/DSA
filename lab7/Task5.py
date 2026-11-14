SIZE = 11
EMPTY = -1
DELETED = -2
table = [EMPTY] * SIZE

def h1(k):
    return k % 11

def h2(k):
    return 8 - (k % 8)

def insert_key(k):
    """Returns (success, list of indexes probed)."""
    probes = []
    for i in range(SIZE):
        idx = (h1(k) + i * h2(k)) % SIZE
        probes.append(idx)
        if table[idx] == EMPTY or table[idx] == DELETED:
            table[idx] = k
            return True, probes
    return False, probes

def search_key(k):
    for i in range(SIZE):
        idx = (h1(k) + i * h2(k)) % SIZE
        if table[idx] == k:
            return idx
        if table[idx] == EMPTY:
            return -1
        # DELETED or other key: keep probing
    return -1

def delete_key(k):
    idx = search_key(k)
    if idx == -1:
        return False
    table[idx] = DELETED
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

def reset():
    global table
    table = [EMPTY] * SIZE

# Linear probing on a separate size-11 table, for Ex 3 comparison
def linear_insert(lt, k):
    probes = []
    for i in range(SIZE):
        idx = (k % 11 + i) % SIZE
        probes.append(idx)
        if lt[idx] == EMPTY:
            lt[idx] = k
            return probes
    return probes

# ---------- Ex 1: verify dry run (10, 21, 32, 43) + search/delete ----------
print("=== Ex 1: Insert 10, 21, 32, 43 ===")
for k in [10, 21, 32, 43]:
    ok, p = insert_key(k)
    print(f"Key {k}: H1={h1(k)}, H2={h2(k)}, probes={p}, final index={p[-1]}")
display()
print("Search 32:", search_key(32))
print("Delete 21:", delete_key(21))
print("Search 21 after delete:", search_key(21))
print("Search 43 after delete:", search_key(43))
display()

# ---------- Ex 2: insert 10, 21, 32, 43, 54, 65, 76 ----------
print("\n=== Ex 2: Insert 10, 21, 32, 43, 54, 65, 76 ===")
reset()
keys = [10, 21, 32, 43, 54, 65, 76]
double_probes = {}
for k in keys:
    ok, p = insert_key(k)
    double_probes[k] = p
display()

# ---------- Ex 3: probe sequences, double vs linear ----------
print("\n=== Ex 3: Probe sequences ===")
lt = [EMPTY] * SIZE
total_d = total_l = 0
print(f"{'Key':<5}{'Double Hashing':<20}{'Linear Probing'}")
for k in keys:
    lp = linear_insert(lt, k)
    dp = double_probes[k]
    total_d += len(dp)
    total_l += len(lp)
    print(f"{k:<5}{str(dp):<20}{lp}")
print(f"Total probes -> Double: {total_d}, Linear: {total_l}")