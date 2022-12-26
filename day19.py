from collections import deque
from dataclasses import dataclass
from aocd import get_data
from parse import parse

#
# @dataclass(frozen=True)
# class CollectedMaterials:
#     Ore: int
#     Clay: int
#     Obsidian: int
#     Geode: int
#
#
# @dataclass(frozen=True)
# class RobotFleet:
#     Ore: int
#     Clay: int
#     Obsidian: int
#     Geode: int


@dataclass(frozen=True)
class Robot:
    Ore: int
    Clay: int
    Obsidian: int


@dataclass(frozen=True)
class Blueprint:
    Id: int
    OreRobot: Robot
    ClayRobot: Robot
    ObsidianRobot: Robot
    GeodeRobot: Robot

    def max_ore(self):
        return max(self.OreRobot.Ore, self.ClayRobot.Ore, self.ObsidianRobot.Ore, self.GeodeRobot.Ore)

    def max_clay(self):
        return max(self.OreRobot.Clay, self.ClayRobot.Clay, self.ObsidianRobot.Clay, self.GeodeRobot.Clay)

    def max_obsidian(self):
        return max(self.OreRobot.Obsidian, self.ClayRobot.Obsidian, self.ObsidianRobot.Obsidian,
                   self.GeodeRobot.Obsidian)


def parse_blueprints(input_lines):
    blue_prints = []
    template = "Blueprint {:d}: Each ore robot costs {:d} ore. Each clay robot costs {:d} ore. Each obsidian robot costs {:d} ore and {:d} clay. Each geode robot costs {:d} ore and {:d} obsidian."
    for input_line in input_lines:
        parsed = parse(template, input_line).fixed
        blue_prints.append(Blueprint(
            Id=parsed[0],
            OreRobot=Robot(Ore=parsed[1], Clay=0, Obsidian=0),
            ClayRobot=Robot(Ore=parsed[2], Clay=0, Obsidian=0),
            ObsidianRobot=Robot(Ore=parsed[3], Clay=parsed[4], Obsidian=0),
            GeodeRobot=Robot(Ore=parsed[5], Clay=0, Obsidian=parsed[6])
        ))
    return blue_prints


def best_case_scenario(initial_amount, robots, t):
    return initial_amount + robots * (t + 1) + t * (t + 1) // 2


def search(start_time, blueprint):


    ORE, CLAY, OBS, GEO = range(4)

    best = 0
    visited = set()
    current_search = deque([(start_time, 0, 0, 0, 0, 1, 0, 0, 0, ())])


    while current_search:
        current_state = current_search.pop()

        state = current_state[:-1]
        if state in visited:
            continue

        visited.add(state)

        current_time, ore, clay, obsidian, geode, ore_robots, clay_robots, obsidian_robots, geode_robots, did_not_build = current_state

        new_ore = ore + ore_robots
        new_clay = clay + clay_robots
        new_obsidian = obsidian + obsidian_robots
        new_geode = geode + geode_robots
        current_time -= 1

        if current_time == 0:
            best = max(best, new_geode)
            continue

        if best_case_scenario(new_geode, geode_robots, current_time) < best:
            continue

        if best_case_scenario(new_obsidian, obsidian_robots, current_time) < blueprint.GeodeRobot.Obsidian or best_case_scenario(new_ore, ore_robots, current_time) < blueprint.GeodeRobot.Ore:
            best = max(best, new_geode + geode_robots * current_time)
            continue

        can_build = []

        # build geode robot
        if obsidian >= blueprint.GeodeRobot.Obsidian and ore >= blueprint.GeodeRobot.Ore and GEO not in did_not_build:
            can_build.append(GEO)
            current_search.append((current_time, new_ore - blueprint.GeodeRobot.Obsidian, new_clay, new_obsidian - blueprint.GeodeRobot.Obsidian, new_geode, ore_robots, clay_robots, obsidian_robots, geode_robots + 1, can_build))

        # build an obsidian robot
        if obsidian_robots < blueprint.max_obsidian() and clay >= blueprint.ClayRobot.Clay and ore >= blueprint.ObsidianRobot.Ore and OBS not in did_not_build:
            can_build.append(OBS)
            current_search.append((current_time, new_ore - blueprint.ObsidianRobot.Ore, new_clay - blueprint.ObsidianRobot.Clay, new_obsidian, new_geode, ore_robots, clay_robots, obsidian_robots + 1, geode_robots, ()))

        # build a clay robot
        if clay_robots < blueprint.max_clay() and ore >= blueprint.ClayRobot.Ore and CLAY not in did_not_build:
            can_build.append(CLAY)
            current_search.append((current_time, new_ore - blueprint.ClayRobot.Ore, new_clay, new_obsidian, new_geode, ore_robots, clay_robots + 1, obsidian_robots, geode_robots, ()))

        # Build an ore robot
        if ore_robots < blueprint.max_ore() and ore >= blueprint.OreRobot.Ore and ORE not in did_not_build:
            can_build.append(ORE)
            current_search.append((current_time, new_ore - blueprint.OreRobot.Ore, new_clay, new_obsidian, new_geode, ore_robots + 1, clay_robots, obsidian_robots, geode_robots, ()))

        # Only collect
        if (ore_robots and obsidian < blueprint.max_obsidian()) or (clay_robots and clay < blueprint.max_clay()) or ore < blueprint.max_ore():
            current_search.append((current_time, new_ore, new_clay, new_obsidian, new_geode, ore_robots, clay_robots, obsidian_robots, geode_robots, can_build))

    return best


if __name__ == '__main__':
    data = [
        'Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.',
        'Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.'
    ]
    # data = get_data(day=19, year=2022).splitlines()


    blueprints = parse_blueprints(data)

    results = {}

    for blueprint in blueprints:
        results[blueprint.Id] = search(24, blueprint)

    part1_sum = 0
    for key, value in results.items():
        part1_sum += key * value

    print(f'Part 1: {part1_sum}')

