def parse_line(line: str):
    name, job = line.strip().split(': ')
    parts = job.split()
    if len(parts) == 1:
        return name, ('num', int(parts[0]))
    return name, ('op', parts[0], parts[1], parts[2])


with open('input') as f:
    monkeys = dict(parse_line(line) for line in f if line.strip())


def value(name):
    kind = monkeys[name]
    if kind[0] == 'num':
        return kind[1]
    _, left, op, right = kind
    a, b = value(left), value(right)
    if op == '+':
        return a + b
    if op == '-':
        return a - b
    if op == '*':
        return a * b
    return a // b


print('Part 1:', value('root'))
