import math
from dataclasses import dataclass, field
from functools import cache
from itertools import starmap
from collections import Counter, deque
from aocd import get_data


def snafu_to_decimal(snafu_number):
    snafu_translation = {
        "2": 2,
        "1": 1,
        "0": 0,
        "-": -1,
        "=": -2
    }

    number = 0
    multiplier = 0
    input_chars = deque(snafu_number)
    while input_chars:
        snafu_char = input_chars.pop()
        place = int(math.pow(5, multiplier) if multiplier > 0 else 1)
        number += snafu_translation[snafu_char] * place
        multiplier += 1
    return number


def decimal_to_snafu(decimal_number):

    snafu_result = deque()
    while decimal_number:
        decimal_number, remainder = divmod(decimal_number, 5)
        if remainder > 2:
            decimal_number += 1
            if remainder == 3:
                snafu_result.appendleft('=')
            if remainder == 4:
                snafu_result.appendleft('-')
        else:
            snafu_result.appendleft(str(remainder))

    return ''.join(snafu_result)


if __name__ == '__main__':
    data = [
        '1=-0-2',
        '12111',
        '2=0=',
        '21',
        '2=01',
        '111',
        '20012',
        '112',
        '1=-1=',
        '1-12',
        '12',
        '1=',
        '122'
    ]

    data = get_data(day=25, year=2022).splitlines()

    total = sum([snafu_to_decimal(snafu) for snafu in data])
    snafu_result = decimal_to_snafu(total)

    print(f'Part 1: {snafu_result}')
