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


def algebra_solve(input):
    left_side, operand, right_side = parse('{} {} {}', input)
    if isinstance(left_side, str) or isinstance(right_side, str):
        return False
    return True

def part2(monkeys_to_search, search_monkey_id, human_id) -> int:

    # Setup functions to run for solver
    math = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: x / y
    }

    # assign the variable
    symbolic_monkeys = { human_id: sympy.Symbol("x") }

    # you can keep appending to a list as it loops through to run over and over
    for next_line in monkeys_to_search:
        current_key, current_value = parse('{}: {}', next_line)
        if current_key in symbolic_monkeys:
            continue
        if not current_value.lower().islower():
            symbolic_monkeys[current_key] = sympy.Integer(current_value) # make sure solver knows this is an integer
        else:
            left_side, fn, right_side = parse('{} {} {}', current_value)
            if left_side in symbolic_monkeys and right_side in symbolic_monkeys:
                if current_key == search_monkey_id:
                    # You want solver to find your varilable so subtract the 2 sides to get what x needs to be to balance
                    # the equations, only 1 value so pop it off
                    solved = sympy.solve(symbolic_monkeys[left_side] - symbolic_monkeys[right_side]).pop()
                    return solved
                # Build the set of algebra rules as lambdas with say x - 3 (value) etc
                symbolic_monkeys[current_key] = math[fn](symbolic_monkeys[left_side], symbolic_monkeys[right_side])
            else:
                # line isn't expressible in single variable yet so add it back to the list so it will be reprocessed
                monkeys_to_search.append(next_line)

    return None

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

    human_id = 'humn'

    part2_answer = part2(data, root_monkey_id, human_id)
    print(f'Part 2: {part2_answer}')