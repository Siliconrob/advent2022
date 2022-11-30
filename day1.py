import itertools
from aocd import get_data

if __name__ == '__main__':
    data = [int(i) for i in list(get_data(day=1, year=2022).splitlines())]
    print("Preparing")