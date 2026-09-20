import re
from math import prod

RESOURCES = ['ore', 'clay', 'obsidian', 'geode']


def parse_blueprint(line: str):
    numbers = list(map(int, re.findall(r'\d+', line)))
    blueprint_id = numbers[0]
    costs = {
        'ore': {'ore': numbers[1]},
        'clay': {'ore': numbers[2]},
        'obsidian': {'ore': numbers[3], 'clay': numbers[4]},
        'geode': {'ore': numbers[5], 'obsidian': numbers[6]},
    }
    return blueprint_id, costs


def max_geodes(costs, time_limit):
    max_needed = {
        res: max(costs[robot].get(res, 0) for robot in RESOURCES)
        for res in ['ore', 'clay', 'obsidian']
    }
    best = 0

    def dfs(time_left, resources, robots):
        nonlocal best
        best = max(best, resources['geode'] + robots['geode'] * time_left)
        upper_bound = resources['geode'] + robots['geode'] * time_left + time_left * (time_left - 1) // 2
        if upper_bound <= best:
            return

        for robot_type in ['geode', 'obsidian', 'clay', 'ore']:
            if robot_type in max_needed and robots[robot_type] >= max_needed[robot_type]:
                continue

            cost = costs[robot_type]
            feasible = True
            wait = 0
            for res, amount in cost.items():
                if resources[res] >= amount:
                    continue
                if robots[res] == 0:
                    feasible = False
                    break
                needed = amount - resources[res]
                wait = max(wait, -(-needed // robots[res]))
            if not feasible:
                continue

            new_time = time_left - wait - 1
            if new_time <= 0:
                continue

            new_resources = {r: resources[r] + robots[r] * (wait + 1) for r in RESOURCES}
            for res, amount in cost.items():
                new_resources[res] -= amount

            new_robots = dict(robots)
            new_robots[robot_type] += 1

            dfs(new_time, new_resources, new_robots)

    dfs(time_limit, {r: 0 for r in RESOURCES}, {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0})
    return best


with open('input') as f:
    blueprints = [parse_blueprint(line) for line in f if line.strip()]

top_results = [max_geodes(costs, 32) for _, costs in blueprints[:3]]
print('Part 2:', prod(top_results))
