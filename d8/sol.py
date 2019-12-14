import sys
from collections import Counter

width = 25
height = 6

text = sys.stdin.read().strip()
digits = [*map(int, text)]

resolution = width * height
layers_num = len(digits) // resolution
layers = [digits[i : i + resolution] for i in range(layers_num)]

counters = [Counter(l) for l in layers]

counters = sorted(counters, key=lambda x: x[0])
print(*counters, sep="\n")
