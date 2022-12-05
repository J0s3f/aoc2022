import copy
import re

with open('input', 'r') as file:
    lines = file.readlines()

crate_pattern = r'(?:(?:^| )(   |\[[A-Z]\]))'
crate_name_pattern = r'\[([A-Z])\]'
step_pattern = r'move (\d+) from (\d+) to (\d+)'

stacks = []
for line in lines:
    crates = re.findall(crate_pattern, line)

    if crates:
        for stack, crate in enumerate(crates):
            if crate.strip() == '':
                continue
            if stack >= len(stacks) or stacks[stack] is None:
                stacks.extend((stack - len(stacks) + 1) * [None])
                stacks[stack] = []
            id = re.match(crate_name_pattern, crate).group(1)
            stacks[stack].append(id)

steps = []
for line in lines:
    match = re.search(step_pattern, line)

    if match:
        count, source, destination = map(int, match.groups())
        steps.append((source, destination, count))


def part1(stack, steps):
    stacks = copy.deepcopy(stack)
    for source, destination, count in steps:
        source, destination = source - 1, destination - 1
        for i in range(count):
            crates = stacks[source][:1]

            crates.extend(stacks[destination])
            stacks[destination] = crates

            stacks[source] = stacks[source][1:]
    return stacks


def part2(stack, steps):
    stacks = copy.deepcopy(stack)
    for source, destination, count in steps:
        source, destination = source - 1, destination - 1
        crates = stacks[source][:count]

        crates.extend(stacks[destination])
        stacks[destination] = crates

        stacks[source] = stacks[source][count:]
    return stacks


for stack in part1(stacks, steps):
    print(stack[0], end='')
print('')
for stack in part2(stacks, steps):
    print(stack[0], end='')
print('')
