import itertools
import re
from collections import deque
from copy import deepcopy
from aocd import get_data
from parse import parse


if __name__ == '__main__':
    data = [
        'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg',
    ]
    data = get_data(day=6, year=2022).splitlines()
    packet_marker_size = 4
    current_index = 0
    input = data[0]

    # for each in itertools.permutations(input, 4):
    #     print(each)

    while current_index + packet_marker_size < len(input):
        packet = set(input[current_index:current_index+packet_marker_size])
        if len(packet) == packet_marker_size:
            break
        current_index += 1
    print(f'Part 1: {current_index + packet_marker_size}')




    #
    # for index in data[0]:
    #     print(index)
    #
    #
    # while len(stream_reader) < packet_marker_size:
    #     current_char = input_stream.popleft()
    #     if current_char in stream_reader:
    #         if len(stream_reader) > 0:
    #             stream_reader.popleft()
    #     else:
    #         stream_reader.append(current_char)
    #     current_index += 1
    #
    # print(f'Part 1: {current_index - 1}')






    # splitter_index = data.index('')
    # initial_state = data[:splitter_index - 1]
    # commands = data[splitter_index + 1:]
    #
    # stack_start = build_initial_state(initial_state)
    # part1_stack_start = deepcopy(stack_start)
    # part2_stack_start = deepcopy(stack_start)
    #
    # print(f'Part 1: {part1(part1_stack_start, commands)}')
    # print(f'Part 2: {part2(part2_stack_start, commands)}')
