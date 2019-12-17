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


if __name__ == "__main__":
    import sys
    import itertools as it

    text = sys.stdin.read()
    memory = [*map(int, text.split(","))]

    computer = Computer(memory)
    if len(sys.argv) > 1:
        computer.input.append(int(sys.argv[1]))
    computer.memory[0] == 2  # free mode

    grid = [[0] * 100 for _ in range(100)]
    computer.run()
    objects = [
        computer.output[i * 3 : i * 3 + 3] for i in range(len(computer.output) // 3)
    ]
    for o in objects:
        grid[o[0]][o[1]] = o[2]

    print(*["".join(map(str, line)) for line in grid], sep="\n")
    print(f"{len([o for o in it.chain(*grid) if o==2])}")
