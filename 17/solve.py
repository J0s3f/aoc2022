SHAPES = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (1, 0), (0, 1), (1, 1)],
]

WIDTH = 7


def fits(occupied, shape, x, y):
    for dx, dy in shape:
        px, py = x + dx, y + dy
        if px < 0 or px >= WIDTH or py < 0:
            return False
        if (px, py) in occupied:
            return False
    return True


def simulate(jets, rock_count):
    occupied = set()
    height = 0
    jet_index = 0

    for i in range(rock_count):
        shape = SHAPES[i % len(SHAPES)]
        x, y = 2, height + 3

        while True:
            direction = jets[jet_index % len(jets)]
            jet_index += 1
            dx = 1 if direction == '>' else -1
            if fits(occupied, shape, x + dx, y):
                x += dx
            if fits(occupied, shape, x, y - 1):
                y -= 1
            else:
                break

        for dx, dy in shape:
            occupied.add((x + dx, y + dy))
        height = max(height, y + max(dy for _, dy in shape) + 1)

    return height


with open('input') as f:
    jets = f.read().strip()

print('Part 1:', simulate(jets, 2022))
