from typing import NamedTuple


class Vector(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other):
        return self.__class__(*[self[i] + other[i] for i in range(3)])

    def direction(self, other):
        return self.__class__(
            *[(self[i] < other[i]) - (self[i] > other[i]) for i in range(3)]
        )

    def energy(self):
        return sum(abs(self[i]) for i in range(3))


if __name__ == "__main__":
    import sys
    import re

    text = sys.stdin.read()
    pat = r"x=(-?\d+).*y=(-?\d+).*z=(-?\d+)"
    positions = [
        Vector(*map(int, re.search(pat, l).groups())) for l in text.splitlines()
    ]
    num = len(positions)
    velocities = [Vector(0, 0, 0) for _ in range(num)]
    steps = int(sys.argv[1])

    start_positions = positions[:]
    start_velocities = velocities[:]

    for coord in range(3):
        i = 0
        positions = start_positions[:]
        velocities = start_velocities[:]
        while True:
            i += 1
            for p1 in range(num):
                for p2 in range(p1 + 1, num):
                    velocities[p1] += positions[p1].direction(positions[p2])
                    velocities[p2] += positions[p2].direction(positions[p1])
            for p in range(num):
                positions[p] += velocities[p]
            if i % 1_000_000 == 0:
                print(i)
            if [p[coord] for p in positions] == [
                p[coord] for p in start_positions
            ] and [p[coord] for p in velocities] == [
                p[coord] for p in start_velocities
            ]:
                print(i)
                break

    print(positions)
    print(velocities)
    total = sum(pos.energy() * vel.energy() for pos, vel in zip(positions, velocities))
    print(total)
