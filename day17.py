import itertools
from collections import deque
from dataclasses import dataclass, field
import networkx
import networkx as nx
import numpy as np
import pandas
import shapely.affinity
from networkx import DiGraph, Graph
from numpy import array
from parse import parse
from aocd import get_data
from ordered_set import OrderedSet
from scipy.sparse import csr_matrix
from shapely import LineString, Polygon, difference, Point, MultiPolygon


@dataclass(frozen=True, kw_only=True)
class OpenValve:
    Id: str
    Minute: int

@dataclass
class Valve:
    Id: str
    FlowRate: int


def next_piece(piece_index, start_x, start_y):
    if piece_index == 0:
        return LineString([Point(start_x + index, start_y) for index in range(0, 4)])
    if piece_index == 1:
        return Polygon([[p.x, p.y] for p in [
            Point(start_x + 1, start_y),
            Point(start_x, start_y + 1),
            Point(start_x + 1, start_y + 2),
            Point(start_x + 2, start_y + 1)
        ]])
    if piece_index == 2:
        return LineString([
            Point(start_x, start_y),
            Point(start_x + 1, start_y),
            Point(start_x + 2, start_y),
            Point(start_x + 2, start_y + 1),
            Point(start_x + 2, start_y + 2)
        ])
    if piece_index == 3:
        return LineString([
            Point(start_x, start_y),
            Point(start_x, start_y + 1),
            Point(start_x, start_y + 2),
            Point(start_x, start_y + 3)
        ])
    if piece_index == 4:
        return Polygon([[p.x, p.y] for p in [
            Point(start_x, start_y),
            Point(start_x + 1, start_y),
            Point(start_x + 1, start_y + 1),
            Point(start_x, start_y + 1)
        ]])


if __name__ == '__main__':
    data = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'
    #data = get_data(day=17, year=2022)

    bottom = [0, 0, 0, 0, 0, 0, 0]

    piece_generator = itertools.cycle([
        [
            [0, 0, 1, 1, 1, 1, 0]
        ],
        [
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0]
        ],
        [
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0, 0]
        ],
        [
            [1, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0]
        ],
        [
            [1, 1, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0]
        ]
    ])

    push_generator = itertools.cycle(data)

    piece_index = 0

    #y_infinity = 1_000_000_000

    polygons = Polygon()

    # bottom_line = []
    # :
    #     bottom_line.append()
    #
    # draw_line = LineString(Point(0,0))
    #     #[geometry.Point(line_infinity_bound * -1, target_y_line), geometry.Point(line_infinity_bound, target_y_line)])
    # print(f'Part 1: {part1(draw_line, scan_details)}')


    bottom_line = LineString([Point(x, 0) for x in range(0, 7)])

    polygons = polygons.union(bottom_line)

    for piece_index in range(0, 2022):
        current_piece = next_piece(piece_index % 5, 2, int(polygons.bounds[3]) + 3)
        print(current_piece)
        for push in push_generator:
            move_x = 1 if push == '>' else -1
            shifted_piece_x = shapely.affinity.translate(current_piece, move_x, 0)
            if shifted_piece_x.bounds[0] < 0 or shifted_piece_x.bounds[2] > 6:
                shifted_piece_x = current_piece
            if shifted_piece_x.intersects(polygons):
                shifted_piece_x = current_piece
            shifted_piece_y = shapely.affinity.translate(shifted_piece_x, 0, -1)
            if shifted_piece_y.intersects(polygons):
                polygons = polygons.union(shifted_piece_x)
                break
            current_piece = shifted_piece_y
        print(f'{piece_index} Height: {polygons.bounds[3]}')




    #current_piece = next_piece(piece_index, start_x, start_y)


    print(data)

    # pieces_to_run = 8


    # tetris = array([[1, 1, 1, 1, 1, 1, 1]])

    #tetris = np.insert(tetris, 0, [[0, 0, 0, 0, 0, 0, 0]],axis= 0)

    # tetris = np.concatenate(tetris, [[0, 0, 0, 0, 0, 0, 0]]) #, axis=0)

    # tetris = pandas.DataFrame(columns = ['1', '2', '3', '4', '5', '6', '7'])
    # tetris.concat(pandas.Series([1, 1, 1, 1, 1, 1, 1]))


    # tetris.insert(0, {'1': '1', '2': '1', '3': '1', '4': '1', '5': '1', '6': '1', '7': '1'})
    # tetris.insert(0, {'1': '0', '2': '0', '3': '0', '4': '0', '5': '0', '6': '0', '7': '0'})

    # for index in range(0, 7):
    #     tetris.
    #     tetris[f'Column{index}'] = "+"
    # tetris

    #result = tetris.any(axis='columns')

    # print(tetris)

    # current_height = 0
    # for piece_count, piece in enumerate(piece_generator):
    #     if piece_count == pieces_to_run:
    #         break
    #     print(piece)
    #
    #     for spaces in range(0, 3):
    #         tetris = np.insert(tetris, 0, [[0, 0, 0, 0, 0, 0, 0]], axis=0)
    #
    #     for line_index, line in enumerate(piece):
    #         tetris = np.insert(tetris, 0, [line], axis=0)
    #
    #     piece_height = len(piece)
    #     for push in push_generator:
    #
    #
    #
    #
    #     print(tetris)


    #
    #     start_y = current_height + 3
    #     for push in push_generator:
    #
    #
    #         move_x = 1 if push == '>' else -1








