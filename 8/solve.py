with open("input") as f:
    grid = [list(l) for l in f.read().strip().split("\n")]

visited = set()
visible = len(grid[0])
# top to bottom
highest = grid[0].copy()
for i in range(1, len(grid) - 1):
    for j in range(1, len(grid[0]) - 1):
        if grid[i][j] > highest[j]:
            highest[j] = grid[i][j]
            if not (i, j) in visited:
                visited.add((i, j))
                visible += 1
# bottom to top
b = len(grid) - 1
visible += len(grid[b])
highest = grid[b].copy()
for i in range(len(grid) - 2, 0, -1):
    for j in range(1, len(grid[0]) - 1):
        if grid[i][j] > highest[j]:
            highest[j] = grid[i][j]
            if not (i, j) in visited:
                visited.add((i, j))
                visible += 1

# left to right
visible += len(grid) - 2
highest = [l[0] for l in grid]
for j in range(1, len(grid[0]) - 1):
    for i in range(1, len(grid) - 1):
        if grid[i][j] > highest[i]:
            highest[i] = grid[i][j]
            if not (i, j) in visited:
                visited.add((i, j))
                visible += 1

# right to left
visible += len(grid) - 2
r = len(grid[0]) - 1
highest = [l[r] for l in grid]
for j in range(len(grid[0]) - 2, 0, -1):
    for i in range(1, len(grid) - 1):
        if grid[i][j] > highest[i]:
            highest[i] = grid[i][j]
            if not (i, j) in visited:
                visited.add((i, j))
                visible += 1

print(visible)
