from aocd import get_data
from shapely import LineString, Polygon, difference, geometry, LinearRing

def parse_input(input_data):
	elves = set()
	for y_index, row in enumerate(input_data):
		for x_index, position_value in enumerate(row):
			if position_value == '#':
				elves.add(f'{x_index}_{y_index}')
	return elves


def read_key(input):
	splits = input.split('_')
	return int(splits[0]), int(splits[1])


def all_positions(x, y):
	return set([
		f'{x - 1}_{y - 1}', #NW
		f'{x - 1}_{y}',  # W
		f'{x - 1}_{y + 1}',  # SW
		f'{x}_{y - 1}', #N
		f'{x}_{y + 1}',  # S
		f'{x + 1}_{y - 1}',  # NE
		f'{x + 1}_{y}',  # E
		f'{x + 1}_{y + 1}',  # SE
	])

def north_positions(x, y):
	return set([
		f'{x - 1}_{y - 1}', #NW
		f'{x}_{y - 1}', #N
		f'{x + 1}_{y - 1}' #NE
	])

def south_positions(x, y):
	return set([
		f'{x - 1}_{y + 1}', #SW
		f'{x}_{y + 1}', #S
		f'{x + 1}_{y + 1}' #SE
	])


def west_positions(x, y):
	return set([
		f'{x - 1}_{y - 1}', #NW
		f'{x - 1 }_{y}', #W
		f'{x - 1}_{y + 1}' #SW
	])


def east_positions(x, y):
	return set([
		f'{x + 1}_{y - 1}', #NE
		f'{x + 1}_{y}', #E
		f'{x + 1}_{y + 1}' #SE
	])

def move(input_elf_frame, round):
	proposed_elf_frame = []

	for _, key in enumerate(input_elf_frame):
		x, y = read_key(key)
		all = all_positions(x, y)
		if all.isdisjoint(input_elf_frame):
			proposed_elf_frame.append(key)
			continue
		north = north_positions(x, y)
		if north.isdisjoint(input_elf_frame):
			proposed_elf_frame.append(f'{x}_{y - 1}')
			continue
		south = south_positions(x, y)
		if south.isdisjoint(input_elf_frame):
			proposed_elf_frame.append(f'{x}_{y + 1}')
			continue
		west = west_positions(x, y)
		if west.isdisjoint(input_elf_frame):
			proposed_elf_frame.append(f'{x - 1}_{y}')
			continue
		east = east_positions(x, y)
		if east.isdisjoint(input_elf_frame):
			proposed_elf_frame.append(f'{x + 1}_{y}')
			continue
		else:
		 	proposed_elf_frame.append(key)

	next_elf_frame = set()
	for old, new in zip(input_elf_frame, proposed_elf_frame):
		if old == new:
			next_elf_frame.add(old)
		elif proposed_elf_frame.count(new) > 1:
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

	x_list = []
	y_list = []
	for _, key in enumerate(input_elves):
		x, y = read_key(key)
		x_list.append(x)
		y_list.append(y)

	coords = list(zip(x_list, y_list))
	for y_index in range(min(y_list), max(y_list) + 1):
		row = ''
		for x_index in range(min(x_list), max(x_list) + 1):
			if (x_index, y_index) in coords:
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