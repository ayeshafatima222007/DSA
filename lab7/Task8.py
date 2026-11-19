def is_prime(x):
    if x < 2:
        return False
    i = 2
    while i * i <= x:
        if x % i == 0:
            return False
        i += 1
    return True


def next_prime(x):
    x += 1
    while not is_prime(x):
        x += 1
    return x


class LinearHash:
    def __init__(self, size=7):
        self.size = size
        self.table = [None] * size
        self.count = 0

    def load_factor(self):
        return self.count / self.size

    def _place(self, k):
        # linear probing, no load check
        for i in range(self.size):
            idx = (k % self.size + i) % self.size
            if self.table[idx] is None:
                self.table[idx] = k
                self.count += 1
                return True
        return False

    def insert(self, k):
        if self.load_factor() > 0.7:
            self.rehash()
        return self._place(k)

    def rehash(self):
        old_keys = [k for k in self.table if k is not None]
        old_size = self.size
        self.size = next_prime(2 * old_size)
        self.table = [None] * self.size
        self.count = 0
        for k in old_keys:
            self._place(k)
        print(f"  >> REHASH: old size {old_size} -> new size {self.size}")


# Ex 1 and Ex 2
h = LinearHash(7)
for k in range(10, 101, 10):
    h.insert(k)
    print(f"Insert {k}: table size = {h.size}, load factor = {h.load_factor():.3f}")

print("\nFinal table:")
for i, v in enumerate(h.table):
    print(f"{i}: {v if v is not None else '-'}")