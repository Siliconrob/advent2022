from collections import deque
from dataclasses import dataclass
from aocd import get_data


@dataclass(frozen=True)
class Cube:
    x: int
    y: int
    z: int

    def neighbors(self):
        yield Cube(self.x + 1, self.y, self.z)
        yield Cube(self.x - 1, self.y, self.z)
        yield Cube(self.x, self.y + 1, self.z)
        yield Cube(self.x, self.y - 1, self.z)
        yield Cube(self.x, self.y, self.z + 1)
        yield Cube(self.x, self.y, self.z - 1)


def read_cubes(data):
    cubes = set()
    for input_line in data:
        positions = list(map(int, input_line.split(",")))
        cubes.add(Cube(positions[0], positions[1], positions[2]))
    return cubes


def part1(input_cubes):
    surface_area = 0
    for cube in input_cubes:
        connections = len(set(cube.neighbors()) & input_cubes)
        surface_area += 6 - connections
    return surface_area


def search(start_cube, input_cubes):
    current_visit = set()
    queue = deque([start_cube])
    marked = 0

    x_range, y_range, z_range = get_possible_range(input_cubes)

    while queue:
        current = queue.pop()
        if current in current_visit:
            continue

        current_visit.add(current)

        if current.x not in x_range or current.y not in y_range or current.z not in z_range:
            return 0, current_visit

        for neighbor in current.neighbors():
            if neighbor in input_cubes:
                marked += 1
            elif neighbor not in current_visit:
                queue.append(neighbor)

    return marked, current_visit


def get_possible_range(input_cubes):
    x_inputs = list(map(lambda z: z.x, input_cubes))
    y_inputs = list(map(lambda z: z.y, input_cubes))
    z_inputs = list(map(lambda z: z.z, input_cubes))

    return range(min(x_inputs), max(x_inputs) + 1), range(min(y_inputs), max(y_inputs) + 1), range(min(z_inputs),
                                                                                                   max(z_inputs) + 1)


def part2(input_cubes):
    x_range, y_range, z_range = get_possible_range(input_cubes)

    complete_set = set()
    for x in x_range:
        for y in y_range:
            for z in z_range:
                complete_set.add(Cube(x, y, z))

    visited_cubes = set()
    surface_area = part1(input_cubes)

    for current_cube in complete_set:
        if current_cube not in input_cubes and current_cube not in visited_cubes:
            marked, current_visits = search(current_cube, input_cubes)
            surface_area -= marked
            visited_cubes |= current_visits

    return surface_area


if __name__ == '__main__':
    data = [
        '2,2,2',
        '1,2,2',
        '3,2,2',
        '2,1,2',
        '2,3,2',
        '2,2,1',
        '2,2,3',
        '2,2,4',
        '2,2,6',
        '1,2,5',
        '3,2,5',
        '2,1,5',
        '2,3,5'
    ]

    data = get_data(day=18, year=2022).splitlines()
    current_cubes = read_cubes(data)
    print(f'Part 1: {part1(current_cubes)}')
    print(f'Part 2: {part2(current_cubes)}')
