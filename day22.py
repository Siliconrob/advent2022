from dataclasses import dataclass
from enum import Enum
from aocd import get_data
from parse import parse
import sympy

class Turn(Enum):
    Right: int =  1
    Left: int = -1

@dataclass
class Pointer:
    x: int
    y: int
    Direction: int = 0

    def turn(self, turn_direction: Turn):
        self.Direction = abs((self.Direction + turn_direction.value) % 4)

    def pointer_character(self):
        match self.Direction:
            case 0:
                return ">"
            case 1:
                return "V"
            case 2:
                return "<"
            case 3:
                return "^"


def parse_input_lines(input_lines):
    grid = {}
    instructions = None
    for index, input_line in enumerate(input_lines):
        if input_line == '':
            instructions = input_lines[index + 1]
            break
        else:
            grid[index] = list(input_line)

    current_pointer = Pointer(x=grid[0].index('#') - 1, y=0)
    return grid, instructions, current_pointer


def print_map(input_grid, current_pointer):
    for y_row, locations in input_grid.items():
        if current_pointer.y == y_row:
            locations[current_pointer.x] = current_pointer.pointer_character()
        the_row = "".join(locations)
        print(the_row)






if __name__ == '__main__':
    data = [
        '        ...#',
        '        .#..',
        '        #...',
        '        ....',
        '...#.......#',
        '........#...',
        '..#....#....',
        '..........#.',
        '        ...#....',
        '        .....#..',
        '        .#......',
        '        ......#.',
        '',
        '10R5L5R10L4R5L5'
    ]
    # data = get_data(day=22, year=2022).splitlines()
    grid, instructions, the_pointer = parse_input_lines(data)

    # print(the_pointer.pointer_character())
    # the_pointer.turn(Turn.Right)
    #print(instructions)
