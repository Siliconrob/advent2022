from dataclasses import dataclass
from aocd import get_data
from parse import parse


@dataclass
class Cycle:
    Count: int
    Register: int
    Instruction: str

    def signal_strength(self) -> int:
        return self.Count * self.Register


def part2(instructions: list[str]) -> str:
    current_run = []
    cycle = 0
    current_value = 1
    screen_draw = ''
    for instruction in instructions:
        # print(instruction)
        cycle += 1
        if instruction == "noop":
            cycle, screen_draw = run_cycle(current_run, current_value, cycle, instruction, screen_draw)
        else:
            parsed_instruction = parse('{} {}', instruction).fixed
            cycle, screen_draw = run_cycle(current_run, current_value, cycle, instruction, screen_draw)
            cycle += 1
            cycle, screen_draw = run_cycle(current_run, current_value, cycle, instruction, screen_draw)
            current_value += int(parsed_instruction[1])

    return screen_draw


def run_cycle(current_run: list[Cycle], current_value: int, cycle: int, instruction: str, screen_draw: str) -> (int, str):
    current_cycle = Cycle(Count=cycle, Register=current_value, Instruction=instruction)
    current_run.append(current_cycle)
    new_pixel = pixel_type(current_cycle, cycle - 1)
    cycle = 0 if '\n' in new_pixel else cycle
    screen_draw += new_pixel
    return cycle, screen_draw


def pixel_type(current_cycle: Cycle, sprite_position: int) -> str:
    print_char = ''
    q, r = divmod(current_cycle.Count, 40)

    if r == 0:
        print_char = '\n'
    if current_cycle.Register in [sprite_position - 1, sprite_position, sprite_position + 1]:
        return f'#{print_char}'
    else:
        return f'.{print_char}'


def part1(instructions: list[str]) -> int:
    current_run = []
    cycle = 0
    current_value = 1

    for instruction in instructions:
        cycle += 1
        if instruction == "noop":
            current_run.append(Cycle(Count=cycle, Register=current_value, Instruction=instruction))
        else:
            parsed_instruction = parse('{} {}', instruction).fixed
            current_run.append(Cycle(Count=cycle, Register=current_value, Instruction=instruction))
            cycle += 1
            current_run.append(Cycle(Count=cycle, Register=current_value, Instruction=instruction))
            current_value += int(parsed_instruction[1])

    key_cycles = [current_run[key_index] for key_index in range(19, 221, 40)]
    return sum([key_cycle.signal_strength() for key_cycle in key_cycles])


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

    print(f'Part 1: {part1(data)}')
    print(f'Part 2: \n\n{part2(data)}')
