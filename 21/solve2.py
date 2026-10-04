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


def has_humn(name):
    if name == 'humn':
        return True
    kind = monkeys[name]
    if kind[0] == 'num':
        return False
    _, left, _, right = kind
    return has_humn(left) or has_humn(right)


def solve(name, target):
    if name == 'humn':
        return target
    _, left, op, right = monkeys[name]
    if has_humn(left):
        rv = value(right)
        if op == '+':
            new_target = target - rv
        elif op == '-':
            new_target = target + rv
        elif op == '*':
            new_target = target // rv
        else:
            new_target = target * rv
        return solve(left, new_target)
    else:
        lv = value(left)
        if op == '+':
            new_target = target - lv
        elif op == '-':
            new_target = lv - target
        elif op == '*':
            new_target = target // lv
        else:
            new_target = lv // target
        return solve(right, new_target)


_, root_left, _, root_right = monkeys['root']
if has_humn(root_left):
    print('Part 2:', solve(root_left, value(root_right)))
else:
    print('Part 2:', solve(root_right, value(root_left)))
