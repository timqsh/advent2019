class Computer:
    def __init__(self, memory, input):
        self.memory = memory
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
            99: (self.f_stop, 0),
        }
        self.pointer = 0
        self.stopped = False

    def run(self):
        while not self.stopped:
            op_code_and_params = self.memory[self.pointer]
            self.pointer += 1

            params_code, op_code = divmod(op_code_and_params, 100)
            func, arg_num = self.func_and_arg_num[op_code]
            params = self.decode_params(params_code, arg_num)

            args = self.memory[self.pointer : self.pointer + arg_num]
            self.pointer += arg_num

            func(*args, *params)

    @staticmethod
    def decode_params(params_code, arg_num):
        result = []
        rest = params_code
        for i in range(arg_num):
            rest, value = divmod(rest, 10)
            result.append(value)
        return result

    def f_input(self, val, val_mode):
        self.memory[val] = self.input

    def f_output(self, v, val_mode):
        v = v if val_mode else self.memory[v]
        self.output.append(v)

    def f_add(self, a, b, res, a_mode, b_mode, res_mode):
        a = a if a_mode else self.memory[a]
        b = b if b_mode else self.memory[b]
        self.memory[res] = a + b

    def f_mul(self, a, b, res, a_mode, b_mode, res_mode):
        a = a if a_mode else self.memory[a]
        b = b if b_mode else self.memory[b]
        self.memory[res] = a * b

    def f_jump_true(self, condition, address, condition_mode, address_mode):
        condition = condition if condition_mode else self.memory[condition]
        address = address if address_mode else self.memory[address]
        if condition:
            self.pointer = address

    def f_jump_false(self, condition, address, condition_mode, address_mode):
        condition = condition if condition_mode else self.memory[condition]
        address = address if address_mode else self.memory[address]
        if not condition:
            self.pointer = address

    def f_less(self, a, b, res, a_mode, b_mode, res_mode):
        a = a if a_mode else self.memory[a]
        b = b if b_mode else self.memory[b]
        self.memory[res] = int(a < b)

    def f_equals(self, a, b, res, a_mode, b_mode, res_mode):
        a = a if a_mode else self.memory[a]
        b = b if b_mode else self.memory[b]
        self.memory[res] = int(a == b)

    def f_stop(self):
        self.stopped = True


if __name__ == "__main__":
    import sys

    text = input()
    memory = [*map(int, text.split(","))]

    computer = Computer(memory, input=int(sys.argv[1]))
    computer.run()

    print(computer.output)
