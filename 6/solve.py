def detect_marker(buffer, marker_size):
    last_chars = [None] * marker_size
    for i, c in enumerate(buffer):
        last_chars = last_chars[1:] + [c]

        if i > marker_size - 1 and len(set(last_chars)) == marker_size:
            return i + 1

    return -1


with open('input', 'r') as file:
    lines = file.readlines()

for l in lines:
    print(detect_marker(l.strip(), 4))
    print(detect_marker(l.strip(), 14))
