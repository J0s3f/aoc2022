from math import lcm

with open('input') as f:
    grid = [line.rstrip('\n') for line in f if line.strip()]

height = len(grid) - 2
width = len(grid[0]) - 2

blizzards = []
for r, row in enumerate(grid):
    for c, ch in enumerate(row):
        if ch in '><^v':
            blizzards.append((r, c, ch))

start = (0, grid[0].index('.'))
end = (len(grid) - 1, grid[-1].index('.'))

period = lcm(height, width)
occupied_cache = {}


def occupied_at(t):
    if t in occupied_cache:
        return occupied_cache[t]
    t_mod = t % period
    occ = set()
    for r, c, d in blizzards:
        if d == '>':
            nc = (c - 1 + t_mod) % width + 1
            occ.add((r, nc))
        elif d == '<':
            nc = (c - 1 - t_mod) % width + 1
            occ.add((r, nc))
        elif d == 'v':
            nr = (r - 1 + t_mod) % height + 1
            occ.add((nr, c))
        else:
            nr = (r - 1 - t_mod) % height + 1
            occ.add((nr, c))
    occupied_cache[t_mod] = occ
    return occ


def travel(start, end, start_time):
    positions = {start}
    t = start_time
    while end not in positions:
        t += 1
        occ = occupied_at(t)
        new_positions = set()
        for r, c in positions:
            for dr, dc in [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if (nr, nc) == start or (nr, nc) == end:
                    new_positions.add((nr, nc))
                elif 1 <= nr <= height and 1 <= nc <= width and (nr, nc) not in occ:
                    new_positions.add((nr, nc))
        positions = new_positions
    return t


print('Part 1:', travel(start, end, 0))
