def get_priority(c: str) -> int:
    val = ord(c)
    return val - 96 if val >= 97 else val - 38


def get_sum_of_priorities(s: str) -> int:
    first = s[:len(s) // 2]
    second = s[len(s) // 2:]
    first_set = set(first)
    second_set = set(second)

    common_items = first_set.intersection(second_set)

    return sum(get_priority(c) for c in common_items)


def get_sum_of_badges():
    sum_of_badges = 0
    for i in range(0, len(rucksacks), 3):
        rucksack1 = set(rucksacks[i])
        rucksack2 = set(rucksacks[i + 1])
        rucksack3 = set(rucksacks[i + 2])

        common_items = rucksack1.intersection(rucksack2, rucksack3)

        sum_of_badges += sum(get_priority(c) for c in common_items)

    return sum_of_badges


with open('./input', 'r') as file:
    rucksacks = [s.strip() for s in file.readlines()]

rucksack_values = (get_sum_of_priorities(s) for s in rucksacks)
sum_of_priorities = sum(rucksack_values)

print(sum_of_priorities)

print(get_sum_of_badges())
