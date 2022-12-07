import re
from itertools import chain


class FsNode:
    def __init__(self, parent, name, is_dir, size=0):
        self.name = name
        self.parent = parent
        self.children = {}
        self.is_dir = is_dir
        self.size = int(size) if not is_dir else 0
        if not is_dir and int(size) < 1:
            raise (Exception("Files need a size"))

    def __iter__(self):
        for v in chain(*map(iter, self.children.values())):
            yield v
        yield self

    def get_child(self, name):
        if name in self.children:
            return self.children[name]
        return None

    def add_child(self, name, is_dir, size=0):
        if not self.is_dir:
            raise (Exception("Files have no children"))
        self.children[name] = FsNode(self, name, is_dir, size)

    def get_size(self):
        if not self.is_dir:
            return self.size
        else:
            return sum(f.get_size() for f in self.children.values())

    def __repr__(self):
        if self.is_dir:
            return f"<Directory {self.name}>"
        else:
            return f"<File {self.name}, size {self.size}>"


root = FsNode(None, "/", True)
current_node = None

command_pattern = r"^\$ (\S+)(?: (\S+)|)"

file_pattern = r"([0-9]+|dir) (\S+)"

with open('input', 'r') as file:
    lines = file.readlines()

for l in lines:
    command = re.match(command_pattern, l)
    if command:
        dir = command.group(2)
        command = command.group(1)
        match command:
            case 'cd':
                if dir == '/':
                    current_node = root
                elif dir == '..':
                    current_node = current_node.parent
                else:
                    existing = current_node.get_child(dir)
                    if existing:
                        current_node = existing
                    else:
                        raise (Exception("cannot cd to missing dir"))
    else:
        file = re.match(file_pattern, l)
        if file:
            filesize = file.group(1)
            filename = file.group(2)
            current_node.add_child(filename, filesize == 'dir', filesize)

folders = filter(lambda f: f.is_dir, iter(root))
folders_with_max_size = [f for f in folders if f.get_size() <= 100000]
total_size = sum([f.get_size() for f in folders_with_max_size])
print('part1: ', total_size)
total = 70000000
need = 30000000
free = total - root.get_size()
to_delete = need-free
candidates = [f for f in filter(
    lambda f: f.is_dir, iter(root)) if f.get_size() >= to_delete]
delete = sorted(candidates, key=FsNode.get_size)
print('part2: ', delete[0].get_size())
