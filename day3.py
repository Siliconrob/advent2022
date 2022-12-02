import types
from aocd import get_data
from dataclasses import dataclass, field
from parse import parse
from enum import Enum


class Result(Enum):
    Win = 6
    Loss = 0
    Tie = 3


@dataclass
class Score:
    Player1Points: int
    Player2Points: int


def parse_round(input: str) -> (any, any):
    player1, player2 = parse('{} {}', input)
    return player1, player2

def part1() -> any:
    return None

def part2() -> any:
    return None

if __name__ == '__main__':
    data = ['A Y', 'B X', 'C Z']
    # data = get_data(day=3, year=2022).splitlines()
    parsed_rounds = [parse_round(input_line) for input_line in data]

    print(f'Part 1: {part1()}')

    print(f'Part 2: { part2()}')