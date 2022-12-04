from dataclasses import dataclass
from aocd import get_data
from parse import parse


@dataclass
class ElfAssignments:
    Elf1: set
    Elf2: set


def parse_line(elf_pair_input: str) -> ElfAssignments:
    elf1_range_start, elf1_range_end, elf2_range_start, elf2_range_end = parse('{:d}-{:d},{:d}-{:d}', elf_pair_input)
    elf1_assignment = set(list(range(elf1_range_start, elf1_range_end + 1)))
    elf2_assignment = set(list(range(elf2_range_start, elf2_range_end + 1)))
    return ElfAssignments(elf1_assignment, elf2_assignment)


if __name__ == '__main__':
    # data = get_data(day=5, year=2022).splitlines()
    data = ['2-4,6-8',
            '2-3,4-5',
            '5-7,7-9',
            '2-8,3-7',
            '6-6,4-6',
            '2-6,4-8']

    part1_matches = 0
    part2_matches = 0
    for input_line in data:
        assignment = parse_line(input_line)
        matches = assignment.Elf1 & assignment.Elf2
        if (matches & assignment.Elf1 == assignment.Elf1) or (matches & assignment.Elf2 == assignment.Elf2):
            part1_matches += 1
        elif len(matches) > 0:
            part2_matches += 1
    print(f'Part 1: {part1_matches}')
    print(f'Part 2: {part1_matches + part2_matches}')
