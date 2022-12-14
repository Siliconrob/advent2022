import itertools
from collections import deque
from dataclasses import dataclass
from enum import Enum
from aocd import get_data


class Turn(Enum):
    Right: int = 1
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

    def move(self, move, grid):
        if self.Direction == 0 or self.Direction == 2:
            move_x = 1 if self.Direction == 0 else -1
            row = grid[self.y]
            first_dot = row.index('.')
            first_hash = row.index('#')
            row.reverse()
            max_length = len(row) - 1
            last_dot = max_length - row.index('.')
            last_hash = max_length - row.index('#')
            row.reverse()
            start_x = first_dot if first_dot < first_hash else first_hash
            end_x = last_dot if last_dot > last_hash else last_hash
            next_position = self.x + move_x
            if next_position > end_x:
                next_position = start_x
            if next_position < start_x:
                next_position = end_x
            next_position_char = row[next_position]
            if next_position_char == '.':
                self.x = next_position
            return
        if self.Direction == 1 or self.Direction == 3:
            move_y = 1 if self.Direction == 1 else -1
            column = []
            for key, row in grid.items():
                column.append(row[self.x])
            first_dot = column.index('.')
            first_hash = column.index('#')
            column.reverse()
            max_length = len(column) - 1
            last_dot = max_length - column.index('.')
            last_hash = max_length - column.index('#')
            column.reverse()
            start_y = first_dot if first_dot < first_hash else first_hash
            end_y = last_dot if last_dot > last_hash else last_hash
            next_position = self.y + move_y
            if next_position > end_y:
                next_position = start_y
            if next_position < start_y:
                next_position = end_y
            next_position_char = column[next_position]
            if next_position_char == '.':
                self.y = next_position
            return


def parse_input_lines(input_lines):
    grid = {}
    instructions = None
    max_line_length = 0
    for index, input_line in enumerate(input_lines):
        max_line_length = len(input_line) if max_line_length < len(input_line) else max_line_length
        if input_line == '':
            instructions = input_lines[index + 1]
            break
        else:
            if len(input_line) < max_line_length:
                repeats = max_line_length - len(input_line)
                for space in range(0, repeats):
                    input_line += ' '
            grid[index] = list(input_line)


    current_pointer = Pointer(x=grid[0].index('#') - 1, y=0)
    return grid, parse_instructions(instructions), current_pointer


def print_map(input_grid, current_pointer):
    for y_row, locations in input_grid.items():
        if current_pointer.y == y_row:
            locations[current_pointer.x] = current_pointer.pointer_character()
        the_row = "".join(locations)
        print(the_row)


def parse_instructions(instructions_input):
    instruction_queue = deque()

    current_instruction = ''
    read_line = deque(instructions_input)

    while read_line:
        current_char = read_line.popleft()
        if current_char == 'L' or current_char == 'R':
            if len(current_instruction) > 0:
                move_steps = int(current_instruction)
                instruction_queue.append(move_steps)
            instruction_queue.append(Turn.Left if current_char == 'L' else Turn.Right)
            current_instruction = ''
            continue
        current_instruction += current_char
    if len(current_instruction) > 0:
        move_steps = int(current_instruction)
        instruction_queue.append(move_steps)

    return instruction_queue


def part1(input_data):
	grid, instructions, the_pointer = parse_input_lines(input_data)
	for instruction in instructions:
		if isinstance(instruction, Turn):
			the_pointer.turn(instruction)
			continue
		grid[the_pointer.y][the_pointer.x] = '.'
		for move in range(0, instruction):
			the_pointer.move(1, grid)
		grid[the_pointer.y][the_pointer.x] = the_pointer.pointer_character()
	return compute_answer(the_pointer.x, the_pointer.y, the_pointer.Direction)


def compute_answer(x,y, direction):
	return (1000 * (y + 1)) + (4 * (x + 1)) + direction


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
	data = get_data(day=22, year=2022).splitlines()

	print(f'Part 1: {part1(data)}')