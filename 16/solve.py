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


scores = best_per_mask(30)
print('Part 1:', max(scores.values()))
