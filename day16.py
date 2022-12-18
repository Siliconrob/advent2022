import itertools
from collections import deque
from dataclasses import dataclass, field
import networkx
import networkx as nx
from networkx import DiGraph, Graph
from parse import parse
from aocd import get_data
from ordered_set import OrderedSet

@dataclass(frozen=True, kw_only=True)
class OpenValve:
    Id: str
    Minute: int

@dataclass
class Valve:
    Id: str
    FlowRate: int



if __name__ == '__main__':
    data = [
        'Valve AA has flow rate=0; tunnels lead to valves DD, II, BB',
        'Valve BB has flow rate=13; tunnels lead to valves CC, AA',
        'Valve CC has flow rate=2; tunnels lead to valves DD, BB',
        'Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE',
        'Valve EE has flow rate=3; tunnels lead to valves FF, DD',
        'Valve FF has flow rate=0; tunnels lead to valves EE, GG',
        'Valve GG has flow rate=0; tunnels lead to valves FF, HH',
        'Valve HH has flow rate=22; tunnel leads to valve GG',
        'Valve II has flow rate=0; tunnels lead to valves AA, JJ',
        'Valve JJ has flow rate=21; tunnel leads to valve II'
    ]

    # data = get_data(day=16, year=2022).splitlines()

    all_valves = {}
    G = Graph()

    for input_line in data:
        valve_line, tunnel_line = parse("{}; {}", input_line)
        id, rate = parse('Valve {} has flow rate={:d}', valve_line)
        all_valves[id] = rate
        spaces = [index for index, the_char in enumerate(tunnel_line) if the_char == " "]
        for identifier in tunnel_line[spaces[3] + 1:].split(', '):
            G.add_edge(id, identifier, weight=1)

    #target_valves = sorted(filter(lambda x: x.FlowRate > 0, all_valves), key=lambda x: x.FlowRate, reverse=True)
    #target_values = list(filter(lambda x: x.get() > 0, all_valves))

    target_values = list(filter(lambda x: x is not None, [key if value > 0 else None for key, value in all_valves.items()]))



    #valves_to_open = list(map(lambda z: z.Id, filter(lambda x: x.FlowRate > 0, all_valves)))
    #valves_to_open.append('AA')

    #combinations = itertools.combinations(valves_to_open, 2)
    #for source, target in combinations:
    #    print(f'{source} {target}')

    paths = dict(nx.all_pairs_shortest_path_length(G))

    valid_max = 0

    for permutation in itertools.permutations(target_values, len(target_values)):
        current = 'AA'
        flow = deque(permutation)
        minutes = 30
        sums = []
        while flow and minutes > 0:
            target = flow.popleft()
            path_length = paths[current][target]
            minutes = minutes - path_length - 1
            sums.append(minutes * all_valves[target])
            current = target
        if minutes >= 0:
            set_max = sum(sums)
            if set_max > valid_max:
                valid_max = set_max
                print(f'{permutation} completed {valid_max}')
        else:

            set_max = sum(sums[:-1])
            if set_max > valid_max:
                valid_max = set_max
                print(f'{permutation} completed {valid_max}')
    print(valid_max)

    # path = dict(networkx.all_shortest_paths(G, 'AA'))
    # print(path)

    #path = networkx.approximation.steiner_tree(G, valves_to_open, weight=30)

    # path = networkx.shortest_path(G, 'AA', 'HH')
    #
    # path_distances = {}
    # path = dict(networkx.all_pairs_shortest_path_length(G, 30))
    # print(path)
    #      path_distances[id] = path_lengths
    #      print(path_lengths)
    #
    #
    # print(path_distances)
    #
    #
    # open_valves = OrderedSet()
    #
    # current_node = 'AA'
    #
    # target_valves = valves_to_open.copy()
    # minute = 0
    # while minute < 30:
    #     if len(open_valves) == len(valves_to_open):
    #         break
    #     nx.shortest_path(G, current_node, target_valves.pop())
    #
    # # for minute in range(0, 30):
    # #     if m
    # #     nx.shortest_path(G, current_node, current.)
    #
    #
    #     print(minute)






    #
    # for target in target_valves:
    #     path = networkx.shortest_path(G,'AA', target.Id)
    #     possible_max = (30 - len(path)) * target.FlowRate
    #     print(f'{target.Id}: {possible_max} {path}')
    #
    # for target in target_valves:
    #     path = networkx.shortest_path(G, 'DD', target.Id)
    #     possible_max = (30 - len(path)) * target.FlowRate
    #     print(f'{target.Id}: {possible_max} {path}')
    #
    #     #print(networkx.shortest_path(G, 'AA', 'HH'))



    # all_computed_paths = {}
    # for path in networkx.all_pairs_shortest_path_length(G):
    #     print(path)



