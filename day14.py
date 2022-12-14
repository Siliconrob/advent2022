import itertools
import string
import typing
from collections import deque
from dataclasses import dataclass, field
from aocd import get_data
import networkx as nx
from parse import parse

@dataclass(frozen=True)
class Coordinate:
    X: int
    Y: int


@dataclass(kw_only=True, frozen=True)
class Bounds:
    NorthEast: Coordinate
    SouthEast: Coordinate
    NorthWest: Coordinate
    SouthWest: Coordinate



@dataclass
class Line:
    Coordinates: list[Coordinate] = field(default_factory=list)

    def filled_blocks(self) -> list[Coordinate]:
        blocks = set()
        for coord_pair in list(itertools.pairwise(self.Coordinates)):
            start = coord_pair[0]
            end = coord_pair[1]
            if start.X == end.X:  # fill vertically
                blocks.update(
                    [Coordinate(start.X, next_Y) for next_Y in range(start.Y, end.Y, -1 if start.Y > end.Y else 1)])
            else:
                blocks.update(
                    [Coordinate(next_X, start.Y) for next_X in range(start.X, end.X, -1 if start.X > end.X else 1)])
            blocks.add(end)
        return blocks


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


def parse_line_coords(line_coords: str) -> Line:
    edges = []
    for coordinate in line_coords.split('->'):
        parse_result = coordinate.split(',')
        edges.append(Coordinate(int(parse_result[0]), int(parse_result[1])))
    return Line(edges).filled_blocks()


def get_bounds(input_lines) -> Bounds:
    min_x = None
    max_x = None
    min_y = 0
    max_y = None
    for current_line in input_lines:
        current_coords_X = list(current_line)
        current_coords_X.sort(key=lambda x: x.X)
        current_coords_Y = list(current_line)
        current_coords_Y.sort(key=lambda x: x.Y)
        if min_x is None or min_x > current_coords_X[0].X:
            min_x = current_coords_X[0].X
        if max_x is None or max_x < current_coords_X[-1].X:
            max_x = current_coords_X[-1].X
        if max_y is None or max_y < current_coords_Y[-1].Y:
            max_y = current_coords_Y[-1].Y

    return Bounds(NorthEast=Coordinate(min_x, min_y),
           SouthEast=Coordinate(min_x, max_y),
           NorthWest=Coordinate(max_x, min_y),
           SouthWest=Coordinate(max_x, max_y))


if __name__ == '__main__':
    data = [
        '498, 4 -> 498, 6 -> 496, 6',
        '503, 4 -> 502, 4 -> 502, 9 -> 494, 9'
    ]

    # data = get_data(day=14, year=2022).splitlines()

    lines = [parse_line_coords(line_coords) for line_coords in data]
    bounds = get_bounds(lines)
    print(bounds)

    for line in lines:
        print(line)

    # grid, start, end = build_grid(data)
    # part1_answer = find_path(grid, start, end)
    # print(f'Part 1: {part1_answer}')
    #
    # path_lengths = []
    # for start_point in get_all_possible_start_positions(grid):
    #     distance = find_path(grid, start_point, end)
    #     if distance is not None:
    #         path_lengths.append(distance)
    # print(f'Part 2: {sorted(path_lengths)[0]}')
