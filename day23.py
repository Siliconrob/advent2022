from collections import Counter, deque
from aocd import get_data


def parse_input(input_data):
    elves = set()
    for y_index, row in enumerate(input_data):
        for x_index, position_value in enumerate(row):
            if position_value == '#':
                elves.add((x_index, y_index))
    return elves


def all_positions(x, y):
    return set([
        (x - 1, y - 1),  # NW
        (x - 1, y),  # W
        (x - 1, y + 1),  # SW
        (x, y - 1),  # N
        (x, y + 1),  # S
        (x + 1, y - 1),  # NE
        (x + 1, y),  # E
        (x + 1, y + 1),  # SE
    ])


def check_north(x, y, input_elfs):
    north_positions = set([(x - 1, y - 1), (x, y - 1), (x + 1, y - 1)])
    return (x, y - 1) if north_positions.isdisjoint(input_elfs) else (None, None)


def check_south(x, y, input_elfs):
    south_positions = set([(x - 1, y + 1), (x, y + 1), (x + 1, y + 1)])
    return (x, y + 1) if south_positions.isdisjoint(input_elfs) else (None, None)


def check_west(x, y, input_elfs):
    west_positions = set([(x - 1, y - 1), (x - 1, y), (x - 1, y + 1)])
    return (x - 1, y) if west_positions.isdisjoint(input_elfs) else (None, None)


def check_east(x, y, input_elfs):
    east_positions = set([(x + 1, y - 1), (x + 1, y), (x + 1, y + 1)])
    return (x + 1, y) if east_positions.isdisjoint(input_elfs) else (None, None)


def move(input_elf_frame, round, move_check_fns):
    proposed_elf_frame = []

    for _, position in enumerate(input_elf_frame):
        x, y = position
        all = all_positions(x, y)
        if all.isdisjoint(input_elf_frame):
            proposed_elf_frame.append(position)
            continue
        new_x, new_y = move_check_fns[0](x, y, input_elf_frame)
        if new_x is not None and new_y is not None:
            proposed_elf_frame.append((new_x, new_y))
            continue
        new_x, new_y = move_check_fns[1](x, y, input_elf_frame)
        if new_x is not None and new_y is not None:
            proposed_elf_frame.append((new_x, new_y))
            continue
        new_x, new_y = move_check_fns[2](x, y, input_elf_frame)
        if new_x is not None and new_y is not None:
            proposed_elf_frame.append((new_x, new_y))
            continue
        new_x, new_y = move_check_fns[3](x, y, input_elf_frame)
        if new_x is not None and new_y is not None:
            proposed_elf_frame.append((new_x, new_y))
            continue
        else:
            proposed_elf_frame.append(position)

    next_elf_frame = set()
    next_counts = Counter(proposed_elf_frame)

    for old, new in zip(input_elf_frame, proposed_elf_frame):
        if old == new:
            next_elf_frame.add(old)
        elif next_counts[new] > 1:
            next_elf_frame.add(old)
        else:
            next_elf_frame.add(new)

    stop = True if next_elf_frame.intersection(input_elf_frame) == input_elf_frame else False

    return next_elf_frame, stop


def part1(elves):
    move_fns = deque((check_north, check_south, check_west, check_east))
    # show_map(elves)
    for round in range(0, 10):
        elves, stop = move(elves, round, move_fns)
        move_fns.rotate(-1)
        empties = show_map(elves)
    return empties


def part2(elves):
    move_fns = deque((check_north, check_south, check_west, check_east))
    # show_map(elves)
    round = 0
    while True:
        elves, stop = move(elves, round, move_fns)
        if stop:
            break
        round += 1
        move_fns.rotate(-1)
    # empties = show_map(elves)
    return round + 1


def show_map(input_elves):
    empties = 0

    x_list = [x for x, y in input_elves]
    y_list = [y for x, y in input_elves]

    for y_index in range(min(y_list), max(y_list) + 1):
        row = ''
        for x_index in range(min(x_list), max(x_list) + 1):
            if (x_index, y_index) in input_elves:
                row += '#'
            else:
                row += '.'
                empties += 1
        print(row)
    print(f'Empties {empties}\n')
    return empties


if __name__ == '__main__':
    # data = [
    # 	'.....',
    # 	'..##.',
    # 	'..#..',
    # 	'.....',
    # 	'..##.',
    # 	'.....'
    # ]

    data = [
        '....#..',
        '..###.#',
        '#...#.#',
        '.#...##',
        '#.###..',
        '##.#.##',
        '.#..#..'
    ]

    data = get_data(day=23, year=2022).splitlines()
    elves = parse_input(data)

    part1_answer = part1(elves)
    print(f'Part 1: {part1_answer}')

    part2_answer = part2(elves)
    print(f'Part 2: {part2_answer}')
