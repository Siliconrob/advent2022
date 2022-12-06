from aocd import get_data


def read_input_stream(packet_length, input_line):
    current_index = 0
    while current_index + packet_length < len(input_line):
        packet = set(input_line[current_index:current_index + packet_length])
        if len(packet) == packet_length:
            break
        current_index += 1
    return current_index + packet_length


if __name__ == '__main__':
    data = [
        'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw',
    ]

    #data = get_data(day=7, year=2022).splitlines()
    part1_index = read_input_stream(4, data[0])
    print(f'Part 1: {part1_index}')

    part2_index = read_input_stream(14, data[0])
    print(f'Part 2: {part2_index}')
