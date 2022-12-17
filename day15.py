from dataclasses import dataclass
from aocd import get_data
from parse import parse
from shapely import LineString, geometry


@dataclass(kw_only=True, frozen=True)
class Point:
    X: int
    Y: int

@dataclass()
class Scan:
    Sensor: Point
    Beacon: Point

    def distance(self):
        return abs(self.Sensor.X - self.Beacon.X) + abs(self.Sensor.Y - self.Beacon.Y)

    def get_points(self):
        current_distance = self.distance()
        points = [
            geometry.Point(self.Sensor.X - current_distance, self.Sensor.Y),
            geometry.Point(self.Sensor.X, self.Sensor.Y - current_distance),
            geometry.Point(self.Sensor.X + current_distance, self.Sensor.Y),
            geometry.Point(self.Sensor.X, self.Sensor.Y + current_distance),
            geometry.Point(self.Sensor.X - current_distance, self.Sensor.Y)
        ]
        return points

    def get_polygon(self):
        return geometry.Polygon([[p.x, p.y] for p in self.get_points()])

def read_scan_inputs(input_lines):
    details = []
    for line in input_lines:
        parse_result = parse(input_line_template, line).fixed
        new_scan = Scan(Point(X=parse_result[0], Y=parse_result[1]), Point(X=parse_result[2], Y=parse_result[3]))
        details.append(new_scan)
    return details


def part1(intersection_line, scan_inputs):
    beacons_on_line = set()
    scanners_on_line = set()
    segments = set()
    for scanner in scan_inputs:
        if scanner.Beacon.Y == target_y_line:
            beacons_on_line.add(scanner.Beacon)
        if scanner.Sensor.Y == target_y_line:
            scanners_on_line.add(scanner.Sensor)
        current_poly = scanner.get_polygon()
        intersection = current_poly.intersection(intersection_line)
        if intersection.wkt != 'LINESTRING Z EMPTY':
            x_coords = [int(intersection.bounds[0]), int(intersection.bounds[2])]
            x_coords.sort()
            segments = segments.union(set(range(x_coords[0], x_coords[1] + 1)))
    return len(segments) - len(beacons_on_line)


if __name__ == '__main__':
    data = [
        'Sensor at x=2, y=18: closest beacon is at x=-2, y=15',
        'Sensor at x=9, y=16: closest beacon is at x=10, y=16',
        'Sensor at x=13, y=2: closest beacon is at x=15, y=3',
        'Sensor at x=12, y=14: closest beacon is at x=10, y=16',
        'Sensor at x=10, y=20: closest beacon is at x=10, y=16',
        'Sensor at x=14, y=17: closest beacon is at x=10, y=16',
        'Sensor at x=8, y=7: closest beacon is at x=2, y=10',
        'Sensor at x=2, y=0: closest beacon is at x=2, y=10',
        'Sensor at x=0, y=11: closest beacon is at x=2, y=10',
        'Sensor at x=20, y=14: closest beacon is at x=25, y=17',
        'Sensor at x=17, y=20: closest beacon is at x=21, y=22',
        'Sensor at x=16, y=7: closest beacon is at x=15, y=3',
        'Sensor at x=14, y=3: closest beacon is at x=15, y=3',
        'Sensor at x=20, y=1: closest beacon is at x=15, y=3'
    ]

    input_line_template = "Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}"

    data = get_data(day=15, year=2022).splitlines()

    scan_details = read_scan_inputs(data)
    target_y_line = 2000000

    line_infinity_bound = 10000000
    draw_line = LineString([geometry.Point(line_infinity_bound * -1, target_y_line), geometry.Point(line_infinity_bound, target_y_line)])

    print(f'Part 1: {part1(draw_line, scan_details)}')
