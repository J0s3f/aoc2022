DIGITS = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
SYMBOLS = {2: '2', 1: '1', 0: '0', -1: '-', -2: '='}


def snafu_to_int(snafu: str) -> int:
    value = 0
    for ch in snafu:
        value = value * 5 + DIGITS[ch]
    return value


def int_to_snafu(value: int) -> str:
    digits = []
    while value != 0:
        value, remainder = divmod(value, 5)
        if remainder > 2:
            remainder -= 5
            value += 1
        digits.append(SYMBOLS[remainder])
    return ''.join(reversed(digits)) or '0'


with open('input') as f:
    total = sum(snafu_to_int(line.strip()) for line in f if line.strip())

print('Part 1:', int_to_snafu(total))
