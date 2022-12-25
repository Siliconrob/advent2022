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
