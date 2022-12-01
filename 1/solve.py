import re

def split_on_empty_lines(s):

    # greedily match 2 or more new-lines
    blank_line_regex = r"(?:\r?\n){2,}"

    return re.split(blank_line_regex, s.strip())

with open('./input', 'r') as file:
    elves = split_on_empty_lines(file.read())
    data = [x.split() for x in elves] 
    sums = [sum([int(y) for y in x]) for x in data]
    res = max(sums)
    print('part 1: ' +str(res))
    top3 = sorted(sums, reverse=True)[0:3]
    sum3 = sum(top3)
    print('part 2: ' + str(sum3))