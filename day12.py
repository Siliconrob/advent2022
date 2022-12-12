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
    current_path = deque()
    current_path.append((0, start[0], start[1]))
    visited = {(start[0], start[1])}

    part1_complete = False
    while current_path and part1_complete == False:
        distance, row, column = current_path.popleft()
        for neighbor_row, neighbor_column in neighbors(row, column, 0, len(grid) - 1, len(grid[0]) - 1):
            if (neighbor_row, neighbor_column) in visited:
                continue
            if grid[neighbor_row][neighbor_column] - grid[row][column] > 1:
                continue
            if neighbor_row == end[0] and neighbor_column == end[1]:
                part1_complete = True
                distance += 1
                break
            visited.add((neighbor_row, neighbor_column))
            current_path.append((distance + 1, neighbor_row, neighbor_column))
    print(f'Part 1: {distance}')
