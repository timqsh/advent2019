import itertools as it

start = 146810
end = 612564


def has_2_in_row(s: str) -> bool:
    return 2 in [len([*group]) for _, group in it.groupby(s)]
    # return any(s[i] == s[i + 1] for i in range(len(s) - 1))


total = 0
for i in range(start, end + 1):
    s = str(i)
    if has_2_in_row(s) and sorted(s) == list(s):
        total += 1

print(total)
