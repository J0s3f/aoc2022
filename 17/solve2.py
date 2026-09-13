SHAPES = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (1, 0), (0, 1), (1, 1)],
]

WIDTH = 7
PROFILE_DEPTH = 40


def fits(occupied, shape, x, y):
    for dx, dy in shape:
        px, py = x + dx, y + dy
        if px < 0 or px >= WIDTH or py < 0:
            return False
        if (px, py) in occupied:
            return False
    return True


def column_heights(occupied, height):
    heights = []
    for x in range(WIDTH):
        for y in range(height - 1, max(height - PROFILE_DEPTH, -1) - 1, -1):
            if (x, y) in occupied:
                heights.append(height - y)
                break
        else:
            heights.append(height - max(height - PROFILE_DEPTH, 0))
    return tuple(heights)


def simulate(jets, rock_count):
    occupied = set()
    height = 0
    jet_index = 0
    seen = {}
    extra_height = 0
    rock_index = 0

    while rock_index < rock_count:
        shape_id = rock_index % len(SHAPES)
        shape = SHAPES[shape_id]
        x, y = 2, height + 3

        while True:
            direction = jets[jet_index % len(jets)]
            step = jet_index % len(jets)
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

        if extra_height == 0:
            key = (shape_id, step, column_heights(occupied, height))
            if key in seen:
                prev_rock_index, prev_height = seen[key]
                cycle_len = rock_index - prev_rock_index
                cycle_height = height - prev_height
                remaining = rock_count - rock_index - 1
                cycles = remaining // cycle_len
                extra_height = cycles * cycle_height
                rock_index += cycles * cycle_len
            else:
                seen[key] = (rock_index, height)

        rock_index += 1

    return height + extra_height


with open('input') as f:
    jets = f.read().strip()

print('Part 2:', simulate(jets, 1000000000000))
