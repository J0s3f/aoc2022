NEIGHBORS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
CHECKS = [
    ('N', [(-1, -1), (-1, 0), (-1, 1)], (-1, 0)),
    ('S', [(1, -1), (1, 0), (1, 1)], (1, 0)),
    ('W', [(-1, -1), (0, -1), (1, -1)], (0, -1)),
    ('E', [(-1, 1), (0, 1), (1, 1)], (0, 1)),
]


def simulate(elves, rounds):
    order = CHECKS[:]
    round_no = 0
    while rounds is None or round_no < rounds:
        proposals = {}
        counts = {}
        for elf in elves:
            if not any((elf[0] + dr, elf[1] + dc) in elves for dr, dc in NEIGHBORS):
                continue
            for _, checks, move in order:
                if not any((elf[0] + dr, elf[1] + dc) in elves for dr, dc in checks):
                    target = (elf[0] + move[0], elf[1] + move[1])
                    proposals[elf] = target
                    counts[target] = counts.get(target, 0) + 1
                    break

        moved = False
        new_elves = set()
        for elf in elves:
            target = proposals.get(elf)
            if target is not None and counts[target] == 1:
                new_elves.add(target)
                moved = True
            else:
                new_elves.add(elf)
        elves = new_elves
        order.append(order.pop(0))
        round_no += 1
        if rounds is None and not moved:
            return elves, round_no

    return elves, round_no


with open('input') as f:
    elves = {(r, c) for r, line in enumerate(f) for c, ch in enumerate(line) if ch == '#'}

final, _ = simulate(elves, 10)
min_r = min(r for r, _ in final)
max_r = max(r for r, _ in final)
min_c = min(c for _, c in final)
max_c = max(c for _, c in final)
area = (max_r - min_r + 1) * (max_c - min_c + 1)
print('Part 1:', area - len(final))
