from dataclasses import dataclass, field
from functools import cache
from itertools import starmap
from collections import Counter
from aocd import get_data


@dataclass
class Blizzards:
    move_up: list = field(default_factory=lambda: [])
    move_down: list = field(default_factory=lambda: [])
    move_left: list = field(default_factory=lambda: [])
    move_right: list = field(default_factory=lambda: [])

    max_x: int = 0
    max_y: int = 0

    def add_blizzard(self, direction, x, y):
        match direction:
            case "<":
                self.move_left.append((x, y))
            case ">":
                self.move_right.append((x, y))
            case "v":
                self.move_down.append((x, y))
            case "^":
                self.move_up.append((x, y))

    def get_character(self, x, y):
        characters = ''
        if (x, y) in self.move_up:
            characters += '^'
        if (x, y) in self.move_down:
            characters += 'v'
        if (x, y) in self.move_left:
            characters += '<'
        if (x, y) in self.move_right:
            characters += '>'
        if len(characters) == 1:
            return characters
        return len(characters)


    def turn(self):
        self.move_left = list(starmap(lambda x, y: (self.max_x, y) if x - 1 < 0 else (x - 1, y), self.move_left))
        self.move_right = list(starmap(lambda x, y: (0, y) if x + 1 > self.max_x else (x + 1, y), self.move_right))
        self.move_up = list(starmap(lambda x, y: (x, self.max_y) if y - 1 < 0 else (x, y - 1), self.move_up))
        self.move_down = list(starmap(lambda x, y: (x, 0) if y + 1 > self.max_y else (x, y + 1), self.move_down))

    def blocked(self):
        return set([*self.move_left, *self.move_right, *self.move_up, *self.move_down])


def parse_input(input_data):
    current_blizzards = Blizzards()

    for y_index, row in enumerate(input_data):
        for x_index, character in enumerate(row):
            if character not in ".#":
                current_blizzards.add_blizzard(character, x_index - 1, y_index - 1)

    current_blizzards.max_x = x_index - 2
    current_blizzards.max_y = y_index - 2

    bounds = [
        (0, 0),
        (0, current_blizzards.max_y),
        (current_blizzards.max_x, current_blizzards.max_y),
        (current_blizzards.max_x, 0)
    ]

    return current_blizzards, bounds



def print_map(input_blizzards, position):
    x, y = position
    for y_index in range(-1, input_blizzards.max_y + 2):
        row = ''
        for x_index in range(-1, input_blizzards.max_x + 2):
            if x == x_index and y == y_index:
                row += '*'
            elif (x_index, y_index) in input_blizzards.blocked():
                row += input_blizzards.get_character(x_index, y_index)
            else:
                row += '.'
        print(row)

def possible_moves(input_blizzards, current_position, destination):
    current_x, current_y = current_position
    destination_x, destination_y = destination
    possible_moves = set()
    possibilities = [
        (current_x - 1, current_y),
        (current_x + 1, current_y),
        (current_x, current_y + 1),
        (current_x, current_y - 1)
    ]
    for possibility in possibilities:
        if possibility in input_blizzards.blocked():
            continue
        pos_x, pos_y = possibility
        if pos_x < 0 or pos_x > input_blizzards.max_x:
            continue
        if pos_y < 0 or pos_y > input_blizzards.max_y:
            continue
        possible_moves.add(possibility)

    if len(possible_moves) == 0:
        possible_moves.add(current_position)

    if destination_y > -1:
        if current_x == destination_x and current_y + 1 == destination_y:
            possible_moves.add((current_x, current_y + 1))
    else:
        if current_x == destination_x and current_y - 1 == destination_y:
            possible_moves.add((current_x, current_y - 1))

    return possible_moves


def search(input_blizzards, start, end):
    time = 0
    locations = set([start])

    while end not in locations:
        time += 1
        input_blizzards.turn()
        new_positions = set()
        for current_location in locations:
            new_positions.update(possible_moves(input_blizzards, current_location, end))
        locations = new_positions
    return time, input_blizzards


if __name__ == '__main__':
    # data = [
    #     '#.#####',
    #     '#.....#',
    #     '#>....#',
    #     '#.....#',
    #     '#...v.#',
    #     '#.....#',
    #     '#####.#'
    # ]

    data = [
        '#.######',
        '#>>.<^<#',
        '#.<..<<#',
        '#>v.><>#',
        '#<^v^^>#',
        '######.#'
    ]

    data = get_data(day=24, year=2022).splitlines()
    blizzards, bounds = parse_input(data)
    print(bounds)

    end_points = {}
    start = (0, -1)
    end = (blizzards.max_x, blizzards.max_y + 1)
    print_map(blizzards, start)

    total_steps = 0

    total_steps, blizzards = search(blizzards, start, end)
    print(f'Part 1: {total_steps}')

    steps, blizzards = search(blizzards, end, start)
    print(f'Steps {steps}')
    total_steps += steps

    steps, blizzards = search(blizzards, start, end)
    total_steps += steps
    print(f'Steps {steps}')
    print(f'Part 2: {total_steps}')

