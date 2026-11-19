import random

SIZE = 101
EMPTY = -1

def h1(k):
    return k % SIZE

def h2(k):
    return 8 - (k % 8)

def insert_linear(table, k):
    probes = 0
    for i in range(SIZE):
        idx = (h1(k) + i) % SIZE
        probes += 1
        if table[idx] == EMPTY:
            table[idx] = k
            return probes
    return probes

def insert_quadratic(table, k):
    probes = 0
    for i in range(SIZE):
        idx = (h1(k) + i * i) % SIZE
        probes += 1
        if table[idx] == EMPTY:
            table[idx] = k
            return probes
    return probes

def insert_double(table, k):
    probes = 0
    for i in range(SIZE):
        idx = (h1(k) + i * h2(k)) % SIZE
        probes += 1
        if table[idx] == EMPTY:
            table[idx] = k
            return probes
    return probes

def average_probes(insert_func, n):
    table = [EMPTY] * SIZE
    keys = random.sample(range(1, 1000), n)
    total = 0
    for k in keys:
        total += insert_func(table, k)
    return total / n

RUNS = 5

print(f"{'N':<6}{'Load':<8}{'Linear':<10}{'Quadratic':<12}{'Double':<10}")
for n in [20, 40, 60, 80]:
    lin = 0
    quad = 0
    dbl = 0
    for _ in range(RUNS):
        lin += average_probes(insert_linear, n)
        quad += average_probes(insert_quadratic, n)
        dbl += average_probes(insert_double, n)
    print(f"{n:<6}{n / SIZE:<8.2f}{lin / RUNS:<10.2f}{quad / RUNS:<12.2f}{dbl / RUNS:<10.2f}")