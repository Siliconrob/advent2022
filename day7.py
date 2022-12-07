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


def build_filesystem(start_path: str):
    command_start = "$"
    current_path = start_path
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


def part1(start_path: str) -> dict:
    # global paths_under_limit, root, dirs, files, current_dir, current_path, dir_size
    limit = 100000
    paths_under_limit = {}
    for root, dirs, files in os.walk(start_path):
        for current_dir in dirs:
            current_path = os.path.join(root, current_dir)
            dir_size = get_dir_size(current_path)
            # paths_under_limit.
            if dir_size < limit:
                paths_under_limit[current_path] = dir_size
    return paths_under_limit


def part2(start_path: str) -> str | None:
    all_dir_sizes = {}
    for root, dirs, files in os.walk(start_path):
        for current_dir in dirs:
            current_path = os.path.join(root, current_dir)
            dir_size = get_dir_size(current_path)
            all_dir_sizes[current_path] = dir_size
    total_dirs_size = get_dir_size(temp_dir_root.name)
    max_disk_size = 70000000
    desired_free_space = 30000000
    for current_entry in sorted(all_dir_sizes.items(), key=lambda x: x[1]):
        size_of_dir = current_entry[1]
        if total_dirs_size + desired_free_space - size_of_dir <= max_disk_size:
            return size_of_dir
    return None


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

    temp_dir_root = tempfile.TemporaryDirectory()
    build_filesystem(temp_dir_root.name)

    part1_paths = part1(temp_dir_root.name)
    part1_result = sum([v for k, v in part1_paths.items()])
    print(f'Part 1: {part1_result}')

    part2_result = part2(temp_dir_root.name)
    print(f'Part 1: {part2_result}')

    # dir_to_delete.sort()
