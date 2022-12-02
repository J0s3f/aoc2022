import re
from enum import Enum


class Move(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @staticmethod
    def from_first(first: str):
        match first:
            case 'A':
                return Move.ROCK
            case 'B':
                return Move.PAPER
            case 'C':
                return Move.SCISSORS
        raise "No match"

    @staticmethod
    def from_second(second: str):
        match second:
            case 'X':
                return Move.ROCK
            case 'Y':
                return Move.PAPER
            case 'Z':
                return Move.SCISSORS
        raise "No match"

    @staticmethod
    def calc(opponent, outcome):
        match outcome:
            case Outcome.DRAW:
                return opponent
            case Outcome.WON:
                match opponent:
                    case Move.PAPER:
                        return Move.SCISSORS
                    case Move.ROCK:
                        return Move.PAPER
                    case Move.SCISSORS:
                        return Move.ROCK
            case Outcome.LOST:
                match opponent:
                    case Move.PAPER:
                        return Move.ROCK
                    case Move.ROCK:
                        return Move.SCISSORS
                    case Move.SCISSORS:
                        return Move.PAPER
        raise "No Match"


class Outcome(Enum):
    LOST = 0
    WON = 6
    DRAW = 3

    @staticmethod
    def from_second(second: str):
        match second:
            case 'X':
                return Outcome.LOST
            case 'Y':
                return Outcome.DRAW
            case 'Z':
                return Outcome.WON
        raise "No match"

    @staticmethod
    def calc(opponent, own):
        if opponent == own:
            return Outcome.DRAW

        if (opponent == Move.ROCK and own == Move.SCISSORS) or (opponent == Move.SCISSORS and own == Move.PAPER) or (
                opponent == Move.PAPER and own == Move.ROCK):
            return Outcome.LOST

        if (own == Move.ROCK and opponent == Move.SCISSORS) or (own == Move.SCISSORS and opponent == Move.PAPER) or (
                own == Move.PAPER and opponent == Move.ROCK):
            return Outcome.WON


def part_one(strategies):
    decoded = [(Move.from_first(x[0]), Move.from_second(x[1])) for x in strategies]
    results = [(x[0], x[1], Outcome.calc(x[0], x[1])) for x in decoded]
    values = [x[1].value + x[2].value for x in results]
    return sum(values)


def part_two(strategies):
    decoded = [(Move.from_first(x[0]), Outcome.from_second(x[1])) for x in strategies]
    results = [(x[0], x[1], Move.calc(x[0], x[1])) for x in decoded]
    values = [x[1].value + x[2].value for x in results]
    return sum(values)


with open('./input', 'r') as file:
    lines = file.readlines()
    strategies = [re.split(r"\W+", x.strip()) for x in lines]

    print('Part one: ', part_one(strategies))
    print('Part two: ', part_two(strategies))
