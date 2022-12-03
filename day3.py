import string
from aocd import get_data
import more_itertools as mit


# https://stackoverflow.com/questions/22571259/split-a-string-into-n-equal-parts
def chunk(in_string, num_chunks):
    chunk_size = len(in_string) // num_chunks
    if len(in_string) % num_chunks: chunk_size += 1
    iterator = iter(in_string)
    for _ in range(num_chunks):
        accumulator = list()
        for _ in range(chunk_size):
            try:
                accumulator.append(next(iterator))
            except StopIteration:
                break
        yield ''.join(accumulator)


def part1_priority(alphabet: str, input_line: str) -> list[int]:
    chunks = list(chunk(input_line, 2))
    return alphabet.index((set(chunks[0]) & set(chunks[1])).pop()) + 1


# https://stackoverflow.com/questions/312443/how-do-i-split-a-list-into-equally-sized-chunks
def part2_priorities(alphabet: str, input_lines: list[str]) -> list[int]:
    return [(alphabet.index((set(basket[0]) & set(basket[1]) & set(basket[2])).pop()) + 1) for basket in list(mit.batched(input_lines, 3))]

if __name__ == '__main__':
    data = get_data(day=3, year=2022).splitlines()
    # data = ['vJrwpWtwJgWrhcsFMMfFFhFp',
    #         'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL',
    #         'PmmdzqPrVvPwwTWBwg',
    #         'wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn',
    #         'ttgJtRGJQctTZtZT',
    #         'CrZsJsPPZsGzwwsLwLmpwMDw'
    # ]

    alphabet: str = ''.join([string.ascii_lowercase, string.ascii_uppercase])
    part1_priorities = [part1_priority(alphabet, input_line) for input_line in data]
    print(f'Part 1: {sum(part1_priorities)}')

    part2_answer = part2_priorities(alphabet, data)
    print(f'Part 2: {sum(part2_answer)}')
