import string
import typing
from collections import deque
from dataclasses import dataclass
from aocd import get_data
from parse import parse
import networkx as nx


def build_grid(input_data: list[str]) -> list[[int]]:
    current_grid = []
    start = ()
    end = ()
    for row, input_line in enumerate(input_data):
        grid_row = []
        for column, input_char in enumerate(input_line):
            if input_char == 'S':
                grid_row.append(0)
                start = row, column
            elif input_char == 'E':
                grid_row.append(26)
                end = row, column
            else:
                grid_row.append(string.ascii_lowercase.index(input_char))
        current_grid.append(grid_row)
    return current_grid, start, end


def neighbors(row: int, column: int, min: int, max_row: int, max_column: int) -> list[(int, int)]:
    start_possible = [
        (row + 1, column),
        (row - 1, column),
        (row, column + 1),
        (row, column - 1)
    ]

    valid = []
    for (new_row, new_column) in start_possible:
        if new_row < min:
            continue
        if new_row > max_row:
            continue
        if new_column < min:
            continue
        if new_column > max_column:
            continue
        valid.append((new_row, new_column))
    return valid


def find_path(input_grid, start_point, end_point):
    current_path = deque()
    current_path.append((0, start_point[0], start_point[1]))
    visited = {(start_point[0], start_point[1])}

    while current_path:
        distance, row, column = current_path.popleft()
        for neighbor_row, neighbor_column in neighbors(row, column, 0, len(input_grid) - 1, len(input_grid[0]) - 1):
            if (neighbor_row, neighbor_column) in visited:
                continue
            if input_grid[neighbor_row][neighbor_column] - input_grid[row][column] > 1:
                continue
            if neighbor_row == end_point[0] and neighbor_column == end_point[1]:
                return distance + 1
            visited.add((neighbor_row, neighbor_column))
            current_path.append((distance + 1, neighbor_row, neighbor_column))
    return None


def get_all_possible_start_positions(input_data):
    start_positions = []

    # top row
    for current_index, check_position in enumerate(input_data[0]):
        if check_position == 0:
            start_positions.append((0, current_index))

    # bottom row
    for current_index, check_position in enumerate(input_data[-1]):
        if check_position == 0:
            start_positions.append((len(input_data) - 1, current_index))

    # left/right columns
    for row in range(1, len(input_data) - 1):
        check_position = input_data[row][0]
        if check_position == 0:
            start_positions.append((row, 0))
        check_position = input_data[row][len(input_data[0]) - 1]
        if check_position == 0:
            start_positions.append((row, len(input_data[0]) - 1))

    return start_positions


if __name__ == '__main__':
    data = [
        'Sabqponm',
        'abcryxxl',
        'accszExk',
        'acctuvwj',
        'abdefghi'
    ]
    data = get_data(day=12, year=2022).splitlines()
    grid, start, end = build_grid(data)
    part1_answer = find_path(grid, start, end)
    print(f'Part 1: {part1_answer}')

    path_lengths = []
    for start_point in get_all_possible_start_positions(grid):
        distance = find_path(grid, start_point, end)
        if distance is not None:
            path_lengths.append(distance)
    print(f'Part 2: {sorted(path_lengths)[0]}')
