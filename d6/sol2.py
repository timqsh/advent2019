import sys

text = sys.stdin.read()

di = dict(l.split(")")[::-1] for l in text.splitlines())

dist = {}
i = 0
cur = "YOU"
while cur != "COM":
    cur = di[cur]
    dist[cur] = i
    i += 1

i = 0
cur = "SAN"
while cur != "COM":
    if cur in dist:
        total = i + dist[cur]
        print(total - 1)
        break
    cur = di[cur]
    i += 1
