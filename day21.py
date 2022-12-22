from aocd import get_data
from parse import parse
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
            if isinstance(value, int) or isinstance(value, float):
                for k, v in monkeys_to_search.items():
                    if isinstance(v, str):
                        monkeys_to_search[k] = v.replace(key, str(value))
                        try:
                            monkeys_to_search[k] = eval(v)
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
    data = get_data(day=21, year=2022).splitlines()

    screaming_monkeys = parse_input_lines(data)
    root_monkey_id = 'root'

    part1_answer = part1(screaming_monkeys, root_monkey_id)
    print(f'Part 1: {part1_answer}')

