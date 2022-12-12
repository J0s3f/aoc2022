def get_allowed(heightmap, last_node):
    i = last_node[0]
    j = last_node[1]
    allowed = []
    for ni, nj in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
        if (0 <= ni < len(heightmap) and
                0 <= nj < len(heightmap[i]) and
                ord(heightmap[ni][nj]) - ord(heightmap[i][j]) <= 1):
            allowed.append((ni, nj))
    return allowed


def shortest_path(heightmap, start_pos, end_pos):
    path_list = [[start_pos]]
    path_index = 0
    previous_nodes = {start_pos}

    while path_index < len(path_list):
        current_path = path_list[path_index]
        last_node = current_path[-1]
        next_nodes = get_allowed(heightmap, last_node)
        if end_pos in next_nodes:
            current_path.append(end_pos)
            return current_path
        for next_node in next_nodes:
            if next_node not in previous_nodes:
                new_path = current_path[:]
                new_path.append(next_node)
                path_list.append(new_path)
                previous_nodes.add(next_node)
        path_index += 1
    return []


with open("input") as f:
    heightmap = f.readlines()

heightmap = [x.strip() for x in heightmap]

start_pos = None
end_pos = None
for i in range(len(heightmap)):
    for j in range(len(heightmap[i])):
        if heightmap[i][j] == 'S':
            start_pos = (i, j)
            heightmap[i] = heightmap[i].replace("S", "a")
        if heightmap[i][j] == 'E':
            end_pos = (i, j)
            heightmap[i] = heightmap[i].replace("E", "z")

shortest_path = shortest_path(heightmap, start_pos, end_pos)

print(len(shortest_path)-1)
