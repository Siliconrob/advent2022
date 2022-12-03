import types
from aocd import get_data
from dataclasses import dataclass, field
from parse import parse
from enum import Enum

# https://stackoverflow.com/questions/22571259/split-a-string-into-n-equal-parts
def chunk(in_string,num_chunks):
    chunk_size = len(in_string)//num_chunks
    if len(in_string) % num_chunks: chunk_size += 1
    iterator = iter(in_string)
    for _ in range(num_chunks):
        accumulator = list()
        for _ in range(chunk_size):
            try: accumulator.append(next(iterator))
            except StopIteration: break
        yield ''.join(accumulator)

chars = 'abcdefghijklmnopqrstuvwxyz'
alphabet = ''.join([chars, chars.upper()])


if __name__ == '__main__':
    # data = ['vJrwpWtwJgWrhcsFMMfFFhFp',
    #         'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL',
    #         'PmmdzqPrVvPwwTWBwg',
    #         'wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn',
    #         'ttgJtRGJQctTZtZT',
    #         'CrZsJsPPZsGzwwsLwLmpwMDw'
    # ]
    data = get_data(day=3, year=2022).splitlines()
    priorities = []
    for input_line in data:
        chunks = list(chunk(input_line, 2))
        first_half = set(chunks[0])
        second_half = set(chunks[1])
        common_elements = first_half & second_half
        priority = alphabet.index(common_elements.pop()) + 1
        priorities.append(priority)

    print(f'Part 1: {sum(priorities)}')

    # print(f'Part 2: {part2()}')
