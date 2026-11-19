class Node:
    def __init__(self, key):
        self.key = key
        self.next = None


class LinkedChainHash:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size      # each index holds the head Node or None

    def hash_fn(self, k):
        return k % self.size

    def insert(self, k):
        idx = self.hash_fn(k)
        node = Node(k)
        node.next = self.table[idx]     # new node points to the old head
        self.table[idx] = node          # new node becomes the head

    def search(self, k):
        cur = self.table[self.hash_fn(k)]
        while cur is not None:
            if cur.key == k:
                return True
            cur = cur.next
        return False

    def remove(self, k):
        idx = self.hash_fn(k)
        cur = self.table[idx]
        prev = None
        while cur is not None:
            if cur.key == k:
                if prev is None:
                    self.table[idx] = cur.next    # deleting the head
                else:
                    prev.next = cur.next          # skip the deleted node
                return True
            prev = cur
            cur = cur.next
        return False

    def display(self):
        for i in range(self.size):
            line = ""
            cur = self.table[i]
            while cur is not None:
                line += f"{cur.key} -> "
                cur = cur.next
            print(f"{i}: {line}None")


h = LinkedChainHash(10)
for k in [15, 25, 35, 12, 22, 7]:
    h.insert(k)
h.display()
print("Search 25:", h.search(25))
print("Search 99:", h.search(99))
print("Remove 25:", h.remove(25))
print("Remove 35 (head):", h.remove(35))
print("Remove 99:", h.remove(99))
h.display()