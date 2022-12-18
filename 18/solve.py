import re


def calculate_surface_area(scanned_lava_droplet: set[tuple[int, int, int]]):
    surface_area = 0

    for x, y, z in scanned_lava_droplet:
        surface_area += 6 - sum(
            [(x + 1, y, z) in scanned_lava_droplet, (x - 1, y, z) in scanned_lava_droplet,
             (x, y + 1, z) in scanned_lava_droplet,
             (x, y - 1, z) in scanned_lava_droplet, (x, y, z + 1) in scanned_lava_droplet,
             (x, y, z - 1) in scanned_lava_droplet])

    return surface_area


def calculate_exterior_surface_area(scanned_lava_droplet: set[tuple[int, int, int]]):
    surface_area = calculate_surface_area(scanned_lava_droplet)
    max_x = max(x for x, _, _ in scanned_lava_droplet)
    max_y = max(y for _, y, _ in scanned_lava_droplet)
    max_z = max(z for _, _, z in scanned_lava_droplet)
    area = {(x, y, z) for x in range(max_x + 2) for y in range(max_y + 2) for z in range(max_z + 2)}
    empty_space = list(area - scanned_lava_droplet)
    air_pockets = []

    while empty_space:
        to_check = [empty_space[0]]
        current_bubble = set()

        while len(to_check):
            next_air = to_check.pop()

            if next_air in empty_space:
                current_bubble.add(next_air)
                empty_space.remove(next_air)

                x, y, z = next_air
                for dx, dy, dz in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
                    to_check.append((x + dx, y + dy, z + dz))

        if (0, 0, 0) not in current_bubble:
            air_pockets.append(current_bubble)

    pockets_surface_area = [calculate_surface_area(pocket) for pocket in air_pockets]

    return surface_area - sum(pockets_surface_area)


def parse_line(line: str) -> tuple[int, int, int] | None:
    pattern = r'(-?\d+),(-?\d+),(-?\d+)'
    match = re.search(pattern, line)
    if match:
        x, y, z = map(int, match.groups())
        return x, y, z
    return None


with open('input', 'r') as file:
    scanned_lava_droplet = {s for line in file.readlines() if (s := parse_line(line)) is not None}

surface_area = calculate_surface_area(scanned_lava_droplet)

print("Part 1:", surface_area)

exterior_surface_area = calculate_exterior_surface_area(scanned_lava_droplet)

print("Part 2:", exterior_surface_area)
