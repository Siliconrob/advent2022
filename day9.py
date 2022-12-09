from dataclasses import dataclass
from enum import Enum

from aocd import get_data
from parse import parse


class Move(Enum):
    Left: str = 'L'
    Right: str = 'R'
    Up: str = 'U'
    Down: str = 'D'

@dataclass
class Position:
    X: int
    Y: int


def move_head(start: Position, direction: Move) -> Position:
    match direction:
        case Move.Left:
            start.X -= 1
        case Move.Right:
            start.X += 1
        case Move.Up:
            start.Y += 1
        case Move.Down:
            start.Y -= 1
    return Position(start.X, start.Y)


def expand_moves(input_data: list[str]):
    all_moves = []
    for moves in input_data:
        compact_move = parse('{} {:d}', moves).fixed
        all_moves.extend([compact_move[0] for index in range(0, compact_move[1])])
    return all_moves


def move_tail(head: Position, tail: Position) -> Position:
    # print(head)
    if tail.X == head.X and tail.Y == head.Y:
        return Position(tail.X, tail.Y)

    if tail.X + 1 == head.X or tail.X - 1 == head.X:
        if tail.Y == head.Y or tail.Y + 1 == head.Y or tail.Y - 1 == head.Y:
            return Position(tail.X, tail.Y)

    if tail.Y + 1 == head.Y or tail.Y - 1 == head.Y:
        if tail.X == head.X or tail.X + 1 == head.X or tail.X - 1 == head.X:
            return Position(tail.X, tail.Y)

    if tail.X == head.X:
        if tail.Y < head.Y and head.Y - tail.Y == 2: # up
            return Position(tail.X, tail.Y + 1)
        if tail.Y > head.Y and tail.Y - head.Y == 2: # down
            return Position(tail.X, tail.Y - 1)
    if tail.Y == head.Y:
        if tail.X < head.X and head.X - tail.X == 2: # right
            return Position(tail.X + 1, tail.Y)
        if tail.X > head.X and tail.X - head.X == 2: # left
            return Position(tail.X - 1, tail.Y)

    if (tail.X + 1 == head.X or tail.X - 1 == head.X) and (tail.Y + 1 == head.Y or tail.Y - 1 == head.Y):
        return Position(tail.X, tail.Y)

    if tail.X < head.X: # move east
        if tail.Y < head.Y: # move north
            return Position(tail.X + 1, tail.Y + 1)
        if tail.Y > head.Y: # move south
            return Position(tail.X + 1, tail.Y - 1)
    if tail.X > head.X: # move west
        if tail.Y < head.Y: # move north
            return Position(tail.X - 1, tail.Y + 1)
        if tail.Y > head.Y: # move south
            return Position(tail.X - 1, tail.Y - 1)


def part1(input_moves: list[str]):
    head = Position(0, 0)
    tail = Position(0, 0)
    head_visits = [head]
    tail_visits = [f'{tail.X},{tail.Y}']
    for move in expand_moves(input_moves):
        head = move_head(head, Move(move))
        head_visits.append(head)
        tail = move_tail(head, tail)
        tail_visits.append(f'{tail.X},{tail.Y}')
    return len(set(tail_visits))

def part2(input_moves: list[str]):
    return 0


if __name__ == '__main__':
    # data = [
    #     'R 4',
    #     'U 4',
    #     'L 3',
    #     'D 1',
    #     'R 4',
    #     'D 1',
    #     'L 5',
    #     'R 2'
    # ]

    data = [
        'R 5',
        'U 8',
        'L 8',
        'D 3',
        'R 17',
        'D 10',
        'L 25',
        'U 20'
    ]

    data = get_data(day=9, year=2022).splitlines()
    print(f'Part 1: {part1(data)}')
    print(f'Part 2: {part2(data)}')
