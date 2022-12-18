import re


class Sensor:
    def __init__(self, sx, sy, bx, by):
        self.pos = (sx, sy)
        self.beacon = (bx, by)

    def __str__(self):
        return "Sensor at x=" + str(self.pos[0]) + ", y=" + str(self.pos[1]) + ": closest beacon is at x=" + str(
            self.beacon[0]) + ", y=" + str(self.beacon[1]) + ""

    @staticmethod
    def dist(a: tuple, b: tuple):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def radius(self):
        return Sensor.dist(self.pos, self.beacon)


def parse_line(line: str):
    pattern = r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)'
    match = re.search(pattern, line)
    if match:
        sx, sy, bx, by = map(int, match.groups())
        return Sensor(sx, sy, bx, by)
    return None


def beacon_location(sensors: list[Sensor], boundaries: tuple[int, int]):
    from ortools.sat.python import cp_model

    bound_size = abs(boundaries[1] - boundaries[0])
    model = cp_model.CpModel()
    x = model.NewIntVar(boundaries[0], boundaries[1], 'x')
    y = model.NewIntVar(boundaries[0], boundaries[1], 'y')
    for i, s in enumerate(sensors):
        xtmp = model.NewIntVar(-1 * 2 * bound_size, 2 * bound_size, "xtmp" + str(i))
        ytmp = model.NewIntVar(-1 * 2 * bound_size, 2 * bound_size, "ytmp" + str(i))
        xabs = model.NewIntVar(0, 2 * bound_size, "xabs" + str(i))
        yabs = model.NewIntVar(0, 2 * bound_size, "yabs" + str(i))
        model.Add(xtmp == s.pos[0] - x)
        model.Add(ytmp == s.pos[1] - y)
        model.AddAbsEquality(xabs, xtmp)
        model.AddAbsEquality(yabs, ytmp)
        model.Add(xabs + yabs > s.radius())

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        return solver.Value(x), solver.Value(y)
    return None


def tuning_frequency(pos: tuple[int, int]):
    return pos[0] * 4000000 + pos[1]


def find_tuning_frequency(sensors: list[Sensor], boundaries: tuple[int, int]):
    return tuning_frequency(beacon_location(sensors, boundaries))


test = ('test', (0, 20))
real = ('input', (0, 4000000))
data = real
with open(data[0], 'r') as file:
    sensors = [s for line in file.readlines() if (s := parse_line(line)) is not None]

print(find_tuning_frequency(sensors, data[1]))
