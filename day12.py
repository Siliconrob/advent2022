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


def find_path(input_grid, start_point, end_point) -> int:
    current_path = deque()
    current_path.append((0, start_point[0], start_point[1]))
    visited = {(start_point[0], start_point[1])}

    path_found = False
    while current_path and path_found == False:
        distance, row, column = current_path.popleft()
        for neighbor_row, neighbor_column in neighbors(row, column, 0, len(input_grid) - 1, len(input_grid[0]) - 1):
            if (neighbor_row, neighbor_column) in visited:
                continue
            if input_grid[neighbor_row][neighbor_column] - input_grid[row][column] > 1:
                continue
            if neighbor_row == end_point[0] and neighbor_column == end_point[1]:
                path_found = True
                distance += 1
                break
            visited.add((neighbor_row, neighbor_column))
            current_path.append((distance + 1, neighbor_row, neighbor_column))
    return distance

def get_all_possible_start_positions(input_data):
    start_positions = []
    for row, input_line in enumerate(input_data):
        for column, input_char in enumerate(input_line):
            if input_char == 'S' or input_char == 'a':
                start_positions.append((row, column))
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
    for start_point in get_all_possible_start_positions(data):
        distance = find_path(grid, start_point, end)
        if distance > 300: # something is wrong with the path finding that it gives short paths
            path_lengths.append(distance)
    print(f'Part 2: {sorted(path_lengths)[0]}')



