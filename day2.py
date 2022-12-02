from aocd import get_data
from dataclasses import dataclass
from parse import parse
from enum import Enum

class Result(Enum):
    Win = 6
    Loss = 0
    Tie = 3


class PlayerAction(Enum):
    Rock = 1
    Paper = 2
    Scissors = 3

@dataclass
class Score:
    Player1Points: int
    Player2Points: int

@dataclass
class Round:
    Player1Action: str
    Player2Action: str

def parse_round(input: str) -> Round:
    player1, player2 = parse('{} {}', input)
    return Round(player1, player2)



player1_action = {
    'A': PlayerAction.Rock,
    'B': PlayerAction.Paper,
    'C': PlayerAction.Scissors
}

player2_action = {
    'X': PlayerAction.Rock,
    'Y': PlayerAction.Paper,
    'Z': PlayerAction.Scissors
}

player2_result = {
    'X': Result.Loss,
    'Y': Result.Tie,
    'Z': Result.Win
}


def play_round_part1(current: Round) -> Score:
    player1_points = player1_action[current.Player1Action]
    player2_points = player2_action[current.Player2Action]
    if player1_points == player2_points:
        return Score(player1_points.value + Result.Tie.value, player2_points.value + Result.Tie.value)
    if player1_points == PlayerAction.Rock and player2_points == PlayerAction.Scissors:
        return Score(player1_points.value + Result.Win.value, player2_points.value)
    if player1_points == PlayerAction.Scissors and player2_points.value == PlayerAction.Paper:
        return Score(player1_points.value + Result.Win.value, player2_points.value)
    if player1_points == PlayerAction.Paper and player2_points == PlayerAction.Rock:
        return Score(player1_points.value + Result.Win.value, player2_points.value)
    else:
        return Score(player1_points.value, player2_points.value + Result.Win.value)


def play_round_part2(current: Round) -> Score:
    player1_points = player1_action[current.Player1Action]
    player_result_intention = player2_result[current.Player2Action]

    if player_result_intention == Result.Tie:
        return Score(player1_points.value + Result.Tie.value, player1_points.value + Result.Tie.value)
    if player_result_intention == Result.Win:
        if current.Player1Action == 'A':
            return Score(player1_points.value, player2_action['Y'].value + Result.Win.value)
        if current.Player1Action == 'B':
            return Score(player1_points.value, player2_action['Z'].value + Result.Win.value)
        if current.Player1Action == 'C':
            return Score(player1_points.value, player2_action['X'].value + Result.Win.value)
    if player_result_intention == Result.Loss:
        if current.Player1Action == 'A':
            return Score(player1_points.value + Result.Win.value, player2_action['Z'].value)
        if current.Player1Action == 'B':
            return Score(player1_points.value + Result.Win.value, player2_action['X'].value)
        if current.Player1Action == 'C':
            return Score(player1_points.value + Result.Win.value, player2_action['Y'].value)


if __name__ == '__main__':
    #data = ['A Y', 'B X', 'C Z']
    data = get_data(day=2, year=2022).splitlines()

    round_scores_part1 = {
        'player1': [],
        'player2': []
    }

    round_scores_part2 = {
        'player1': [],
        'player2': []
    }

    for input_line in data:
        current_round = parse_round(input_line)
        round_score_part1 = play_round_part1(current_round)
        round_scores_part1['player1'].append(round_score_part1.Player1Points)
        round_scores_part1['player2'].append(round_score_part1.Player2Points)

        round_score_part2 = play_round_part2(current_round)
        round_scores_part2['player1'].append(round_score_part2.Player1Points)
        round_scores_part2['player2'].append(round_score_part2.Player2Points)
        # print(current_round)

    print(f'Part 1: {sum(round_scores_part1["player2"])}')
    print(f'Part 2: {sum(round_scores_part2["player2"])}')
