from collections import Counter

from aocd import get_data
from shapely import LineString, Polygon, difference, geometry, LinearRing

def parse_input(input_data):
	elves = set()
	for y_index, row in enumerate(input_data):
		for x_index, position_value in enumerate(row):
			if position_value == '#':
				elves.add((x_index, y_index))
	return elves


def all_positions(x, y):
	return set([
		(x - 1, y - 1), #NW
		(x - 1, y),  # W
		(x - 1, y + 1),  # SW
		(x, y - 1), #N
		(x, y + 1),  # S
		(x + 1, y - 1),  # NE
		(x + 1, y),  # E
		(x + 1, y + 1),  # SE
	])

def north_positions(x, y):
	return set([
		(x - 1,y - 1), #NW
		(x,y - 1), #N
		(x + 1,y - 1) #NE
	])

def south_positions(x, y):
	return set([
		(x - 1,y + 1), #SW
		(x,y + 1), #S
		(x + 1,y + 1) #SE
	])


def west_positions(x, y):
	return set([
		(x - 1,y - 1), #NW
		(x - 1 ,y), #W
		(x - 1,y + 1) #SW
	])


def east_positions(x, y):
	return set([
		(x + 1,y - 1), #NE
		(x + 1,y), #E
		(x + 1,y + 1) #SE
	])

def move(input_elf_frame, round):
	proposed_elf_frame = []

	for _, position in enumerate(input_elf_frame):
		x, y = position
		all = all_positions(x, y)
		if all.isdisjoint(input_elf_frame):
			proposed_elf_frame.append(position)
			continue
		north = north_positions(x, y)
		if north.isdisjoint(input_elf_frame):
			proposed_elf_frame.append((x, y - 1))
			continue
		south = south_positions(x, y)
		if south.isdisjoint(input_elf_frame):
			proposed_elf_frame.append((x ,y + 1))
			continue
		west = west_positions(x, y)
		if west.isdisjoint(input_elf_frame):
			proposed_elf_frame.append((x - 1,y))
			continue
		east = east_positions(x, y)
		if east.isdisjoint(input_elf_frame):
			proposed_elf_frame.append((x + 1, y))
			continue
		else:
		 	proposed_elf_frame.append(position)

	next_elf_frame = set()
	next_counts = Counter(proposed_elf_frame)

	for old, new in zip(input_elf_frame, proposed_elf_frame):
		if old == new:
			next_elf_frame.add(old)
		elif next_counts[new] > 1:
			next_elf_frame.add(old)
		else:
			next_elf_frame.add(new)

	return next_elf_frame



def part1(elves):
	show_map(elves)
	for round in range(0, 10):
		elves = move(elves, round)
		empties = show_map(elves)


def show_map(input_elves):
	empties = 0

	x_list = [x for x, y in input_elves]
	y_list = [y for x, y in input_elves]

	for y_index in range(min(y_list), max(y_list) + 1):
		row = ''
		for x_index in range(min(x_list), max(x_list) + 1):
			if (x_index, y_index) in input_elves:
				row += '#'
			else:
				row += '.'
				empties += 1
		print(row)
	print(f'Empties {empties}\n')
	return empties


if __name__ == '__main__':
	data = [
		'....#..',
		'..###.#',
		'#...#.#',
		'.#...##',
		'#.###..',
		'##.#.##',
		'.#..#..'
    ]

	data = [
		'.....',
		'..##.',
		'..#..',
		'.....',
		'..##.',
		'.....'
	]
    #data = get_data(day=23, year=2022).splitlines()
	elves = parse_input(data)

	part1_answer = part1(elves)
	print(f'Part 1: {part1_answer}')