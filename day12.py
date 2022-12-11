from collections import deque
from dataclasses import dataclass
from aocd import get_data
from parse import parse


@dataclass
class Monkey:
    Raw: list[str]
    CurrentItems: deque[int] = deque[int]
    ItemsInspected: int = 0

    def inspect(self, worry_func, monkeys):
        while len(self.CurrentItems) > 0:
            current_item = self.CurrentItems.popleft()
            parsed = parse('{} = {} {} {}', self.Raw[2].split(':').pop()).fixed
            operation_func = lambda x, y: x * y
            if parsed[2] == "+":
                operation_func = lambda x, y: x + y
            last_arg = current_item
            if parsed[3] != "old":
                last_arg = int(parsed[3])
            new_worry_level = operation_func(current_item, last_arg)
            self.ItemsInspected += 1
            bored_value = worry_func(new_worry_level)
            q, r = divmod(bored_value, self.test())
            new_monkey_index = self.if_true() if r == 0 else self.if_false()
            monkeys[new_monkey_index].CurrentItems.append(bored_value)

    def if_true(self):
        return int(self.Raw[4].split(':')[1].split(' ').pop())

    def if_false(self):
        return int(self.Raw[5].split(':')[1].split(' ').pop())

    def test(self):
        return int(self.Raw[3].split(':')[1].split(' ').pop())

    def starting_items(self):
        return [int(item) for item in self.Raw[1].split(':')[1].split(',')]

    def id(self):
        parsed = parse('{} {:d}:', self.Raw[0]).fixed
        return parsed[1]

    def run_operation(self):
        pass


def parse_monkey_inputs(data) -> dict:
    monkeys = {}
    monkey_input_lines = []
    for input_line in data:
        if input_line == '':
            current_monkey = Monkey(monkey_input_lines)
            current_monkey.CurrentItems = deque(current_monkey.starting_items())
            monkeys[current_monkey.id()] = current_monkey
            monkey_input_lines = []
        else:
            monkey_input_lines.append(input_line)
    current_monkey = Monkey(monkey_input_lines)
    current_monkey.CurrentItems = deque(current_monkey.starting_items())
    monkeys[current_monkey.id()] = current_monkey

    return monkeys


def monkey_business_factor(input_monkeys):
    answer = 1
    for top_monkeys in sorted(input_monkeys, key=lambda x: (input_monkeys[x].ItemsInspected), reverse=True)[:2]:
        answer *= input_monkeys[top_monkeys].ItemsInspected
    return answer


if __name__ == '__main__':
    data = [
        'Monkey 0:',
        '  Starting items: 79, 98',
        '  Operation: new = old * 19',
        '  Test: divisible by 23',
        '    If true: throw to monkey 2',
        '    If false: throw to monkey 3',
        '',
        'Monkey 1:',
        '  Starting ,items: 54, 65, 75, 74',
        '  Operation: new = old + 6',
        '  Test: divisible by 19',
        '    If true: throw to monkey 2',
        '    If false: throw to monkey 0',
        '',
        'Monkey 2:',
        '  Starting ,items: 79, 60, 97',
        '  Operation: new = old * old',
        '  Test: divisible by 13',
        '    If true: throw to monkey 1',
        '    If false: throw to monkey 3',
        '',
        'Monkey 3:',
        '  Starting items: 74',
        '  Operation: new = old + 3',
        '  Test: divisible by 17',
        '    If true: throw to monkey 0',
        '    If false: throw to monkey 1'
    ]
    # data = get_data(day=11, year=2022).splitlines()

    monkeys = parse_monkey_inputs(data)

    for round in range(0, 20):
        for current_monkey in monkeys.values():
            current_monkey.inspect(lambda x: x // 3, monkeys)

    part1_answer = monkey_business_factor(monkeys)
    print(f'Part 1: {part1_answer}')

    # You can multiply all the divisors to get a least common multiple across all monkeys
    # Math tip here
    # https://www.youtube.com/watch?v=F4MCuPZDKog
    mod_products = 1
    for monkey in monkeys.values():
        mod_products *= monkey.test()

    monkeys = parse_monkey_inputs(data)
    for round in range(0, 10000):
        for current_monkey in monkeys.values():
            current_monkey.inspect(lambda x: x % mod_products, monkeys)

    part2_answer = monkey_business_factor(monkeys)
    print(f'Part 2: {part2_answer}')
