from dataclasses import dataclass, field
from itertools import starmap
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

    def turn(self):
        self.move_left = list(starmap(lambda x, y: (self.max_x, y) if x - 1 < 0 else (x - 1, y), self.move_left))
        self.move_right = list(starmap(lambda x, y: (0, y) if x + 1 > self.max_x else (x + 1, y), self.move_right))
        self.move_up = list(starmap(lambda x, y: (x, self.max_y) if y - 1 < 0 else (x, y - 1), self.move_up))
        self.move_down = list(starmap(lambda x, y: (x, 0) if y + 1 > self.max_y else (x, y + 1), self.move_down))

    def blocked(self):
        return set([*self.move_left, *self.move_right, *self.move_up, *self.move_down])


def parse_input(input_data):
    bounds = []
    current_blizzards = Blizzards()

    for y_index, row in enumerate(input_data):
        for x_index, character in enumerate(row):
            if character not in ".#":
                current_blizzards.add_blizzard(character, x_index - 1, y_index - 1)

    current_blizzards.max_x = x_index - 2
    current_blizzards.max_y = y_index - 2

    print(current_blizzards.blocked())
    current_blizzards.turn()
    current_blizzards.turn()
    current_blizzards.turn()
    print(current_blizzards.blocked())
    current_blizzards.turn()
    print(current_blizzards.blocked())


if __name__ == '__main__':
    data = [
        '#.#####',
        '#.....#',
        '#>....#',
        '#.....#',
        '#...v.#',
        '#.....#',
        '#####.#'
    ]

    # data = get_data(day=24, year=2022).splitlines()
    map = parse_input(data)

# part1_answer = part1(elves)
# print(f'Part 1: {part1_answer}')
#
# part2_answer = part2(elves)
# print(f'Part 2: {part2_answer}')
