def part1(pairs):
    num_overlapping_pairs = 0
    for pair in pairs:
        r1, r2 = pair.split(',')

        r1_start, r1_end = map(int, r1.split('-'))
        r2_start, r2_end = map(int, r2.split('-'))

        if (r1_start <= r2_start and r1_end >= r2_end) or (r2_start <= r1_start and r2_end >= r1_end):
            num_overlapping_pairs += 1
    return num_overlapping_pairs


def part2(pairs):
    num_overlapping_pairs = 0

    for pair in pairs:
        r1, r2 = pair.split(',')

        r1_start, r1_end = map(int, r1.split('-'))
        r2_start, r2_end = map(int, r2.split('-'))

        if r1_start <= r2_end and r2_start <= r1_end:
            num_overlapping_pairs += 1
    return num_overlapping_pairs


with open('input', 'r') as f:
    lines = [line.strip() for line in f]

print(part1(lines))
print(part2(lines))
