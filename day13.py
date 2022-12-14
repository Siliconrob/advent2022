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
    if isinstance(left_side, int) and isinstance(right_side, list):
        return compare_sides([left_side], right_side)
    if isinstance(left_side, list) and isinstance(right_side, int):
        return compare_sides(left_side, [right_side])
    compares = 0
    if isinstance(left_side, list) and isinstance(right_side, list):
        for index, left in enumerate(left_side):
            right = get_value(right_side, index)
            if isinstance(left, int) and isinstance(right, int):
                if right is None:
                    return 1
                if left > right:
                    return -1
                compares += 1
            else:
                if isinstance(left, int) and isinstance(right, list):
                    return compare_sides([left], right)
                if isinstance(left, list) and isinstance(right, int):
                    return compare_sides(left, [right])
                if isinstance(left, list) and isinstance(right, list):
                    return compare_sides(left, right)
        if compares == 0 and len(right_side) > len(left_side):
            return 1
        if compares == 0 and len(left_side) > len(right_side):
            return -1
    return compares


def get_value(input_list, index):
  try:
    return input_list[index]
  except IndexError:
    return None


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
        '[1,[2,[3,[4,[5,6,0]]]],8,9]'
    ]
    data = get_data(day=13, year=2022).splitlines()

    sum = 0
    for input_pair in read_input_pairs(data):
        left_result = eval(input_pair.Left)
        right_result = eval(input_pair.Right)

        result = compare_sides(left_result, right_result)
        if result >= 1:
            sum += input_pair.Index
    print(f'Part 1: {sum}')




