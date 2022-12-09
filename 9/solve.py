import re


class Grid:
    def __init__(self, rope_length):
        self.rope = [[0, 0] for _ in range(rope_length)]
        self.visited = set()
        self.visited.add(tuple(self.rope[-1]))

    def head(self):
        return self.rope[0]

    def tail(self):
        return self.rope[-1]

    def move(self, direction):
        match direction:
            case 'U':
                self.head()[1] += 1
            case 'D':
                self.head()[1] -= 1
            case 'R':
                self.head()[0] += 1
            case 'L':
                self.head()[0] -= 1
        self.follow_tail()
        self.visited.add(tuple(self.tail()))

    def follow_tail(self):
        for i in range(1, len(self.rope)):
            diff = (self.rope[i][0] - self.rope[i - 1][0], self.rope[i][1] - self.rope[i - 1][1])
            abs_diff = (abs(diff[0]), abs(diff[1]))
            corr_x = 0
            corr_y = 0
            match abs_diff:
                case (2, 0):
                    if diff[0] < 0:
                        corr_x = 1
                    else:
                        corr_x = -1
                case (0, 2):
                    if diff[1] < 0:
                        corr_y = 1
                    else:
                        corr_y = -1
                case (2, 1) | (1, 2) | (2, 2):
                    if diff[0] < 0:
                        corr_x = 1
                    else:
                        corr_x = -1
                    if diff[1] < 0:
                        corr_y = 1
                    else:
                        corr_y = -1
            self.rope[i][0] += corr_x
            self.rope[i][1] += corr_y

    def execute_moves(self, moves):
        for move in moves:
            for _ in range(move[1]):
                self.move(move[0])

    def get_count(self):
        return len(self.visited)


with open("input") as f:
    moves = [(match.group(1), int(match.group(2))) for match in (re.match(r'([UDLR]) (\d+)', m) for m in f.readlines())]

grid = Grid(2)
grid.execute_moves(moves)
print('part 1: ', grid.get_count())

grid2 = Grid(10)
grid2.execute_moves(moves)
print('part 2: ', grid2.get_count())
