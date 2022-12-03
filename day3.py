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


chars = 'abcdefghijklmnopqrstuvwxyz'
alphabet = ''.join([chars, chars.upper()])


def part1_priority(input_line: str) -> list[int]:
    chunks = list(chunk(input_line, 2))
    common_elements = set(chunks[0]) & set(chunks[1])
    priority = alphabet.index(common_elements.pop()) + 1
    return priority


def part2_priorities(input_lines: list[str]) -> list[int]:
    part2_priorities = []
    baskets = list(mit.batched(input_lines, 3))
    for basket in baskets:
        common_elements = set(basket[0]) & set(basket[1]) & set(basket[2])
        part2_priorities.append(alphabet.index(common_elements.pop()) + 1)
    return part2_priorities


if __name__ == '__main__':
    # data = ['vJrwpWtwJgWrhcsFMMfFFhFp',
    #         'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL',
    #         'PmmdzqPrVvPwwTWBwg',
    #         'wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn',
    #         'ttgJtRGJQctTZtZT',
    #         'CrZsJsPPZsGzwwsLwLmpwMDw'
    # ]
    data = get_data(day=3, year=2022).splitlines()
    part1_priorities = [part1_priority(input_line) for input_line in data]
    print(f'Part 1: {sum(part1_priorities)}')
    part2_answer = part2_priorities(data)
    print(f'Part 2: {sum(part2_answer)}')
