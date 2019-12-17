from typing import NamedTuple, List
import math


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

    def clockwise_around(self, p: "Pos") -> float:
        return -math.atan2(p.x - self.x, p.y - self.y)


class Robot:
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    SIZE = 100

    step = {
        UP: Pos(0, -1),
        RIGHT: Pos(1, 0),
        DOWN: Pos(0, 1),
        LEFT: Pos(-1, 0),
    }

    def __init__(self):
        self.direction = self.UP
        self.pos = Pos(self.SIZE, self.SIZE) // 2
        self.grid = [[0] * self.SIZE for i in range(self.SIZE)]
        self.painted_pos = set()

    def rotate(self, rotate_direction):
        if rotate_direction == 1:
            self.direction += 1
        elif rotate_direction == 0:
            self.direction -= 1
        self.direction %= 4

    def move(self):
        self.pos += self.step[self.direction]

    def paint(self, color):
        self.grid[self.pos.y][self.pos.x] = color
        self.painted_pos.add(self.pos)

    def get_color(self):
        return self.grid[self.pos.y][self.pos.x]

    def process_input(self, color, rotate_direction):
        self.paint(color)
        self.rotate(rotate_direction)
        self.move()


if __name__ == "__main__":
    import sys

    text = sys.stdin.read()
    memory = [*map(int, text.split(","))]

    computer = Computer(memory)
    if len(sys.argv) > 1:
        computer.input.append(int(sys.argv[1]))
    robot = Robot()
    robot.grid[robot.pos.y][robot.pos.x] = 1

    while not computer.stopped:
        color = robot.get_color()
        computer.input.append(color)
        computer.run()
        new_color = computer.output.pop(0)
        direction = computer.output.pop(0)
        robot.process_input(new_color, direction)

    print(f"{len(robot.painted_pos)}")
    print(*["".join(map(lambda i: "#" if i else ".", l)) for l in robot.grid], sep="\n")
