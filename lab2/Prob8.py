import time
from funcs import InsertionSort, MergeSort, ShuffleArray

file = open("words.txt", "r")
words = []
for line in file:
    word = line.strip()    #strip remove \n and extra spaces at the end of line
    words.append(word)
file.close()

n = len(words)

wordsCopy1 = words[:]
wordsCopy2 = words[:]

start = time.time()
InsertionSort(wordsCopy1, 0, n-1)
end = time.time()
print(f"Insertion sort on original words.txt: {end - start} seconds")

start = time.time()
MergeSort(wordsCopy2, 0, n-1)
end = time.time()
print(f"Merge sort on original words.txt: {end - start} seconds")

wordsShuffled = words[:]
ShuffleArray(wordsShuffled, 0, n-1)

wordsCopy3 = wordsShuffled[:]
wordsCopy4 = wordsShuffled[:]

start = time.time()
InsertionSort(wordsCopy3, 0, n-1)
end = time.time()
print(f"Insertion sort on shuffled words: {end - start} seconds")

start = time.time()
MergeSort(wordsCopy4, 0, n-1)
end = time.time()
print(f"Merge sort on shuffled words: {end - start} seconds")