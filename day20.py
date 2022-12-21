from dataclasses import dataclass
from typing import TypeVar

from aocd import get_data

Node = TypeVar("Node")


@dataclass
class Node:
    Value: int
    Next: Node
    Previous: Node


def build_double_linked_list(original_data, multiplier = 1):
    nodes = [Node(input_value, None, None) for input_value in [int(z) * multiplier for z in original_data]]
    for index, current_node in enumerate(nodes):
        current_node.Previous = nodes[(index - 1) % len(nodes)]
        current_node.Next = nodes[(index + 1) % len(nodes)]
    return nodes


def mix_nodes(the_nodes, mixes=1):
    zero_node = None
    list_length = len(the_nodes) - 1
    for mix_times in range(mixes):
        for current_node in the_nodes:
            if current_node.Value == 0:
                zero_node = current_node
                continue
            target_node = current_node
            if target_node.Value < 0:
                for steps in range(-target_node.Value % list_length):
                    target_node = target_node.Previous
                if target_node == current_node:
                    continue
                current_node.Previous.Next = current_node.Next
                current_node.Next.Previous = current_node.Previous
                target_node.Previous.Next = current_node

                current_node.Previous = target_node.Previous
                target_node.Previous = current_node
                current_node.Next = target_node
            else:
                for steps in range(target_node.Value % list_length):
                    target_node = target_node.Next
                if target_node == current_node:
                    continue
                current_node.Next.Previous = current_node.Previous
                current_node.Previous.Next = current_node.Next
                target_node.Next.Previous = current_node

                current_node.Next = target_node.Next
                target_node.Next = current_node
                current_node.Previous = target_node
    return zero_node


def move_and_sum_nodes(start_node):
    answer = 0
    for loops in range(3):
        for steps_in_loop in range(1000):
            start_node = start_node.Next
        answer += start_node.Value
    return answer


if __name__ == '__main__':
    data = [
        '1',
        '2',
        '-3',
        '3',
        '-2',
        '0',
        '4'
    ]

    data = get_data(day=20, year=2022).splitlines()

    nodes = build_double_linked_list(data)
    part1_answer = move_and_sum_nodes(mix_nodes(nodes))
    print(f'Part 1: {part1_answer}')

    nodes = build_double_linked_list(data, multiplier=811589153)
    part2_answer = move_and_sum_nodes(mix_nodes(nodes, 10))
    print(f'Part 2: {part2_answer}')
