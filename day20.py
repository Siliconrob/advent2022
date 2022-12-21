from dataclasses import dataclass
from typing import TypeVar

from aocd import get_data

Node = TypeVar("Node")


@dataclass
class Node:
    Value: int
    Next: Node
    Previous: Node


def build_double_linked_list(original_data):
    nodes = [Node(input_value, None, None) for input_value in [int(z) for z in original_data]]
    for index, current_node in enumerate(nodes):
        current_node.Previous = nodes[(index - 1) % len(nodes)]
        current_node.Next = nodes[(index + 1) % len(nodes)]
    return nodes


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

    zero_node = None
    list_length = len(nodes) - 1

    for current_node in nodes:
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
    part1_answer = 0
    for loops in range(3):
        for steps_in_loop in range(1000):
            zero_node = zero_node.Next
        part1_answer += zero_node.Value
    print(f'Part 1: {part1_answer}')
