import types
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


def parse_round(input_line: str) -> Round:
    player1, player2 = parse('{} {}', input_line)
    return Round(player1, player2)


def player_action(input_round: Round) -> (PlayerAction, PlayerAction):
    actions = { 'A': PlayerAction.Rock, 'X': PlayerAction.Rock, 'B': PlayerAction.Paper, 'Y': PlayerAction.Paper, 'C': PlayerAction.Scissors, 'Z': PlayerAction.Scissors }
    return actions[input_round.Player1Action], actions[input_round.Player2Action]


def player_result(result_round: Round) -> (PlayerAction, PlayerAction):
    player1_action = {'A': PlayerAction.Rock, 'B': PlayerAction.Paper, 'C': PlayerAction.Scissors }.get(result_round.Player1Action)
    player2_result = { 'X': Result.Loss, 'Y': Result.Tie, 'Z': Result.Win }.get(result_round.Player2Action)

    if player2_result == Result.Tie:
        player2_action = player1_action
        return player1_action, player2_action
    if player2_result == Result.Win:
        match player1_action:
            case PlayerAction.Rock:
                player2_action = PlayerAction.Paper
            case PlayerAction.Paper:
                player2_action = PlayerAction.Scissors
            case PlayerAction.Scissors:
                player2_action = PlayerAction.Rock
        return player1_action, player2_action
    if player2_result == Result.Loss:
        match player1_action:
            case PlayerAction.Rock:
                player2_action = PlayerAction.Scissors
            case PlayerAction.Paper:
                player2_action = PlayerAction.Rock
            case PlayerAction.Scissors:
                player2_action = PlayerAction.Paper
        return player1_action, player2_action


def play_round_part(player1_action: PlayerAction, player2_action: PlayerAction) -> Score:
    if player1_action == player2_action:
        return Score(player1_action.value + Result.Tie.value, player2_action.value + Result.Tie.value)
    if player1_action == PlayerAction.Rock and player2_action == PlayerAction.Scissors:
        return Score(player1_action.value + Result.Win.value, player2_action.value)
    if player1_action == PlayerAction.Scissors and player2_action == PlayerAction.Paper:
        return Score(player1_action.value + Result.Win.value, player2_action.value)
    if player1_action == PlayerAction.Paper and player2_action == PlayerAction.Rock:
        return Score(player1_action.value + Result.Win.value, player2_action.value)
    else:
        return Score(player1_action.value, player2_action.value + Result.Win.value)

def play_game(rounds: list[Round], run_round_fn: types.FunctionType) -> Game:
    round_scores = Game()
    for current_round in rounds:
        player1, player2 = run_round_fn(current_round)
        completed_round = play_round_part(player1, player2)
        round_scores.Player1.append(completed_round.Player1Points)
        round_scores.Player2.append(completed_round.Player2Points)

    return round_scores

if __name__ == '__main__':
    data = ['A Y', 'B X', 'C Z']
    data = get_data(day=2, year=2022).splitlines()
    parsed_rounds = [parse_round(input_line) for input_line in data]

    part1_game = play_game(parsed_rounds, player_action)
    print(f'Part 1: {sum(part1_game.Player2)}')

    part2_game = play_game(parsed_rounds, player_result)
    print(f'Part 2: {sum(part2_game.Player2)}')