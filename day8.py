import tempfile
from aocd import get_data
import os
from pathlib import Path
from typing import DefaultDict, Callable, Generator

if __name__ == '__main__':
    data = [
        '30373',
        '25512',
        '65332',
        '33549',
        '35390'
    ]
    # data = get_data(day=8, year=2022).splitlines()
    rows = len(data[0])
    columns = len(data)

    exterior_trees = rows + (rows - 1) + (columns - 1) + (columns - 2)

    matrix = []
    for row in data:
        matrix.append(list(row))

    start_row_index, start_column_index = 1, 1

    visible_trees = 0

    for current_row_index in range(start_row_index, rows - 1):
        for current_column_index in range(start_column_index, columns - 1):
            # print(f'({current_row_index}, {current_column_index})')
            current_tree_height = matrix[current_row_index][current_column_index]
            current_row_look_left = matrix[current_row_index][:current_column_index]
            if all(z < current_tree_height for z in current_row_look_left):
                visible_trees += 1
                continue
            current_row_look_right = matrix[current_row_index][current_column_index + 1:]
            if all(z < current_tree_height for z in current_row_look_right):
                visible_trees += 1
                continue

            current_column_look_up = []
            for lookup_row_index_up in range(0, current_row_index):
                current_column_look_up.append(matrix[lookup_row_index_up][current_column_index])
            if all(z < current_tree_height for z in current_column_look_up):
                visible_trees += 1
                continue

            current_column_look_down = []
            for lookup_row_index_down in range(current_row_index + 1, len(matrix)):
                current_column_look_down.append(matrix[lookup_row_index_down][current_column_index])

            if all(z < current_tree_height for z in current_column_look_down):
                visible_trees += 1
                continue

    print(f'Part 1: {visible_trees + exterior_trees}')
