import tempfile
from aocd import get_data
import os
from pathlib import Path


def get_dir_size(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total


if __name__ == '__main__':
    data = [
        '$ cd /',
        '$ ls',
        'dir a',
        '14848514 b.txt',
        '8504156 c.dat',
        'dir d',
        '$ cd a',
        '$ ls',
        'dir e',
        '29116 f',
        '2557 g',
        '62596 h.lst',
        '$ cd e',
        '$ ls',
        '584 i',
        '$ cd ..',
        '$ cd ..',
        '$ cd d',
        '$ ls',
        '4060174 j',
        '8033020 d.log',
        '5626152 d.ext',
        '7214296 k'
    ]
    data = get_data(day=7, year=2022).splitlines()

    command_start = "$"
    temp_dir_root = tempfile.TemporaryDirectory()
    current_path = temp_dir_root.name
    print(current_path)
    current_prompt_index = 2
    # skip first 2 lines always cd / and ls
    while current_prompt_index < len(data):
        prompt_history = data[current_prompt_index]
        current_prompt_index += 1
        if prompt_history.startswith(command_start):
            command_parts = prompt_history.split(" ")
            if len(command_parts) == 3:  # cd command
                target_dir = command_parts[2]
                if target_dir == "..":
                    current_path = Path(current_path).parent.absolute()
                else:
                    current_path = os.path.join(current_path, target_dir)
            else:
                continue
        else:
            entry = prompt_history.split(" ")
            new_path = os.path.join(current_path, entry[1])
            if entry[0] == "dir":
                os.mkdir(new_path)
            else:
                with open(new_path, "wb") as out:
                    out.truncate(int(entry[0]))

    limit = 100000
    paths_under_limit = {}

    for root, dirs, files in os.walk(temp_dir_root.name):
        for current_dir in dirs:
            current_path = os.path.join(root, current_dir)
            dir_size = get_dir_size(current_path)

            # paths_under_limit.
            if dir_size < limit:
                paths_under_limit[current_path] = dir_size

    print(paths_under_limit)
    part1 = sum([v for k, v in paths_under_limit.items()])
    print(f'Part 1: {part1}')

    # part2_index = read_input_stream(14, data[0])
    # print(f'Part 2: {part2_index}')
