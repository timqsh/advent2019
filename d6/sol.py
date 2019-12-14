import sys

text = sys.stdin.read()

di = dict(l.split(")")[::-1] for l in text.splitlines())
total = 0
for k in di:
    while k != "COM":
        k = di[k]
        total += 1

print(total)
