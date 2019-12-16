from typing import NamedTuple, Tuple, List, Callable
from math import gcd


class Pos(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Pos"):  # type: ignore
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Pos"):
        return self.__class__(self.x - other.x, self.y - other.y)

    def __mul__(self, other: int):
        return self.__class__(self.x * other, self.y * other)

    def __floordiv__(self, other: int):
        return self.__class__(self.x // other, self.y // other)


class Grid(list):
    def __init__(self, li: List[List[str]]):
        self.width = len(li[0])
        self.height = len(li)
        return super().__init__(li)

    def pos(self, pos: Pos) -> str:
        return self[pos.y][pos.x]

    def set_pos(self, pos: Pos, value: str) -> None:
        self[pos.y][pos.x] = value

    def asteroids(self) -> List[Pos]:
        res = []
        for x in range(self.width):
            for y in range(self.height):
                p = Pos(x, y)
                if self.pos(p) == "#":
                    res.append(p)
        return res

    def is_visible(self, p1: Pos, p2: Pos) -> bool:
        dx = p2.x - p1.x
        dy = p2.y - p1.y

        div = gcd(dx, dy)
        step = Pos(dx, dy) // div

        for i in range(1, div):
            pos = p1 + (step * i)
            if self.pos(pos) == "#":
                return False
        return True

    def visible_from(self, pos: Pos) -> List[Pos]:
        res = []
        for a in self.asteroids():
            if a != pos and self.is_visible(pos, a):
                res.append(a)
        return res

    def best_pos(self) -> Tuple[Pos, int]:
        cur_max = 0
        cur_pos: Pos
        for a in self.asteroids():
            n = len(self.visible_from(a))
            if n > cur_max:
                cur_max = n
                cur_pos = a
        return cur_pos, cur_max


def clockwise_around(center: Pos) -> Callable:
    def clockwise_order(p: Pos) -> Tuple[int, float]:
        dy, dx = (p.y - center.y), (p.x - center.x)
        if dx == 0 and dy < 0:  # 12 o'clock
            return 1, 0
        elif dx > 0:
            return 2, dy / dx
        elif dx == 0 and dy > 0:  # 6 o'clock
            return 3, 0
        elif dx < 0:
            return 4, dy / dx
        else:
            raise ValueError("sorting error")

    return clockwise_order


if __name__ == "__main__":
    import sys

    text = sys.stdin.read()

    grid = Grid([[*s] for s in text.splitlines()])
    best_pos, best_num = grid.best_pos()
    print(f"best: {best_pos} ({best_num})")

    i = 0
    while True:
        asteroids = grid.visible_from(best_pos)
        if not asteroids:
            break

        asteroids.sort(key=clockwise_around(best_pos))
        for asteroid in asteroids:
            i += 1
            grid.set_pos(asteroid, ".")
            if i == 200:
                print(f"{i}: {asteroid}")
