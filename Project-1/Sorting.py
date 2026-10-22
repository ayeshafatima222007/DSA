import time         #RunSort=time.perf_counter()
import random       #in quick sort for selecting random pivot
import math         #math.isfinite(f)


class Stats:     #this class use to show comparisons and swaps
    __slots__ = ("cmp", "swp")    #only these 2 attributes in this obj

    def __init__(self):     #constructor-initializing the value of comparison and swaps
        self.cmp = 0
        self.swp = 0


class Rev:                #used for descending in multi-level sort)
    __slots__ = ("v",)     #only one attribute in this obj,","tells its single item tuple

    def __init__(self, v):     #constructor=saves the value of v
        self.v = v

    def __eq__(self, o):       #a==b
        return self.v == o.v      
    
    def __lt__(self, o):       #a<b
        return self.v > o.v
    
    def __le__(self, o):       #a<=b
        return self.v >= o.v
    
    def __gt__(self, o):      #a>b
        return self.v < o.v
    
    def __ge__(self, o):      #a>=b
        return self.v <= o.v

 
# a is a list of (key, row) pairs, sorted in place by key.
def InsertionRange(a, start, end, s):      #s is stats obj
    for i in range(start + 1, end + 1):
        item = a[i]     #key,rows to be sorted be stored in item
        key = item[0]
        j = i - 1
        while j >= start:     #move backward
            s.cmp += 1      #one cmp done so count +1
            if a[j][0] > key:       #prev element key > item key
                a[j + 1] = a[j]
                s.swp += 1
                j -= 1
            else:
                break
        a[j + 1] = item


def Merge(a, start, mid, end, s):
    left = a[start:mid + 1]
    right = a[mid + 1:end + 1]
    i = j = 0
    k = start
    while i < len(left) and j < len(right):
        s.cmp += 1
        if left[i][0] <= right[j][0]:          # <= keeps equal keys in order (stable)
            a[k] = left[i];
            i += 1
        else:
            a[k] = right[j];
            j += 1
        k += 1
        s.swp += 1

    while i < len(left):
        a[k] = left[i]; 
        i += 1; 
        k += 1;
        s.swp += 1

    while j < len(right):
        a[k] = right[j];
        j += 1;
        k += 1; 
        s.swp += 1


def MergeSort(a, start, end, s):
    if start < end:
        mid = (start + end) // 2
        MergeSort(a, start, mid, s)
        MergeSort(a, mid + 1, end, s)
        Merge(a, start, mid, end, s)


def HybridMergeSort(a, start, end, s, threshold=16):
    if end - start + 1 <= threshold:
        InsertionRange(a, start, end, s)
    else:
        mid = (start + end) // 2
        HybridMergeSort(a, start, mid, s, threshold)
        HybridMergeSort(a, mid + 1, end, s, threshold)
        Merge(a, start, mid, end, s)


def BubbleSort(a, start, end, s):
    for i in range(start, end):
        for j in range(start, end - i):
            s.cmp += 1
            if a[j][0] > a[j + 1][0]:     #if key of j>key of j+1
                a[j], a[j + 1] = a[j + 1], a[j]
                s.swp += 1


def SelectionSort(a, start, end, s):
    for i in range(start, end):
        mini = i
        for j in range(i + 1, end + 1):
            s.cmp += 1
            if a[j][0] < a[mini][0]:
                mini = j
        if mini != i:
            a[i], a[mini] = a[mini], a[i]
            s.swp += 1


def QuickSort(a, low, high, s):
    while low < high:
        r = random.randint(low, high)
        if r != low:
            a[low], a[r] = a[r], a[low]
            s.swp += 1
        pivot = a[low][0]
        lt, gt, i = low, high, low + 1
        while i <= gt:
            c = a[i][0]
            s.cmp += 1
            if c < pivot:
                a[lt], a[i] = a[i], a[lt]
                lt += 1; i += 1; s.swp += 1
            else:
                s.cmp += 1
                if c > pivot:
                    a[i], a[gt] = a[gt], a[i]
                    gt -= 1; s.swp += 1
                else:
                    i += 1
        if lt - low < high - gt:
            QuickSort(a, low, lt - 1, s)
            low = gt + 1
        else:
            QuickSort(a, gt + 1, high, s)
            high = lt - 1


def SiftDown(a, start, size, i, s):        #i=node which goes down 
    while True:
        largest = i
        left = 2 * i + 1
        right = left + 1

        if left < size:
            s.cmp += 1
            if a[start + left][0] > a[start + largest][0]:
                largest = left

        if right < size:
            
            s.cmp += 1
            if a[start + right][0] > a[start + largest][0]:
                largest = right

        if largest == i:
            return
        a[start + i], a[start + largest] = a[start + largest], a[start + i]
        s.swp += 1
        i = largest


def HeapSort(a, start, end, s):
    n = end - start + 1

    for i in range(n // 2 - 1, -1, -1):
        SiftDown(a, start, n, i, s)

    for i in range(n - 1, 0, -1):
        a[start], a[start + i] = a[start + i], a[start]
        s.swp += 1
        SiftDown(a, start, i, 0, s)


def ShellSort(a, start, end, s):
    gap = (end - start + 1) // 2     #st start gap is half of len of part
    while gap > 0:

        for i in range(start + gap, end + 1):
            temp = a[i]     #store key,row in temp
            j = i           #j is its present place

            while j - gap >= start:
                s.cmp += 1

                if a[j - gap][0] > temp[0]:
                    a[j] = a[j - gap]
                    s.swp += 1
                    j -= gap
                else:
                    break
            a[j] = temp
        gap //= 2

def CountingSort(a, s):
    keys = [x[0] for x in a]
    mini, maxi = min(keys), max(keys)
    k = maxi - mini

    if k > 5_000_000:
        raise ValueError("Value range too large for Counting Sort on this column")
    count = [0] * (k + 1)   #makes a list where at each index its 0

    for key in keys:       #use to find freqquency of number
        count[key - mini] += 1

    for i in range(1, k + 1):        #use to find no.of counts on the index
        count[i] += count[i - 1]

    out = [None] * len(a)

    for i in range(len(a) - 1, -1, -1):        #loop in reverse
        j = keys[i] - mini
        count[j] -= 1
        out[count[j]] = a[i]
    a[:] = out


def RadixSort(a, s):
    mini = min(x[0] for x in a)
    work = [(x[0] - mini, x) for x in a]            # making no. non neg
    biggest = max(w[0] for w in work)
    exp = 1      #defines integer place

    while biggest // exp > 0:
        count = [0] * 10

        for w in work:     #makes current digit (15 // 1) % 10 = 5
            count[(w[0] // exp) % 10] += 1

        for i in range(1, 10):     #cumulative count
            count[i] += count[i - 1]

        out = [None] * len(work)

        for i in range(len(work) - 1, -1, -1):
            d = (work[i][0] // exp) % 10
            count[d] -= 1     #gives correct position of that digit
            out[count[d]] = work[i]

        work = out
        exp *= 10
    a[:] = [w[1] for w in work]

def BucketSort(a, s):
    n = len(a)
    mn = min(x[0] for x in a)
    span = max(x[0] for x in a) - mn
    buckets = [[] for _ in range(n)]
    for item in a:
        idx = 0 if span == 0 else min(int((item[0] - mn) / span * n), n - 1)
        buckets[idx].append(item)
    for b in buckets:
        InsertionRange(b, 0, len(b) - 1, s)
    a[:] = [x for b in buckets for x in b]


def RangeAlgo(fn):           #making same parameters for all algorithms,(a,s)
    return lambda a, s: fn(a, 0, len(a) - 1, s)

#dict of all algorithms
Algorithms = {
    "Insertion Sort":    {"fn": RangeAlgo(InsertionRange),     "complexity": "O(n^2)",                    "stable": True,  "kind": "compare"},
    "Merge Sort":        {"fn": RangeAlgo(MergeSort),          "complexity": "O(n log n)",                "stable": True,  "kind": "compare"},
    "Hybrid Merge Sort": {"fn": RangeAlgo(HybridMergeSort),   "complexity": "O(n log n)",                "stable": True,  "kind": "compare"},
    "Bubble Sort":       {"fn": RangeAlgo(BubbleSort),         "complexity": "O(n^2)",                    "stable": True,  "kind": "compare"},
    "Selection Sort":    {"fn": RangeAlgo(SelectionSort),      "complexity": "O(n^2)",                    "stable": False, "kind": "compare"},
    "Quick Sort":        {"fn": RangeAlgo(QuickSort),          "complexity": "O(n log n) avg, O(n^2) worst", "stable": False, "kind": "compare"},
    "Heap Sort":         {"fn": RangeAlgo(HeapSort),           "complexity": "O(n log n)",                "stable": False, "kind": "compare"},
    "Shell Sort":        {"fn": RangeAlgo(ShellSort),          "complexity": "O(n^2) worst",              "stable": False, "kind": "compare"},
    "Counting Sort":     {"fn": CountingSort,                    "complexity": "O(n + k)",                  "stable": True,  "kind": "int"},
    "Radix Sort":        {"fn": RadixSort,                       "complexity": "O(d(n + b))",               "stable": True,  "kind": "int"},
    "Bucket Sort":       {"fn": BucketSort,                      "complexity": "O(n + k) avg, O(n^2) worst", "stable": True,  "kind": "number"},
}
AlgoNames = list(Algorithms)


# Column handling (CSV values are strings)
def ColumnKind(rows, idx):      #check columns=int,float or text(empty cells are ignored)
    kind, seen = "int", False
    for r in rows:
        v = str(r[idx]).strip()
        if v == "":
            continue
        try:
            f = float(v)
        except ValueError:
            return "text"
        if not math.isfinite(f):
            return "text"
        seen = True
        if f != int(f):
            kind = "float"
    return kind if seen else "text"


def MakeKeys(rows, idx, kind):   #make keys from columns
    if kind == "text":
        return [str(r[idx]).lower() for r in rows]     #make text into lowercase
    conv = int if kind == "int" else float       #check for numbers
    vals = [None if str(r[idx]).strip() == "" else conv(float(r[idx])) for r in rows]
    low = min(v for v in vals if v is not None) - 1     # empty cells sort first
    return [low if v is None else v for v in vals]


def IsApplicable(algo, kind):     #check if the algorithm runs on the respective column
    need = Algorithms[algo]["kind"]
    return need == "compare" or (need == "number" and kind in ("int", "float")) \
        or (need == "int" and kind == "int")


def ApplicableAlgorithms(rows, idx):     #check what algorithm are suitable for this column
    kind = ColumnKind(rows, idx)
    return [n for n in AlgoNames if IsApplicable(n, kind)]

 
# Public API-main function sort calls it
def RunSort(rows, columns, algo):
     
    info = Algorithms[algo]
    note = ""
    n = len(rows)

    if len(columns) == 1:
        idx, desc = columns[0]
        kind = ColumnKind(rows, idx)
        if not IsApplicable(algo, kind):
            raise ValueError(f"{algo} cannot sort this column ({kind}); it needs "
                             f"{'whole numbers' if info['kind'] == 'int' else 'numbers'}")
        keys = MakeKeys(rows, idx, kind)

    else:
        # Multi-level: one pass with a composite key; needs a stable comparison sort.
        if info["kind"] != "compare" or not info["stable"]:
            note = f"{algo} is not suitable for multi-level sort; used Merge Sort instead"
            algo = "Merge Sort"
            info = Algorithms[algo]
        per_col = []

        for idx, desc in columns:
            k = MakeKeys(rows, idx, ColumnKind(rows, idx))
            per_col.append([Rev(x) for x in k] if desc else k)
        keys = list(zip(*per_col))

    items = list(zip(keys, rows))
    s = Stats()
    t0 = time.perf_counter()
    if n > 1:
        info["fn"](items, s)    #runs algo here
    ms = (time.perf_counter() - t0) * 1000

    out = [it[1] for it in items]
    if len(columns) == 1 and columns[0][1]:
        out.reverse()
    return {"rows": out, "time_ms": ms, "comparisons": s.cmp, "swaps": s.swp,
            "algo": algo, "complexity": info["complexity"], "stable": info["stable"],
            "n": n, "note": note}


def Benchmark(rows, idx, limit=3000):
    sample = rows if limit is None else rows[:limit]
    kind = ColumnKind(sample, idx)
    results = []
    for name in AlgoNames:
        info = Algorithms[name]
        if not IsApplicable(name, kind):
            results.append({"algo": name, "complexity": info["complexity"], "stable": info["stable"],
                            "n": len(sample), "time_ms": None, "comparisons": None, "swaps": None,
                            "note": "Not applicable to this column"})
            continue
        r = RunSort(sample, [(idx, False)], name)
        del r["rows"]
        results.append(r)
    return results