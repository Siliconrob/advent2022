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
    data = get_data(day=4, year=2022).splitlines()
    # data = ['2-4,6-8',
    #         '2-3,4-5',
    #         '5-7,7-9',
    #         '2-8,3-7',
    #         '6-6,4-6',
    #         '2-6,4-8']

    part1_matches = 0
    part2_matches = 0
    for input_line in data:
        assignment = parse_line(input_line)
        matches = assignment.common_elements()
        if assignment.is_match(assignment.Elf1) or assignment.is_match(assignment.Elf2):
            part1_matches += 1
        elif len(matches) > 0:
            part2_matches += 1
    print(f'Part 1: {part1_matches}')
    print(f'Part 2: {part1_matches + part2_matches}')
