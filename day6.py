from aocd import get_data

if __name__ == '__main__':
    # data = [
    #     'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw',
    # ]
    data = get_data(day=6, year=2022).splitlines()
    packet_marker_size = 4
    current_index = 0
    input = data[0]

    while current_index + packet_marker_size < len(input):
        packet = set(input[current_index:current_index + packet_marker_size])
        if len(packet) == packet_marker_size:
            break
        current_index += 1
    print(f'Part 1: {current_index + packet_marker_size}')

    start_of_message = 14
    current_index = 0

    while current_index + start_of_message < len(input):
        packet = set(input[current_index:current_index + start_of_message])
        if len(packet) == start_of_message:
            break
        current_index += 1
    print(f'Part 2: {current_index + start_of_message}')
