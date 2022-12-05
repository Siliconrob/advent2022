import re
from copy import deepcopy
from aocd import get_data
from parse import parse

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


    commands = data[splitter_index + 1:]
    part1_stack_start = deepcopy(stacks)
    part2_stack_start = deepcopy(stacks)

    for command_input in commands:
        parsed_command = parse('move {:d} from {:d} to {:d}', command_input).fixed
        for crates in range(1, parsed_command[0] + 1):
            source_stack = part1_stack_start[parsed_command[1]]
            target_stack = part1_stack_start[parsed_command[2]]
            target_stack.append(source_stack.pop())

    completed = ''.join([completed_stack.pop() for completed_stack in part1_stack_start.values()])
    print(f'Part 1: {completed}')

    for command_input in commands:
        parsed_command = parse('move {:d} from {:d} to {:d}', command_input).fixed
        source_stack = part2_stack_start[parsed_command[1]]
        target_stack = part2_stack_start[parsed_command[2]]
        to_move = []
        for crates in range(1, parsed_command[0] + 1):
            to_move.append(source_stack.pop())
        to_move.reverse()
        target_stack.extend(to_move)

    completed = ''.join([completed_stack.pop() for completed_stack in part2_stack_start.values()])
    print(f'Part 2: {completed}')
