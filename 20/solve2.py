DECRYPTION_KEY = 811589153


def mix(values, rounds):
    n = len(values)
    next_ = list(range(1, n)) + [0]
    prev_ = [n - 1] + list(range(n - 1))

    for _ in range(rounds):
        for i in range(n):
            move = values[i] % (n - 1)
            if move == 0:
                continue

            prev_[next_[i]] = prev_[i]
            next_[prev_[i]] = next_[i]

            if move <= (n - 1) // 2:
                target = next_[i]
                for _ in range(move - 1):
                    target = next_[target]
                after = target
            else:
                back = (n - 1) - move
                target = prev_[i]
                for _ in range(back):
                    target = prev_[target]
                after = target

            before = after
            following = next_[before]
            next_[before] = i
            prev_[i] = before
            next_[i] = following
            prev_[following] = i

    order = []
    current = 0
    for _ in range(n):
        order.append(current)
        current = next_[current]
    return order


with open('input') as f:
    values = [int(line) * DECRYPTION_KEY for line in f]

order = mix(values, 10)
zero_pos = next(i for i, idx in enumerate(order) if values[idx] == 0)
n = len(values)
total = sum(values[order[(zero_pos + offset) % n]] for offset in (1000, 2000, 3000))
print('Part 2:', total)
