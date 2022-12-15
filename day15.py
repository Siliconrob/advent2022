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


def build_grid(blocks: set(), sand: set, start: Coordinate, bounds, buffer=1):
    grid = []
    for y in range(-buffer, ((bounds.SouthEast.Y - bounds.NorthEast.Y) + 1) + buffer):
        grid_row = []
        for x in range(-buffer, ((bounds.NorthWest.X - bounds.NorthEast.X) + 1) + buffer):
            test_coord = Coordinate(x + bounds.NorthEast.X, y + bounds.NorthEast.Y)
            if test_coord in blocks:
                if test_coord.X == start.X and test_coord.Y == start.Y:
                    grid_row.append("+")
                else:
                    grid_row.append("#")
            elif test_coord in sand:
                grid_row.append("O")
            else:
                grid_row.append(".")
        grid.append(grid_row)
    return grid


def move_sand(position: Coordinate, current_blocks: set, current_sand: set):
    filled = current_blocks.union(current_sand)
    down = Coordinate(position.X, position.Y + 1)
    if down not in filled:
        return down
    left = Coordinate(position.X - 1, position.Y + 1)
    if left not in filled:
        return left
    right = Coordinate(position.X + 1, position.Y + 1)
    if right not in filled:
        return right
    return None


def print_grid(input_grid):
    for grid_row in input_grid:
        print("".join(grid_row))


def part1(input_lines):
    bounds = get_bounds(input_lines)
    start = Coordinate(500, 0)
    print(bounds)
    blocks = set()
    blocks.add(Coordinate(500, 0))
    for line in lines:
        blocks = blocks.union(list(line))
    filled_sand = set()
    current_position = start
    while current_position.Y < bounds.SouthEast.Y:
        new_position = move_sand(current_position, blocks, filled_sand)
        if new_position is None:
            filled_sand.add(current_position)
            current_position = start
        else:
            current_position = new_position
    print_grid(build_grid(blocks, filled_sand, start, bounds))
    return len(filled_sand)


def can_add_sand(start: Coordinate, current_sand: set):
    top_full = set([
        Coordinate(start.X - 1, start.Y + 1),
        Coordinate(start.X, start.Y + 1),
        Coordinate(start.X + 1, start.Y + 1),
    ])
    return top_full != current_sand & top_full


def part2(input_lines):
    bounds = get_bounds(input_lines)
    bottom_line = Line([Coordinate(bounds.SouthEast.X - 1000, bounds.SouthEast.Y + 2),
                        Coordinate(bounds.SouthWest.X + 1000, bounds.SouthWest.Y + 2)]).filled_blocks()
    input_lines.append(bottom_line)
    bounds = get_bounds(input_lines)
    start = Coordinate(500, 0)
    print(bounds)
    blocks = set()
    blocks.add(Coordinate(500, 0))
    for line in input_lines:
        blocks = blocks.union(list(line))
    filled_sand = set()
    current_position = start
    while can_add_sand(start, filled_sand):
        new_position = move_sand(current_position, blocks, filled_sand)
        if new_position is None:
            filled_sand.add(current_position)
            current_position = start
        else:
            current_position = new_position
    filled_sand.add(start)
    print_grid(build_grid(blocks, filled_sand, start, bounds))
    return len(filled_sand)


if __name__ == '__main__':
    data = [
        'Sensor at x=2, y=18: closest beacon is at x=-2, y=15',
        'Sensor at x=9, y=16: closest beacon is at x=10, y=16',
        'Sensor at x=13, y=2: closest beacon is at x=15, y=3',
        'Sensor at x=12, y=14: closest beacon is at x=10, y=16',
        'Sensor at x=10, y=20: closest beacon is at x=10, y=16',
        'Sensor at x=14, y=17: closest beacon is at x=10, y=16',
        'Sensor at x=8, y=7: closest beacon is at x=2, y=10',
        'Sensor at x=2, y=0: closest beacon is at x=2, y=10',
        'Sensor at x=0, y=11: closest beacon is at x=2, y=10',
        'Sensor at x=20, y=14: closest beacon is at x=25, y=17',
        'Sensor at x=17, y=20: closest beacon is at x=21, y=22',
        'Sensor at x=16, y=7: closest beacon is at x=15, y=3',
        'Sensor at x=14, y=3: closest beacon is at x=15, y=3',
        'Sensor at x=20, y=1: closest beacon is at x=15, y=3'
    ]


    # data = get_data(day=15, year=2022).splitlines()
    for line in data:
        print(line)


    # lines = [parse_line_coords(line_coords) for line_coords in data]
    # print(f'Part 1: {part1(lines)}')
    # print(f'Part 2: {part2(lines)}')
