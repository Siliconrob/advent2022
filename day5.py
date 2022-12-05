import re
from copy import deepcopy
from aocd import get_data
from parse import parse


def build_initial_state():
    position_lookup = {}
    stacks = {}
    for stack_number in stacks_to_make:
        position_lookup[stack_number] = positions.index(str(stack_number))
        stacks[stack_number] = []
    initial_state.reverse()
    for initial_state_row in initial_state:
        for key, value in position_lookup.items():
            stack = [] if stacks.get(key) is None else stacks.get(key)
            if initial_state_row[value] != ' ':
                stack.append(initial_state_row[value])
    return stacks


def part1(input_stacks, commands):
    for command_input in commands:
        parsed_command = parse_command(command_input)
        for crates in range(1, parsed_command[0] + 1):
            source, target = input_stacks[parsed_command[1]], input_stacks[parsed_command[2]]
            target.append(source.pop())
    return read_final_state(input_stacks)


def part2(input_stacks, commands):
    for command_input in commands:
        parsed_command = parse_command(command_input)
        source, target = input_stacks[parsed_command[1]], input_stacks[parsed_command[2]]
        to_move = []
        for crates in range(1, parsed_command[0] + 1):
            to_move.append(source.pop())
        to_move.reverse()
        target.extend(to_move)
    return read_final_state(input_stacks)


def read_final_state(ending_stacks):
    return ''.join([completed_stack.pop() for completed_stack in ending_stacks.values()])


def parse_command(command_input):
    return parse('move {:d} from {:d} to {:d}', command_input).fixed


if __name__ == '__main__':
    data = [
        '    [D]    ',
        '[N] [C]    ',
        '[Z] [M] [P]',
        ' 1   2   3 ',
        '',
        'move 1 from 2 to 1',
        'move 3 from 1 to 3',
        'move 2 from 2 to 1',
        'move 1 from 1 to 2',
    ]

    data = get_data(day=5, year=2022).splitlines()

    splitter_index = data.index('')
    initial_state = data[:splitter_index - 1]
    positions = data[splitter_index - 1]
    stack_numbers = [int(i) for i in re.findall("\d+", positions)]
    stacks_to_make = range(1, max(stack_numbers) + 1)

    commands = data[splitter_index + 1:]
    stack_start = build_initial_state()

    part1_stack_start = deepcopy(stack_start)
    print(f'Part 1: {part1(part1_stack_start, commands)}')

    part2_stack_start = deepcopy(stack_start)
    print(f'Part 2: {part2(part2_stack_start, commands)}')
