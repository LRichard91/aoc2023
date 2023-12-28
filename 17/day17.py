#!/usr/bin/env python

import argparse
from enum import IntEnum
from heapq import heappop, heappush
from pprint import pprint
import sys
from typing import Literal, NamedTuple


GridPoint = tuple[int, int]
Rotation = Literal['CCW', 'CW']


class Direction(IntEnum):
    '''Class representing the directions and implementing rotation'''

    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    @staticmethod
    def rotate(facing: 'Direction', towards: Rotation) -> 'Direction':
        offset = 1 if towards == 'CW' else -1
        return Direction((facing.value + offset) % 4)

    @staticmethod
    def offset(facing: "Direction") -> GridPoint:
        return OFFSETS[facing]


OFFSETS: dict[Direction, GridPoint] = {
    Direction.UP: GridPoint((-1, 0)),
    Direction.RIGHT: GridPoint((0, 1)),
    Direction.DOWN: GridPoint((1, 0)),
    Direction.LEFT: GridPoint((0, -1)),
}


class Position(NamedTuple):
    loc: GridPoint
    facing: Direction

    @property
    def next_loc(self) -> GridPoint:
        return addPoints(self.loc, Direction.offset(self.facing))

    def step(self) -> "Position":
        return Position(self.next_loc, self.facing)

    def rotate_and_step(self, towards: Rotation):
        return Position(self.loc, Direction.rotate(self.facing, towards)).step()


State = tuple[int, Position, int]


def addPoints(x: GridPoint, y: GridPoint) -> GridPoint:
    '''Add two 2-tuples together'''
    return x[0] + y[0], x[1] + y[1]


END_NODE: tuple[int, int]


def parse_input(filename: str, debug: bool=False) -> dict:
    '''Parse the input file'''

    global END_NODE
    parsed_input = {}

    with open(filename, 'r') as f:
        raw = f.read().splitlines()
    
    if debug:
        print('The raw input is:\n')
        pprint(raw)
        print('')

    END_NODE = len(raw) - 1, len(raw[-1]) - 1

    if debug:
        print('The end node is:', END_NODE, '\n')

    for i, row in enumerate(raw):
        for j, weight in enumerate(row):
            parsed_input[i, j] = int(weight)

    return parsed_input


def part_1(input: dict, debug: bool=False) -> int:
    '''Solve Part 1'''
    queue: list[State] = [
        (0, Position((0, 0), Direction.DOWN), 0),
        (0, Position((0, 0), Direction.RIGHT), 0),
    ]
    seen: set[tuple[Position, int]] = set()

    while queue:
        cost, pos, num_steps = heappop(queue)

        if pos.loc == END_NODE:
            return cost
        
        if (pos, num_steps) in seen:
            continue

        seen.add((pos, num_steps))

        if (left := pos.rotate_and_step("CCW")).loc in input:
            heappush(queue, (cost + input[left.loc], left, 1))

        if (right := pos.rotate_and_step("CW")).loc in input:
            heappush(queue, (cost + input[right.loc], right, 1))

        if num_steps < 3 and (forward := pos.step()).loc in input:
            heappush(queue, (cost + input[forward.loc], forward, num_steps + 1))

    return 0


def part_2(input, debug=False):
    '''Solve Part 2'''
    return 0


def main():
    '''Main function'''
    arg_parser = argparse.ArgumentParser(
        description='Solves the puzzles for the given day of AOC'
    )
    arg_parser.add_argument(
        'filename', 
        help='The path to the input file'
    )
    arg_parser.add_argument(
        '-d',
        '--debug',
        dest='debug',
        action='store_true',
        help='Enables debug messages'
    )
    arg_parser.add_argument(
        '-1',
        '--part1',
        dest='part1',
        action='store_true',
        help='Executes the solution for Part 1'
    )
    arg_parser.add_argument(
        '-2',
        '--part2',
        dest='part2',
        action='store_true',
        help='Executes the solution for Part 2'
    )
    args = arg_parser.parse_args()

    if args.debug:
        print('')
        print('Debug messages are ON')
        print('')

    parsed_input = parse_input(args.filename, args.debug)

    if args.debug:
        print('The parsed input:')
        print('')
        pprint(parsed_input)
        print('')        

    if args.part1 and args.debug:
        print('======================================================')
        print('                        Part 1                        ')
        print('======================================================')
        print('')

    if args.part1:
        solution_1 = part_1(parsed_input, args.debug)
        print('')
        print('The solution for Part 1 is:', solution_1)
        print('')

    if args.part2 and args.debug:
        print('======================================================')
        print('                        Part 2                        ')
        print('======================================================')
        print('')

    if args.part2:
        solution_2 = part_2(parsed_input, args.debug)
        print('')
        print('The solution for Part 2 is', solution_2)
        print('')
        
    sys.exit(0)


if __name__ == "__main__":
    main()
