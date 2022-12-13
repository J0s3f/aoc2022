import ast
import re


def is_ordered(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return True
        if right < left:
            return False
        return None
    if isinstance(left, list) and isinstance(right, list):
        for i in range(min(len(left), len(right))):
            ordered = is_ordered(left[i], right[i])
            if ordered is not None:
                return ordered
        if len(left) > len(right):
            return False
        if len(left) < len(right):
            return True
    if isinstance(left, list) and isinstance(right, int):
        return is_ordered(left, [right])
    if isinstance(left, int) and isinstance(right, list):
        return is_ordered([left], right)


with open("input") as f:
    packages = [(ast.literal_eval(p[0]), ast.literal_eval(p[1])) for p in (re.split(r"\r?\n", ln) for ln in
                                                                           re.split(r"\r?\n\r?\n", f.read().strip()))]

with_index = [(p[0], p[1], i + 1) for i, p in enumerate(packages)]
ordered = [p for p in with_index if is_ordered(p[0], p[1])]

sum_ordered = sum([p[2] for p in ordered])

print(sum_ordered)
