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


def pos_without_beacon(sensors: list[Sensor], y: int):
    pos_without_sensor = set()
    for s in sensors:
        pos = (s.pos[0], y)
        while Sensor.dist(s.pos, pos) <= s.radius():
            pos_without_sensor.add(pos)
            pos = (pos[0] - 1, y)
        pos = (s.pos[0], y)
        while Sensor.dist(s.pos, pos) < s.radius():
            pos_without_sensor.add(pos)
            pos = (pos[0] + 1, y)
    for s in filter(lambda s: s.pos[1] == y, sensors):
        pos_without_sensor.remove(s.pos)
    return pos_without_sensor


test = ('test', 10)
real = ('input', 2000000)
data = real
with open(data[0], 'r') as file:
    sensors = [s for line in file.readlines() if (s := parse_line(line)) is not None]

print(len(pos_without_beacon(sensors, data[1])))
