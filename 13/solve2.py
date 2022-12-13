import ast
from functools import cmp_to_key


def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return -1
        if right < left:
            return 1
        return 0
    if isinstance(left, list) and isinstance(right, list):
        for i in range(min(len(left), len(right))):
            ordered = compare(left[i], right[i])
            if ordered != 0:
                return ordered
        if len(left) > len(right):
            return 1
        if len(left) < len(right):
            return -1
    if isinstance(left, list) and isinstance(right, int):
        return compare(left, [right])
    if isinstance(left, int) and isinstance(right, list):
        return compare([left], right)
    return 0


with open("input") as f:
    packages = [ast.literal_eval(ln.strip()) for ln in f.readlines() if ln.strip() != ""]

packages.append([[2]])
packages.append([[6]])

sorted = sorted(packages, key=cmp_to_key(compare))

result = (1 + sorted.index([[2]])) * (1 + sorted.index([[6]]))

print(result)
