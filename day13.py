import functools
from collections import deque
from dataclasses import dataclass
from aocd import get_data


@dataclass
class InputPair:
    Left: str
    Right: str
    Index: int


def read_input_pairs(input_data):
    input_pairs = []
    current_data = deque(input_data)
    current_index = 1
    while current_data:
        input_pairs.append(InputPair(current_data.popleft(), current_data.popleft(), current_index))
        if current_data:
            current_data.popleft()
        current_index += 1
    return input_pairs


def compare_sides(left_side, right_side):
    if isinstance(left_side, int) and isinstance(right_side, int):
        return left_side - right_side
    if isinstance(left_side, int) and isinstance(right_side, list):
        return compare_sides([left_side], right_side)
    if isinstance(left_side, list) and isinstance(right_side, int):
        return compare_sides(left_side, [right_side])
    # zip stops at end of smallest list
    for left, right in zip(left_side, right_side):
        compare = compare_sides(left, right)
        if compare != 0:
            return compare
    # comparisons are all the same 0 now check that right list is smaller than left
    if len(left_side) > len(right_side):
        return 1
    if len(left_side) < len(right_side):
        return -1
    return 0


if __name__ == '__main__':
    data = [
        '[1,1,3,1,1]',
        '[1,1,5,1,1]',
        '',
        '[[1],[2,3,4]]',
        '[[1],4]',
        '',
        '[9]',
        '[[8,7,6]]',
        '',
        '[[4,4],4,4]',
        '[[4,4],4,4,4]',
        '',
        '[7,7,7,7]',
        '[7,7,7]',
        '',
        '[]',
        '[3]',
        '',
        '[[[]]]',
        '[[]]',
        '',
        '[1,[2,[3,[4,[5,6,7]]]],8,9]',
        '[1,[2,[3,[4,[5,6,0]]]],8,9]',
        # '',
        # '[[1], [2, 3, 4], 5]',
        # '[[1], 4, 4]'
    ]
    data = get_data(day=13, year=2022).splitlines()

    part1 = 0
    for input_pair in read_input_pairs(data):
        if compare_sides(eval(input_pair.Left), eval(input_pair.Right)) < 0:
            part1 += input_pair.Index
    print(f'Part 1: {part1}')

    inputs = []
    delimiter1 = [[2]]
    delimiter2 = [[6]]
    for input_line in data:
        if input_line == '':
            continue
        inputs.append(eval(input_line))
    inputs.append(delimiter1)
    inputs.append(delimiter2)
    inputs.sort(key=functools.cmp_to_key(compare_sides))  # functools generates a sortable key from a comparator
    print(f'Part 2: {(inputs.index(delimiter1) + 1) * (inputs.index(delimiter2) + 1)}')
