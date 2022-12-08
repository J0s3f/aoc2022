with open("input") as f:
    grid = [list(l) for l in f.read().strip().split("\n")]

max = 0
for i in range(1, len(grid) - 1):
    for j in range(1, len(grid[0]) - 1):
        visible_left = 0
        l = j - 1
        while l >= 0:
            visible_left += 1
            if not grid[i][l] < grid[i][j]:
                break
            l -= 1
        visible_right = 0
        r = j + 1
        while r < len(grid[0]):
            visible_right += 1
            if not grid[i][r] < grid[i][j]:
                break
            r += 1

        visible_top = 0
        t = i - 1
        while t >= 0:
            visible_top += 1
            if not grid[t][j] < grid[i][j]:
                break
            t -= 1

        visible_bottom = 0
        b = i + 1
        while b < len(grid):
            visible_bottom += 1
            if not grid[b][j] < grid[i][j]:
                break
            b += 1
        score = visible_top * visible_left * visible_bottom * visible_right
        if score > max:
            max = score

print(max)
