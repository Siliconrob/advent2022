import re
import string
from dataclasses import dataclass
from aocd import get_data
from parse import parse

@dataclass
class ElfAssignments:
    Elf1: set
    Elf2: set

    def common_elements(self) -> set:
        return self.Elf1 & self.Elf2

    def is_match(self, set_to_match: set) -> bool:
        return self.common_elements() & set_to_match == set_to_match


def parse_line(elf_pair_input: str) -> ElfAssignments:
    parse_result = parse('{:d}-{:d},{:d}-{:d}', elf_pair_input).fixed
    elf1_assignment = set(list(range(parse_result[0], parse_result[1] + 1)))
    elf2_assignment = set(list(range(parse_result[2], parse_result[3] + 1)))
    return ElfAssignments(elf1_assignment, elf2_assignment)


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

    # data = get_data(day=5, year=2022).splitlines()

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
    for command_input in commands:
        parsed_command = parse('move {:d} from {:d} to {:d}', command_input).fixed
        # print(parsed_command)
        for crates in range(1, parsed_command[0] + 1):
            source_stack = stacks[parsed_command[1]]
            target_stack = stacks[parsed_command[2]]
            target_stack.append(source_stack.pop())

    print(stacks)
    completed = ''.join([completed_stack.pop() for completed_stack in stacks.values()])
    print(f'Part 1: {completed}')
