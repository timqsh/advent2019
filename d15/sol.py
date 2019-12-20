from typing import List, NamedTuple
import sys


class Computer:
    POSITION_MODE = 0
    IMMEDIATE_MODE = 1
    RELATIVE_MODE = 2
    JUMPED = 1

    def __init__(self, memory: List[int], input: List[int] = None):
        self.memory = memory + [0] * 100_000
        self.input = input or []
        self.output: List[int] = []
        self.func_and_arg_num = {
            1: (self.add, 3),
            2: (self.mul, 3),
            3: (self.read, 1),
            4: (self.write, 1),
            5: (self.jump_true, 2),
            6: (self.jump_false, 2),
            7: (self.less, 3),
            8: (self.equals, 3),
            9: (self.shift_base, 1),
            99: (self.stop, 0),
        }
        self.pointer = 0
        self.base = 0
        self.iteration = 0
        self.stopped = False
        self.waiting = False

    def run(self):
        self.waiting = False
        while not self.stopped and not self.waiting:
            op_code_and_params = self.memory[self.pointer]
            params_code, op_code = divmod(op_code_and_params, 100)
            func, arg_num = self.func_and_arg_num[op_code]
            params = self.decode_params(params_code, arg_num)
            args = self.read_args(params, arg_num)

            jumped = func(*args)
            if not jumped:
                self.pointer += arg_num + 1
            self.iteration += 1

    @staticmethod
    def decode_params(params_code: int, arg_num: int) -> List[int]:
        result = []
        rest = params_code
        for i in range(arg_num):
            rest, value = divmod(rest, 10)
            result.append(value)
        return result

    def read_args(self, params: List[int], arg_num: int) -> List[int]:
        args = []
        for i in range(arg_num):
            pos = self.pointer + i + 1
            if params[i] == self.POSITION_MODE:
                arg = self.memory[pos]
            elif params[i] == self.IMMEDIATE_MODE:
                arg = pos
            elif params[i] == self.RELATIVE_MODE:
                arg = self.memory[pos] + self.base
            else:
                raise ValueError(f"unexpected param mode {params[i]}")
            args.append(arg)
        return args

    def add(self, a, b, res):
        self.memory[res] = self.memory[a] + self.memory[b]

    def mul(self, a, b, res):
        self.memory[res] = self.memory[a] * self.memory[b]

    def read(self, val):
        if self.input:
            self.memory[val] = self.input.pop(0)
        else:
            self.waiting = True
            return self.JUMPED

    def write(self, v):
        self.output.append(self.memory[v])

    def jump_true(self, condition, address):
        if self.memory[condition]:
            self.pointer = self.memory[address]
            return self.JUMPED

    def jump_false(self, condition, address):
        if not self.memory[condition]:
            self.pointer = self.memory[address]
            return self.JUMPED

    def less(self, a, b, res):
        self.memory[res] = int(self.memory[a] < self.memory[b])

    def equals(self, a, b, res):
        self.memory[res] = int(self.memory[a] == self.memory[b])

    def shift_base(self, v):
        self.base += self.memory[v]

    def stop(self):
        self.stopped = True


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


class Grid:
    def __init__(self, size):
        self._grid = [[0] * size for _ in size]

    def __getitem__(self, key: Pos):
        return self._grid[key.y][key.x]

    def __setitem__(self, key: Pos, value: int):
        self._grid[key.y][key.x] == value


class Robot:
    DIRECTIONS = {1: Pos(0, -1), 2: Pos(0, 1), 3: Pos(-1, 0), 4: Pos(1, 0)}

    def __init__(self, gridsize, program):
        self.pos = Pos(gridsize // 2, gridsize // 2)
        self.computer = Computer(program)
        self.grid = Grid(gridsize)
        self.oxygen_station_pos = None

    def path_to_oxygen_station(self):
        while not self.oxygen_station_pos:
            pos = self.nearest_unexplored()
            self.move_to(pos)

    def nearest_unexplored(self) -> Pos:
        ...

    def move_to(self, target: Pos) -> None:
        ...

    def bfs(self, start: Pos, end: Pos) -> List[Pos]:
        ...

    def move(self, direction: int):
        self.pos = self.DIRECTIONS[direction]


def main():
    text = sys.stdin.read()
    program = [*map(int, text.split(","))]
    robot = Robot(gridsize=1000, program=program)
    path = robot.path_to_oxygen_station()
    print(len(path))


if __name__ == "__main__":
    main()
