import re
from collections import deque


def parse_line(line: str):
    match = re.match(r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)', line.strip())
    name, rate, tunnels = match.group(1), int(match.group(2)), match.group(3).split(', ')
    return name, rate, tunnels


with open('input') as f:
    valves = {}
    graph = {}
    for line in f:
        name, rate, tunnels = parse_line(line)
        valves[name] = rate
        graph[name] = tunnels


def shortest_paths(start):
    dist = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in dist:
                dist[neighbor] = dist[node] + 1
                queue.append(neighbor)
    return dist


distances = {name: shortest_paths(name) for name in graph}
useful = [name for name, rate in valves.items() if rate > 0]
index = {name: i for i, name in enumerate(useful)}
n = len(useful)


def best_per_mask(time_budget):
    best = {}

    def visit(current, time_left, opened_mask, total):
        if total > best.get(opened_mask, -1):
            best[opened_mask] = total
        for valve in useful:
            bit = 1 << index[valve]
            if opened_mask & bit:
                continue
            remaining = time_left - distances[current][valve] - 1
            if remaining > 0:
                visit(valve, remaining, opened_mask | bit, total + remaining * valves[valve])

    visit('AA', time_budget, 0, 0)
    return best


scores = best_per_mask(26)
best_for_mask = [0] * (1 << n)
for mask, value in scores.items():
    best_for_mask[mask] = max(best_for_mask[mask], value)

for bit in range(n):
    b = 1 << bit
    for mask in range(1 << n):
        if mask & b:
            best_for_mask[mask] = max(best_for_mask[mask], best_for_mask[mask ^ b])

full_mask = (1 << n) - 1
best_total = 0
for mask in range(1 << n):
    total = best_for_mask[mask] + best_for_mask[full_mask ^ mask]
    if total > best_total:
        best_total = total

print('Part 2:', best_total)
