import itertools
from aocd import get_data

if __name__ == '__main__':
    data = get_data(day=1, year=2022).splitlines()
    # data = ['1000', '2000', '3000', '', '4000', '', '5000', '6000', '', '7000', '8000', '9000', '', '10000']

    elves = {}
    current_line = 0
    current_elf = 0

    while current_line < len(data):
        current_line_input = data[current_line]
        if current_line_input == '':
            current_elf += 1
            elves[current_elf] = []
            current_line += 1
            continue

        if current_elf not in elves:
            elves[current_elf] = []
        current_elf_calories = elves[current_elf]
        current_elf_calories.append(int(current_line_input))
        current_line += 1

    calorie_sums = [sum(elves[elf]) for elf in elves]
    calorie_sums.sort()

    max_total_calories = calorie_sums[-1]
    print(max_total_calories)

    top = calorie_sums[-3:]
    print(sum(top))

