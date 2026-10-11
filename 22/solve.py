import re

with open('input') as f:
    content = f.read()

grid_text, path_text = content.split('\n\n')
grid = grid_text.split('\n')
height = len(grid)
width = max(len(row) for row in grid)
grid = [row.ljust(width) for row in grid]

moves = re.findall(r'\d+|[LR]', path_text.strip())

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def tile(row, col):
    if 0 <= row < height and 0 <= col < width:
        return grid[row][col]
    return ' '


row = 0
col = grid[0].index('.')
facing = 0

for move in moves:
    if move == 'L':
        facing = (facing - 1) % 4
    elif move == 'R':
        facing = (facing + 1) % 4
    else:
        for _ in range(int(move)):
            dr, dc = DIRS[facing]
            nr, nc = row + dr, col + dc
            if tile(nr, nc) == ' ':
                nr, nc = row, col
                while tile(nr - dr, nc - dc) != ' ':
                    nr, nc = nr - dr, nc - dc
            if tile(nr, nc) == '#':
                break
            row, col = nr, nc

password = 1000 * (row + 1) + 4 * (col + 1) + facing
print('Part 1:', password)
