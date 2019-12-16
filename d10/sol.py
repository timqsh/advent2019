from typing import NamedTuple, Tuple, List, Optional
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
    def __init__(self, li: List[str]):
        self.width = len(li[0])
        self.height = len(li)
        return super().__init__(li)

    def pos(self, pos: Pos) -> str:
        return self[pos.y][pos.x]

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

    def visible_num(self, pos: Pos) -> int:
        count = 0
        for a in self.asteroids():
            if a != pos and self.is_visible(pos, a):
                count += 1
        return count

    def best_pos(self) -> Tuple[Optional[Pos], int]:
        cur_max = 0
        cur_pos = None
        for a in self.asteroids():
            n = self.visible_num(a)
            if n > cur_max:
                cur_max = n
                cur_pos = a
        return cur_pos, cur_max


if __name__ == "__main__":
    import sys

    text = sys.stdin.read()

    grid = Grid(text.splitlines())

    res = grid.best_pos()
    print(res)
