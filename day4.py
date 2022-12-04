import string
from dataclasses import dataclass
from aocd import get_data
import more_itertools as mit
from parse import parse

@dataclass
class ElfAssignments:
    Elf1: set
    Elf2: set


def part1_priority(alphabet: str, input_line: str) -> list[int]:
    chunk1, chunk2 = mit.divide(2, list(input_line))
    common = set(''.join(list(chunk1))) & set(''.join(list(chunk2)))
    return alphabet.index(common.pop()) + 1


# https://stackoverflow.com/questions/312443/how-do-i-split-a-list-into-equally-sized-chunks
def part2_priorities(alphabet: str, input_lines: list[str]) -> list[int]:
    return [(alphabet.index((set(basket[0]) & set(basket[1]) & set(basket[2])).pop()) + 1) for basket in list(mit.batched(input_lines, 3))]

# def expand_range(elf_range_assignment: str) -> str:
#      = parse('{} {}', elf_pair_input)

def parse_line(elf_pair_input: str):
    elf1_range_start, elf1_range_end, elf2_range_start, elf2_range_end = parse('{:d}-{:d},{:d}-{:d}', elf_pair_input)
    elf1_assignment = set(list(range(elf1_range_start, elf1_range_end + 1)))
    elf2_assignment = set(list(range(elf2_range_start, elf2_range_end + 1)))
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
    for input_line in data:
        assignment = parse_line(input_line)
        matches = assignment.Elf1 & assignment.Elf2
        if (matches & assignment.Elf1 == assignment.Elf1) or (matches & assignment.Elf2 == assignment.Elf2):
            part1_matches += 1
        #print(matches)
    print(f'Part 1: {part1_matches}')

