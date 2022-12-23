from aocd import get_data
from parse import parse
import sympy

def parse_input_lines(data):
    monkeys = {}
    for input_line in data:
        monkey_id, monkey_args = parse('{}: {}', input_line)
        try:
            monkeys[monkey_id] = int(monkey_args)
        except ValueError:
            monkeys[monkey_id] = monkey_args

    return monkeys


def part1(monkeys_to_search, search_monkey_id: str) -> int:
    while isinstance(monkeys_to_search[search_monkey_id], str):
        for key, value in monkeys_to_search.items():
            if isinstance(value, int):
                continue
            else:
                left_side, operand, right_side = parse('{} {} {}', value)
                if left_side.lower().islower() and isinstance(monkeys_to_search[left_side], int):
                    left_side = monkeys_to_search[left_side]
                if right_side.lower().islower() and isinstance(monkeys_to_search[right_side], int):
                    right_side = monkeys_to_search[right_side]
                new_value = f'{left_side} {operand} {right_side}'
                monkeys_to_search[key] = new_value
                if new_value.lower().islower():
                    continue
                else:
                    try:
                        monkeys_to_search[key] = int(eval(new_value))
                        break
                    except:
                        continue
    return monkeys_to_search[search_monkey_id]


if __name__ == '__main__':
    data = [
        'root: pppw + sjmn',
        'dbpl: 5',
        'cczh: sllz + lgvd',
        'zczc: 2',
        'ptdq: humn - dvpt',
        'dvpt: 3',
        'lfqf: 4',
        'humn: 5',
        'ljgn: 2',
        'sjmn: drzm * dbpl',
        'sllz: 4',
        'pppw: cczh / lfqf',
        'lgvd: ljgn * ptdq',
        'drzm: hmdt - zczc',
        'hmdt: 32'
    ]
    # data = get_data(day=21, year=2022).splitlines()

    # sympy.solve(sympy.Integer('4') - sympy.Integer())

    screaming_monkeys = parse_input_lines(data)
    root_monkey_id = 'root'

    part1_answer = part1(screaming_monkeys, root_monkey_id)
    print(f'Part 1: {part1_answer}')
