class Computer:
    def __init__(self, memory, input):
        self.memory = memory + [0] * 100_000
        self.input = input
        self.output = []
        self.func_and_arg_num = {
            1: (self.f_add, 3),
            2: (self.f_mul, 3),
            3: (self.f_input, 1),
            4: (self.f_output, 1),
            5: (self.f_jump_true, 2),
            6: (self.f_jump_false, 2),
            7: (self.f_less, 3),
            8: (self.f_equals, 3),
            9: (self.f_shift_base, 1),
            99: (self.f_stop, 0),
        }
        self.pointer = 0
        self.base = 0
        self.stopped = False
        self.waiting = False

    def run(self):
        self.waiting = False
        while not self.stopped and not self.waiting:
            op_code_and_params = self.memory[self.pointer]
            self.pointer += 1

            params_code, op_code = divmod(op_code_and_params, 100)
            func, arg_num = self.func_and_arg_num[op_code]
            params = self.decode_params(params_code, arg_num)

            args = [
                self.pointer + i
                if params[i] == 1
                else self.memory[self.pointer + i]
                + (self.base if params[i] == 2 else 0)
                for i in range(arg_num)
            ]
            func(*args)
            self.pointer += arg_num

    @staticmethod
    def decode_params(params_code, arg_num):
        result = []
        rest = params_code
        for i in range(arg_num):
            rest, value = divmod(rest, 10)
            result.append(value)
        return result

    def f_input(self, val):
        if self.input:
            self.memory[val] = self.input.pop(0)
        else:
            self.waiting = True
            self.pointer -= 2

    def f_output(self, v):
        self.output.append(self.memory[v])

    def f_add(self, a, b, res):
        self.memory[res] = self.memory[a] + self.memory[b]

    def f_mul(self, a, b, res):
        self.memory[res] = self.memory[a] * self.memory[b]

    def f_jump_true(self, condition, address):
        if self.memory[condition]:
            self.pointer = self.memory[address]

    def f_jump_false(self, condition, address):
        if not self.memory[condition]:
            self.pointer = self.memory[address]

    def f_less(self, a, b, res):
        self.memory[res] = int(self.memory[a] < self.memory[b])

    def f_equals(self, a, b, res):
        self.memory[res] = int(self.memory[a] == self.memory[b])

    def f_shift_base(self, v):
        self.base += self.memory[v]

    def f_stop(self):
        self.stopped = True


if __name__ == "__main__":
    import sys
    import itertools as it

    text = sys.stdin.read()
    memory = [*map(int, text.split(","))]

    computer = Computer(memory, [])
    computer.run()

    print(f"{computer.output}")
