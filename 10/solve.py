import re
from collections.abc import Callable


class CPU:
    def __init__(self):
        self.cycle = 0
        self.x = 1
        self.next_break = 20
        self.break_every = 40
        self.diagnostics = []

    def run_cycle(self, op: Callable[[], None], num: int):
        self.cycle += num
        if self.cycle >= self.next_break:
            if self.cycle < self.next_break:
                op()
                self.diagnostics.append((self.next_break, self.x))
            else:
                self.diagnostics.append((self.next_break, self.x))
                op()
            self.next_break += self.break_every
        else:
            op()

    def addx(self, val: int):
        def op():
            self.x += val

        self.run_cycle(op, 2)

    def noop(self):
        self.run_cycle(lambda: None, 1)

    def __str__(self):
        return "CPU at Cycle " + str(self.cycle) + " with registers: X: " + str(self.x)

    def run_instruction(self, instruction: str):
        parts = re.match(r"\W*(\w+)(?:[^a-zA-Z0-9_-]+(-?\d+))?", instruction)
        instruction = parts.group(1)
        operand = parts.group(2)
        match instruction:
            case 'noop':
                self.noop()
            case 'addx':
                self.addx(int(operand))

    def get_signal_strength_total(self):
        return sum([x[0] * x[1] for x in self.diagnostics])


with open('input', 'r') as file:
    lines = file.readlines()

cpu = CPU()
for line in lines:
    cpu.run_instruction(line)

print(cpu.get_signal_strength_total())
