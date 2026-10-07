import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------- Task 1: Load data ----------
train = pd.read_csv('Train.csv')
test = pd.read_csv('Test.csv')

symptoms = list(train.columns[:-1])
label_col = train.columns[-1]


# ---------- Task 2: Scatter graph of each symptom vs label ----------
def plot_scatter():
    labels = sorted(train[label_col].unique())
    label_pos = {name: i for i, name in enumerate(labels)}
    y = train[label_col].map(label_pos).values

    # small random jitter so overlapping points are visible
    rng = np.random.default_rng(0)
    idx = rng.choice(len(train), size=min(1500, len(train)), replace=False)

    fig, axes = plt.subplots(5, 4, figsize=(16, 18))
    for ax, s in zip(axes.flat, symptoms):
        x = train[s].values[idx] + rng.uniform(-0.12, 0.12, len(idx))
        yy = y[idx] + rng.uniform(-0.2, 0.2, len(idx))
        ax.scatter(x, yy, s=4, alpha=0.4)
        ax.set_title(s, fontsize=9)
        ax.set_xticks([0, 1])
        ax.set_yticks(range(len(labels)))
        ax.set_yticklabels(labels, fontsize=8)
    plt.suptitle('Symptom vs Label')
    plt.tight_layout()
    plt.show()


def dependency_table():
    # % of cases in each disease where the symptom is present
    table = train.groupby(label_col)[symptoms].mean().T * 100
    print(table.round(1))


# ---------- Task 3: Euclidean distance ----------
def euclidean_distance(x, y):
    total = 0
    for i in range(len(x)):
        total += (x[i] - y[i]) ** 2
    return total ** 0.5


# ---------- Task 4: Assign label of the closest entry in main data ----------
def classify_entry(entry, data=None):
    if data is None:
        data = train
    X = data[symptoms].values.tolist()
    labels = data[label_col].values.tolist()

    best_dist = None
    best_label = None
    for i in range(len(X)):
        d = euclidean_distance(entry, X[i])
        if best_dist is None or d < best_dist:
            best_dist = d
            best_label = labels[i]
    return best_label


def classify_test():
    result = test.copy()
    predicted = []
    for row in test[symptoms].values.tolist():
        predicted.append(classify_entry(row))
    result[label_col] = predicted
    return result


# ---------- Task 6: Split main data into two parts ----------
def split_data(part2_size=500, seed=42):
    part2_full = train.sample(n=part2_size, random_state=seed)
    part1 = train.drop(part2_full.index)              # Part 1: no change, with labels
    part2_true_labels = part2_full[label_col].values.tolist()
    part2 = part2_full.drop(columns=[label_col])      # Part 2: without label
    return part1, part2, part2_true_labels


# ---------- Task 7: Run algorithm on Part 2 using Part 1 as reference ----------
def evaluate_split(part1, part2, true_labels):
    X = part1[symptoms].values.tolist()
    labels = part1[label_col].values.tolist()

    correct = 0
    for k, entry in enumerate(part2[symptoms].values.tolist()):
        best_dist = None
        best_label = None
        for i in range(len(X)):
            d = euclidean_distance(entry, X[i])
            if best_dist is None or d < best_dist:
                best_dist = d
                best_label = labels[i]
        if best_label == true_labels[k]:
            correct += 1
    return correct / len(true_labels) * 100


# ---------- Task 8: Recursive algorithm (divide and conquer) ----------
def recursive_nearest(entry, X, labels, lo, hi):
    # Base case: a single row
    if hi - lo == 1:
        return euclidean_distance(entry, X[lo]), labels[lo]

    mid = (lo + hi) // 2
    left = recursive_nearest(entry, X, labels, lo, mid)
    right = recursive_nearest(entry, X, labels, mid, hi)

    # On a tie, keep the left one (same as the iterative version)
    if left[0] <= right[0]:
        return left
    return right


def classify_entry_recursive(entry, data=None):
    if data is None:
        data = train
    X = data[symptoms].values.tolist()
    labels = data[label_col].values.tolist()
    return recursive_nearest(entry, X, labels, 0, len(X))[1]


# ---------- Task 9: Efficient algorithm ----------
def row_to_int(row):
    v = 0
    for b in row:
        v = (v << 1) | int(b)
    return v


def build_index(data):
    # Store each unique symptom pattern once (as an integer) with the label
    # of its first occurrence. Dictionary gives O(1) exact-match lookup.
    pattern_label = {}
    for row, lab in zip(data[symptoms].values.tolist(), data[label_col].values.tolist()):
        key = row_to_int(row)
        if key not in pattern_label:
            pattern_label[key] = lab
    keys = list(pattern_label.keys())
    return pattern_label, keys


def classify_entry_fast(entry, index):
    pattern_label, keys = index
    e = row_to_int(entry)

    if e in pattern_label:                 # exact match: distance 0
        return pattern_label[e]

    best_dist = None
    best_key = None
    for k in keys:
        d = (e ^ k).bit_count()            # Hamming distance (same ranking as Euclidean)
        if best_dist is None or d < best_dist:
            best_dist = d
            best_key = k
    return pattern_label[best_key]


def evaluate_split_fast(part1, part2, true_labels):
    index = build_index(part1)
    correct = 0
    for k, entry in enumerate(part2[symptoms].values.tolist()):
        if classify_entry_fast(entry, index) == true_labels[k]:
            correct += 1
    return correct / len(true_labels) * 100


if __name__ == '__main__':
    import time

    print(train.shape, test.shape)
    dependency_table()
    plot_scatter()
    print(classify_test()[[label_col]])

    part1, part2, part2_true_labels = split_data()
    print('Part1:', part1.shape, 'Part2:', part2.shape)
    print(part2.head(10))
    part1.to_csv('Part1_data.csv', index=False)
    part2.to_csv('Part2_data.csv', index=False)

    start = time.time()
    acc = evaluate_split(part1, part2, part2_true_labels)
    print('Accuracy: %.2f%%' % acc)
    t_old = time.time() - start
    print('Time taken: %.1f seconds' % t_old)

    # Task 8 check: recursive result should match the iterative result
    same = True
    for row in test[symptoms].values.tolist():
        if classify_entry(row) != classify_entry_recursive(row):
            same = False
    print('Recursive matches iterative on test data:', same)

    # Task 9: efficient algorithm vs previous algorithm
    start = time.time()
    acc_fast = evaluate_split_fast(part1, part2, part2_true_labels)
    t_fast = time.time() - start
    print('Efficient algorithm accuracy: %.2f%%' % acc_fast)
    print('Efficient algorithm time: %.3f seconds' % t_fast)
    print('Previous algorithm: %.2f%% in %.1f seconds' % (acc, t_old))