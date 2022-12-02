from aocd import get_data
from dataclasses import dataclass, field
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
class Game:
    Player1: list[Score] = field(default_factory=list)
    Player2: list[Score] = field(default_factory=list)


@dataclass
class Round:
    Player1Action: str
    Player2Action: str


def parse_round(input: str) -> Round:
    player1, player2 = parse('{} {}', input)
    return Round(player1, player2)


def player_action(input: Round):
    actions = {
        'A': PlayerAction.Rock,
        'X': PlayerAction.Rock,
        'B': PlayerAction.Paper,
        'Y': PlayerAction.Paper,
        'C': PlayerAction.Scissors,
        'Z': PlayerAction.Scissors,
    }

    return actions[input.Player1Action], actions[input.Player2Action]


def player_result(input: Round):
    actions = {
        'A': PlayerAction.Rock,
        'X': Result.Loss,
        'B': PlayerAction.Paper,
        'Y': Result.Tie,
        'C': PlayerAction.Scissors,
        'Z': Result.Win,
    }

    player1_action = actions[input.Player1Action]
    player2_result = actions[input.Player2Action]

    if player2_result == Result.Tie:
        player2_action = player1_action
    if player2_result == Result.Win:
        if player1_action == PlayerAction.Rock:
            player2_action = PlayerAction.Paper
        if player1_action == PlayerAction.Paper:
            player2_action = PlayerAction.Scissors
        if player1_action == PlayerAction.Scissors:
            player2_action = PlayerAction.Rock
    if player2_result == Result.Loss:
        if player1_action == PlayerAction.Rock:
            player2_action = PlayerAction.Scissors
        if player1_action == PlayerAction.Paper:
            player2_action = PlayerAction.Rock
        if player1_action == PlayerAction.Scissors:
            player2_action = PlayerAction.Paper
    return player1_action, player2_action


def play_round_part(player1_points: PlayerAction, player2_points: PlayerAction) -> Score:
    if player1_points == player2_points:
        return Score(player1_points.value + Result.Tie.value, player2_points.value + Result.Tie.value)
    if player1_points == PlayerAction.Rock and player2_points == PlayerAction.Scissors:
        return Score(player1_points.value + Result.Win.value, player2_points.value)
    if player1_points == PlayerAction.Scissors and player2_points == PlayerAction.Paper:
        return Score(player1_points.value + Result.Win.value, player2_points.value)
    if player1_points == PlayerAction.Paper and player2_points == PlayerAction.Rock:
        return Score(player1_points.value + Result.Win.value, player2_points.value)
    else:
        return Score(player1_points.value, player2_points.value + Result.Win.value)


if __name__ == '__main__':
    data = ['A Y', 'B X', 'C Z']
    # data = get_data(day=3, year=2022).splitlines()

    round_scores_part1 = Game()
    round_scores_part2 = Game()

    for input_line in data:
        current_round = parse_round(input_line)
        player1, player2 = player_action(current_round)
        round_score_part1 = play_round_part(player1, player2)
        round_scores_part1.Player1.append(round_score_part1.Player1Points)
        round_scores_part1.Player2.append(round_score_part1.Player2Points)

        player1, player2 = player_result(current_round)
        round_score_part2 = play_round_part(player1, player2)
        round_scores_part2.Player1.append(round_score_part2.Player1Points)
        round_scores_part2.Player2.append(round_score_part2.Player2Points)
        # print(current_round)

    print(f'Part 1: {sum(round_scores_part1.Player2)}')
    print(f'Part 2: {sum(round_scores_part2.Player2)}')
