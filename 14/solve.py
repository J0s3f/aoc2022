from enum import Enum


class Cave:
    def __init__(self, rocks_in: list, part2=False):
        rocks = rocks_in.copy() if part2 else rocks_in
        sand_source = (500, 0)
        self.part2 = part2

        all_points = [p for r in rocks for p in r]
        all_points.append(sand_source)
        min_x = min(p[0] for p in all_points)
        min_y = 0
        max_x = max(p[0] for p in all_points)
        max_y = max(p[1] for p in all_points)

        if part2:
            max_y += 2
            max_possible_spread = max_y - min_y
            min_x -= max_possible_spread
            max_x += max_possible_spread
            rocks.append([(min_x, max_y), (max_x, max_y)])
        self.width = max_x - min_x
        self.height = max_y - min_y
        self.x_offset = min_x
        self.y_offset = min_y
        self.sand_source = self.normalize(sand_source)

        normalized = list(map(lambda line: [self.normalize(p) for p in line], rocks))

        self.data = [['.' for _ in range(self.width + 1)] for _ in range(self.height + 1)]

        self.set(self.sand_source, '+')

        self.draw_stones(normalized)

    def draw_stones(self, stones):
        for line in stones:
            if not line:
                continue
            start = line[0]
            for end in line[1:]:
                if start[0] == end[0]:
                    step = 1 if start[1] < end[1] else -1
                    for i in range(start[1], end[1] + step, step):
                        self.draw_stone((start[0], i))
                else:
                    step = 1 if start[0] < end[0] else -1
                    for i in range(start[0], end[0] + step, step):
                        self.draw_stone((i, start[1]))
                start = end

    def draw_stone(self, pos):
        self.data[pos[1]][pos[0]] = '#'

    def simulate_sand(self):
        counter = 0

        NextPos = Enum('NextPos', ['FULL', 'INFINITY'])

        def below(pos):
            return pos[0], pos[1] + 1

        def left(pos):
            return pos[0] - 1, pos[1]

        def right(pos):
            return pos[0] + 1, pos[1]

        def next_pos(pos):
            if not self.in_range(below(pos)):
                return NextPos.INFINITY
            if self.get(below(pos)) == '.':
                return below(pos)
            elif self.get(left(below(pos))) == '.':
                return left(below(pos))
            elif self.get(right(below(pos))) == '.':
                return right(below(pos))
            return NextPos.FULL

        while True:
            s = self.sand_source
            n = next_pos(s)
            while n != NextPos.FULL and n != NextPos.INFINITY:
                s = n
                n = next_pos(s)
            if n == NextPos.FULL and s != self.sand_source:
                self.set(s, 'o')
                counter += 1
            elif n == NextPos.INFINITY:
                return counter
            else:
                return counter + 1 if self.part2 else NextPos.FULL

    def get(self, pos: tuple[int, int]):
        return self.data[pos[1]][pos[0]]

    def set(self, pos: tuple[int, int], val: str):
        self.data[pos[1]][pos[0]] = val

    def in_range(self, pos):
        return 0 <= pos[0] <= self.width and 0 <= pos[1] <= self.height

    def normalize(self, point: tuple):
        return point[0] - self.x_offset, point[1] - self.y_offset

    def denormalize(self, point: tuple):
        return point[0] + self.x_offset, point[1] + self.y_offset

    def __str__(self):
        return '\n'.join(map(lambda l: ''.join([''.join(s) for s in l]), self.data))


with open("input") as f:
    rocks = [list(map(lambda r: tuple(map(int, r.split(","))), ln.strip().split("->"))) for ln in f.readlines()]

cave = Cave(rocks)

res = cave.simulate_sand()

print("Part 1: ", res)

cave2 = Cave(rocks, part2=True)

res = cave2.simulate_sand()

print("Part 2: ", res)
