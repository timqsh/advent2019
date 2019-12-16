from typing import NamedTuple, Tuple, List
import math


class Pos(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Pos") -> "Pos":  # type: ignore
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Pos") -> "Pos":
        return self.__class__(self.x - other.x, self.y - other.y)

    def __mul__(self, other: int) -> "Pos":
        return self.__class__(self.x * other, self.y * other)

    def __floordiv__(self, other: int) -> "Pos":
        return self.__class__(self.x // other, self.y // other)

    def clockwise_around(self, p: "Pos") -> float:
        return -math.atan2(p.x - self.x, p.y - self.y)


class Grid(list):
    def __init__(self, li: List[List[str]]):
        self.width = len(li[0])
        self.height = len(li)
        super().__init__(li)

    def __getitem__(self, key):
        if isinstance(key, Pos):
            return self[key.y][key.x]
        else:
            return super().__getitem__(key)

    def __setitem__(self, key, value):
        if isinstance(key, Pos):
            self[key.y][key.x] = value
        else:
            super().__setitem__(key, value)

    def positions(self) -> List[Pos]:
        return [Pos(x, y) for x in range(self.width) for y in range(self.height)]

    def is_asteroid(self, pos: Pos) -> bool:
        return self[pos] == "#"

    def asteroids(self) -> List[Pos]:
        return [*filter(self.is_asteroid, self.positions())]

    def is_visible(self, p1: Pos, p2: Pos) -> bool:
        delta = p2 - p1
        divisor = math.gcd(delta.x, delta.y)
        step = delta // divisor

        for i in range(1, divisor):
            blocking_pos = p1 + (step * i)
            if self.is_asteroid(blocking_pos):
                return False
        return True

    def asteroids_visible_from(self, pos: Pos) -> List[Pos]:
        return [a for a in self.asteroids() if a != pos and self.is_visible(pos, a)]

    def best_pos(self) -> Tuple[Pos, int]:
        cur_max = 0
        cur_pos = None
        for a in self.asteroids():
            n = len(self.asteroids_visible_from(a))
            if n > cur_max:
                cur_max = n
                cur_pos = a
        assert cur_pos is not None, "no asteroid found :("
        return cur_pos, cur_max


if __name__ == "__main__":
    import sys

    text = sys.stdin.read()

    grid = Grid([[*s] for s in text.splitlines()])
    best_pos, best_num = grid.best_pos()
    print(f"best: {best_pos} ({best_num})")

    i = 0
    while True:
        asteroids = grid.asteroids_visible_from(best_pos)
        if not asteroids:
            break
        asteroids.sort(key=best_pos.clockwise_around)
        for asteroid in asteroids:
            i += 1
            grid[asteroid] = "."
            if i == 200:
                print(f"{i}: {asteroid}")
