import time

from Sorting import RunSort, ColumnKind

TEXT_OPERATORS = ["contains", "starts with", "ends with", "equals"]
NUMBER_OPERATORS = [">", ">=", "<", "<="]
OPERATORS = TEXT_OPERATORS + NUMBER_OPERATORS

SearchAlgorithms = {
    "Linear Search": "O(n)",
    "Binary Search": "O(log n) after sorting",
}

 
def Linear(array, target):
    for i in range(len(array)):
        if array[i] == target:
            return i
    return -1


def Binary(array, target):
    left, right = 0, len(array) - 1
    while left <= right:
        mid = (left + right) // 2
        if array[mid] == target:
            return mid
        elif array[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

 
def FindAllLinear(array, target):
    found = []
    start = 0
    while True:
        i = Linear(array[start:], target)
        if i == -1:
            break
        found.append(start + i)
        start += i + 1
    return found


def FindAllBinary(array, target):
    i = Binary(array, target)
    if i == -1:
        return []
    low = i
    while low > 0 and array[low - 1] == target:
        low -= 1
    high = i
    while high < len(array) - 1 and array[high + 1] == target:
        high += 1
    return list(range(low, high + 1))

 
def ToNumber(value):
    try:
        return float(str(value).strip())
    except ValueError:
        return None


def KeyOf(row, field, kind):
    if kind == "text":
        return str(row.get(field, "")).lower()
    return ToNumber(row.get(field, ""))


def MatchOne(row, field, op, value):
    cell = row.get(field, "")
    if op in TEXT_OPERATORS:
        c = str(cell).lower()
        v = str(value).lower()
        if op == "contains":
            return v in c
        if op == "starts with":
            return c.startswith(v)
        if op == "ends with":
            return c.endswith(v)
        return c == v

    a = ToNumber(cell)
    b = ToNumber(value)
    if a is None or b is None:
        return False
    if op == ">":
        return a > b
    if op == ">=":
        return a >= b
    if op == "<":
        return a < b
    return a <= b


def EqualsIds(rows, field, value, algo):
    kind = ColumnKind(rows, field)
    if kind == "text":
        target = str(value).lower()
    else:
        target = ToNumber(value)
        if target is None:
            return set(), 0.0

    usable = [r for r in rows if kind == "text" or KeyOf(r, field, kind) is not None]
    prep_ms = 0.0
    if algo == "Binary Search":
        t0 = time.perf_counter()
        usable = RunSort(usable, [(field, False)], "Merge Sort")["rows"]     # binary needs sorted data
        prep_ms = (time.perf_counter() - t0) * 1000
        keys = [KeyOf(r, field, kind) for r in usable]
        hits = FindAllBinary(keys, target)
    else:
        keys = [KeyOf(r, field, kind) for r in usable]
        hits = FindAllLinear(keys, target)
    return {id(usable[i]) for i in hits}, prep_ms


def SearchRows(rows, conditions, algo="Linear Search"):
    t0 = time.perf_counter()
    all_ids = {id(r) for r in rows}
    result = None
    prep_total = 0.0
    for c in conditions:
        if c["op"] == "equals":
            ids, prep = EqualsIds(rows, c["field"], c["value"], algo)
            prep_total += prep
        else:
            if algo == "Binary Search":
                raise ValueError(f"Binary Search only works with 'equals', not '{c['op']}'. "
                                 f"Use Linear Search for this condition.")
            ids = {id(r) for r in rows if MatchOne(r, c["field"], c["op"], c["value"])}
        if c["negate"]:
            ids = all_ids - ids
        if result is None:
            result = ids
        elif c["join"] == "OR":
            result = result | ids
        else:
            result = result & ids
    found = [r for r in rows if id(r) in result]
    ms = (time.perf_counter() - t0) * 1000
    return {"rows": found, "time_ms": ms, "prep_ms": prep_total, "algo": algo,
            "complexity": SearchAlgorithms[algo], "n": len(rows)}