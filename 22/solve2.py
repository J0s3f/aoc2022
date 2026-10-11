import re
from math import isqrt

with open('input') as f:
    content = f.read()

grid_text, path_text = content.split('\n\n')
grid = grid_text.split('\n')
height = len(grid)
width = max(len(row) for row in grid)
grid = [row.ljust(width) for row in grid]

moves = re.findall(r'\d+|[LR]', path_text.strip())

filled = sum(row.count('.') + row.count('#') for row in grid)
S = isqrt(filled // 6)


def axis_vec(axis, sign):
    v = [0, 0, 0]
    v[axis] = sign
    return tuple(v)


def propagate(direction, n, r, d):
    if direction == 'right':
        return r, tuple(-x for x in n), d
    if direction == 'left':
        return tuple(-x for x in r), n, d
    if direction == 'down':
        return d, r, tuple(-x for x in n)
    return tuple(-x for x in d), r, n


blocks = set()
for br in range(height // S):
    for bc in range(width // S):
        if grid[br * S][bc * S] != ' ':
            blocks.add((br, bc))

start_block = min(blocks)
orientation = {start_block: ((0, 0, 1), (1, 0, 0), (0, 1, 0))}
queue = [start_block]
while queue:
    br, bc = queue.pop()
    n, r, d = orientation[(br, bc)]
    for direction, (dbr, dbc) in [('right', (0, 1)), ('left', (0, -1)), ('down', (1, 0)), ('up', (-1, 0))]:
        nb = (br + dbr, bc + dbc)
        if nb in blocks and nb not in orientation:
            orientation[nb] = propagate(direction, n, r, d)
            queue.append(nb)

face_by_normal = {}
for block, (n, r, d) in orientation.items():
    face_by_normal[n] = (block, r, d)

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def scale(a, k):
    return (a[0] * k, a[1] * k, a[2] * k)


def point_3d(block, i, j):
    n, r, d = orientation[block]
    return add(scale(n, S - 1), add(scale(r, 2 * j - (S - 1)), scale(d, 2 * i - (S - 1))))


def step(block, i, j, facing):
    dr, dc = DIRS[facing]
    ni, nj = i + dr, j + dc
    if 0 <= ni < S and 0 <= nj < S:
        return block, ni, nj, facing

    _, r, d = orientation[block]
    p = point_3d(block, i, j)
    p = add(p, scale(r, 2 * dc))
    p = add(p, scale(d, 2 * dr))

    axes = [0, 1, 2]
    new_axis = max(axes, key=lambda a: abs(p[a]))
    new_sign = 1 if p[new_axis] > 0 else -1
    new_n = axis_vec(new_axis, new_sign)

    new_block, new_r, new_d = face_by_normal[new_n]

    a_new = dot(p, new_r)
    b_new = dot(p, new_d)
    new_j = (a_new + (S - 1)) // 2
    new_i = (b_new + (S - 1)) // 2

    old_tangent = d if dc != 0 else r
    tangent_axis = next(k for k in range(3) if old_tangent[k] != 0)
    new_r_axis = next(k for k in range(3) if new_r[k] != 0)
    if new_r_axis == tangent_axis:
        new_facing = 1 if new_i == 0 else 3
    else:
        new_facing = 0 if new_j == 0 else 2

    return new_block, new_i, new_j, new_facing


block, i, j = start_block, 0, 0
facing = 0

for move in moves:
    if move == 'L':
        facing = (facing - 1) % 4
    elif move == 'R':
        facing = (facing + 1) % 4
    else:
        for _ in range(int(move)):
            nb, ni, nj, nf = step(block, i, j, facing)
            br, bc = nb
            if grid[br * S + ni][bc * S + nj] == '#':
                break
            block, i, j, facing = nb, ni, nj, nf

br, bc = block
row = br * S + i
col = bc * S + j
password = 1000 * (row + 1) + 4 * (col + 1) + facing
print('Part 2:', password)
