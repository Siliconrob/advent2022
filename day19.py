from collections import deque
from dataclasses import dataclass
from aocd import get_data
from parse import parse


@dataclass(frozen=True)
class CollectedMaterials:
    Ore: int
    Clay: int
    Obsidian: int
    Geode: int


@dataclass(frozen=True)
class RobotFleet:
    Ore: int
    Clay: int
    Obsidian: int
    Geode: int


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


def search(current_time, blueprint, current_robots, collected_amounts):


    ORE, CLAY, OBS, GEO = range(4)

    best = 0
    visited = set()
    current_search = deque([(current_time, current_robots, collected_amounts, ())])

    while current_search:
        tmp = current_search.pop()

        state = tmp[:-1]
        if state in visited:
            continue

        visited.add(state)

        time, current_robots, collected_amounts, did_not_build = tmp

        new_ore = collected_amounts.Ore + current_robots.Ore
        new_clay = collected_amounts.Clay + current_robots.Clay
        new_obsidian = collected_amounts.Obsidian + current_robots.Obsidian
        new_geode = collected_amounts.Geode + current_robots.Geode
        time -= 1

        if time == 0:
            best = max(best, new_geode)
            continue

        if best_case_scenario(new_geode, current_robots.Geode, time) < best:
            continue

        if best_case_scenario(new_obsidian, current_robots.Obsidian, time) < blueprint.GeodeRobot.Obsidian or best_case_scenario(new_ore, current_robots.Ore, time) < blueprint.GeodeRobot.Ore:
            best = max(best, new_geode + current_robots.Geode * time)
            continue

        can_build = []

        if collected_amounts.Obsidian >= current_robots.Obsidian and current_robots.Ore >= blueprint.GeodeRobot.Ore and GEO not in did_not_build:
            can_build.append(GEO)
            new_robots = RobotFleet(Ore=current_robots.Ore, Clay=current_robots.Clay, Obsidian=current_robots.Obsidian, Geode=current_robots.Geode + 1)
            new_amounts = CollectedMaterials(Ore=new_ore - blueprint.GeodeRobot.Ore, Clay=new_clay, Obsidian=new_obsidian - blueprint.GeodeRobot.Obsidian, Geode=new_geode)
            current_search.append((time, new_robots, new_amounts, ()))

        if current_robots.Obsidian < blueprint.max_obsidian() and collected_amounts.Clay >= blueprint.ClayRobot.Clay and collected_amounts.Ore >= blueprint.ObsidianRobot.Ore and OBS not in did_not_build:
            can_build.append(OBS)
            new_robots = RobotFleet(Ore=current_robots.Ore, Clay=current_robots.Clay, Obsidian=current_robots.Obsidian + 1, Geode=current_robots.Geode)
            new_amounts = CollectedMaterials(Ore=new_ore - blueprint.ObsidianRobot.Ore, Clay=new_clay - blueprint.ObsidianRobot.Clay, Obsidian=new_obsidian, Geode=new_geode)
            current_search.append((time, new_robots, new_amounts, ()))

        if current_robots.Clay < blueprint.max_clay() and collected_amounts.Ore >= blueprint.ClayRobot.Ore and CLAY not in did_not_build:
            can_build.append(CLAY)
            new_robots = RobotFleet(Ore=current_robots.Ore, Clay=current_robots.Clay + 1, Obsidian=current_robots.Obsidian, Geode=current_robots.Geode)
            new_amounts = CollectedMaterials(Ore=new_ore - blueprint.ClayRobot.Ore, Clay=new_clay, Obsidian=new_obsidian, Geode=new_geode)
            current_search.append((time, new_robots, new_amounts, ()))

        if current_robots.Ore < blueprint.max_ore() and collected_amounts.Ore >= blueprint.OreRobot.Ore and ORE not in did_not_build:
            can_build.append(ORE)
            new_robots = RobotFleet(Ore=current_robots.Ore + 1, Clay=current_robots.Clay, Obsidian=current_robots.Obsidian, Geode=current_robots.Geode)
            new_amounts = CollectedMaterials(Ore=new_ore - blueprint.OreRobot.Ore, Clay=new_clay, Obsidian=new_obsidian, Geode=new_geode)
            current_search.append((time, new_robots, new_amounts, ()))

        if (current_robots.Ore and collected_amounts.Obsidian < blueprint.max_obsidian()) or (current_robots.Clay and collected_amounts.Clay < blueprint.max_clay()) or collected_amounts.Ore < blueprint.max_ore():
            new_robots = RobotFleet(Ore=current_robots.Ore, Clay=current_robots.Clay, Obsidian=current_robots.Obsidian, Geode=current_robots.Geode)
            new_amounts = CollectedMaterials(Ore=new_ore, Clay=new_clay, Obsidian=new_obsidian, Geode=new_geode)
            current_search.append((time, new_robots, new_amounts, ()))

    return best


if __name__ == '__main__':
    data = [
        'Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.',
        'Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.'
    ]
    # data = get_data(day=19, year=2022).splitlines()

    blueprints = parse_blueprints(data)

    for blueprint in blueprints:
        current_robots = RobotFleet(Ore=1, Clay=0, Obsidian=0, Geode=0)
        collected_amounts = CollectedMaterials(Ore=0, Clay=0, Obsidian=0, Geode=0)
        build_result = search(24, blueprint, current_robots, collected_amounts)

    # current_cubes = read_cubes(data)
    # print(f'Part 1: {part1(current_cubes)}')
