from dataclasses import dataclass
from enum import Enum

from aocd import get_data
from parse import parse

@dataclass
class Cycle:
    Count: int
    Register: int
    Instruction: str
    def signal_strength(self) -> int:
        return self.Count * self.Register

def part1(instructions: list[str]) -> list[Cycle]:

    current_run = []

    cycle = 0
    current_value = 1

    for instruction in instructions:
        # print(instruction)
        cycle += 1
        if instruction == "noop":
            current_cycle = Cycle(Count=cycle, Register=current_value, Instruction=instruction)
            current_run.append(current_cycle)
            continue
        else:
            parsed_instruction = parse('{} {}', instruction).fixed
            current_cycle = Cycle(Count=cycle, Register=current_value, Instruction=instruction)
            current_run.append(current_cycle)
            cycle += 1
            current_cycle = Cycle(Count=cycle, Register=current_value, Instruction=instruction)
            current_value += int(parsed_instruction[1])
            current_run.append(current_cycle)

    return current_run


def part2(input_moves: list[str]):
    pass

if __name__ == '__main__':
    # data = [
    #     'R 4',
    #     'U 4',
    #     'L 3',
    #     'D 1',
    #     'R 4',
    #     'D 1',
    #     'L 5',
    #     'R 2'
    # ]

    data = [
        'addx 15',
        'addx -11',
        'addx 6',
        'addx -3',
        'addx 5',
        'addx -1',
        'addx -8',
        'addx 13',
        'addx 4',
        'noop',
        'addx -1',
        'addx 5',
        'addx -1',
        'addx 5',
        'addx -1',
        'addx 5',
        'addx -1',
        'addx 5',
        'addx -1',
        'addx -35',
        'addx 1',
        'addx 24',
        'addx -19',
        'addx 1',
        'addx 16',
        'addx -11',
        'noop',
        'noop',
        'addx 21',
        'addx -15',
        'noop',
        'noop',
        'addx -3',
        'addx 9',
        'addx 1',
        'addx -3',
        'addx 8',
        'addx 1',
        'addx 5',
        'noop',
        'noop',
        'noop',
        'noop',
        'noop',
        'addx -36',
        'noop',
        'addx 1',
        'addx 7',
        'noop',
        'noop',
        'noop',
        'addx 2',
        'addx 6',
        'noop',
        'noop',
        'noop',
        'noop',
        'noop',
        'addx 1',
        'noop',
        'noop',
        'addx 7',
        'addx 1',
        'noop',
        'addx -13',
        'addx 13',
        'addx 7',
        'noop',
        'addx 1',
        'addx -33',
        'noop',
        'noop',
        'noop',
        'addx 2',
        'noop',
        'noop',
        'noop',
        'addx 8',
        'noop',
        'addx -1',
        'addx 2',
        'addx 1',
        'noop',
        'addx 17',
        'addx -9',
        'addx 1',
        'addx 1',
        'addx -3',
        'addx 11',
        'noop',
        'noop',
        'addx 1',
        'noop',
        'addx 1',
        'noop',
        'noop',
        'addx -13',
        'addx -19',
        'addx 1',
        'addx 3',
        'addx 26',
        'addx -30',
        'addx 12',
        'addx -1',
        'addx 3',
        'addx 1',
        'noop',
        'noop',
        'noop',
        'addx -9',
        'addx 18',
        'addx 1',
        'addx 2',
        'noop',
        'noop',
        'addx 9',
        'noop',
        'noop',
        'noop',
        'addx -1',
        'addx 2',
        'addx -37',
        'addx 1',
        'addx 3',
        'noop',
        'addx 15',
        'addx -21',
        'addx 22',
        'addx -6',
        'addx 1',
        'noop',
        'addx 2',
        'addx 1',
        'noop',
        'addx -10',
        'noop',
        'noop',
        'addx 20',
        'addx 1',
        'addx 2',
        'addx 2',
        'addx -6',
        'addx -11',
        'noop',
        'noop',
        'noop'
    ]

    data = get_data(day=10, year=2022).splitlines()

    start_index = 19
    increment = 40
    part1_run = part1(data)

    key_cycles = [
        part1_run[start_index],
        part1_run[start_index + increment],
        part1_run[start_index + increment * 2],
        part1_run[start_index + increment * 3],
        part1_run[start_index + increment * 4],
        part1_run[start_index + increment * 5]
    ]

    for key_cycle in key_cycles:
        print(f'[{key_cycle.Count}]({key_cycle.Instruction}, {key_cycle.Register}): {key_cycle.signal_strength()}')

    part1_answer = sum([key_cycle.signal_strength() for key_cycle in key_cycles])

    print(f'Part 1: {part1_answer}')

    # print(f'Part 1: {part1(data)}')
    # print(f'Part 2: {part2(data)}')
