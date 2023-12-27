#!/usr/bin/env python

import argparse
from dataclasses import dataclass
from enum import Enum
from pprint import pprint
import sys
from typing import Literal


GridPoint = tuple[int, int]
Rotation = Literal['CCW', 'CW']


class Direction(Enum):
    
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    

    @staticmethod
    def rotate(facing: 'Direction', towards: Rotation) -> 'Direction':
        offset = 1 if towards == 'CW' else -1
        return Direction((facing.value + offset) % 4)


OFFSETS: dict[Direction, GridPoint] = {
    Direction.UP: (-1, 0),
    Direction.RIGHT: (0, 1),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
}


GRID_SIZE: int = 0


def parse_input(filename, debug=False):
    '''Parse the input file'''
    # Parsing the grid into a dict where each key is a 2-tuple of (row, col)
    # and the value is the character in that location
    global GRID_SIZE
    parsed_input = {} 
    with open(filename, 'r') as f:
        raw_input = f.read().splitlines()
        if debug:
            print('The raw input is:\n')
            pprint(raw_input)
            print('')
    assert len(raw_input) == len(raw_input[0]), "NOT A SQUARE GRID!!!"
    GRID_SIZE = len(raw_input)
    for row, line in enumerate(raw_input):
        for col, char in enumerate(line):
            parsed_input[row, col] = char
    return parsed_input


def addPoints(x: GridPoint, y: GridPoint) -> GridPoint:
    '''Add two 2-tuples together'''
    return x[0] + y[0], x[1] + y[1]


@dataclass(frozen=True)
class State:
    '''Class representing our current state'''
    
    loc: GridPoint
    facing: Direction


    @property
    def next_loc(self) -> GridPoint:
        '''Get the next location'''
        return addPoints(self.loc, OFFSETS[self.facing])


    def step(self) -> 'State':
        '''Step through the grid'''
        return State(self.next_loc, self.facing)


    def rotateAndStep(self, towards: Rotation) -> 'State':
        '''Rotate and step forward so we do not rotate endlessly'''
        return State(self.loc, Direction.rotate(self.facing, towards)).step()


    def getNextStates(self, char: str) -> list['State']:
        '''Get the next states based on char and give back a list of them'''
        match char:
            case '.':
                return [self.step()]
            case '-' if self.facing in (Direction.LEFT, Direction.RIGHT):
                return [self.step()]
            case '|' if self.facing in (Direction.UP, Direction.DOWN):
                return [self.step()]
            case '/' if self.facing in (Direction.LEFT, Direction.RIGHT):
                return [self.rotateAndStep('CCW')]
            case '/' if self.facing in (Direction.UP, Direction.DOWN):
                return [self.rotateAndStep('CW')]
            case '\\' if self.facing in (Direction.LEFT, Direction.RIGHT):
                return [self.rotateAndStep('CW')]
            case '\\' if self.facing in (Direction.UP, Direction.DOWN):
                return [self.rotateAndStep('CCW')]
            case '-' | '|':
                return [
                    self.rotateAndStep('CW'),
                    self.rotateAndStep('CCW'),
                ]
            case _:
                raise ValueError(
                    f'Unable to calculate next step from {self} and {char=}'
                )


class Grid:
    '''Class representing the grid'''
    
    grid: dict
    seen: set[State]
    queue: list[State]


    def traceLightPath(self, grid: dict, start: State) -> int:
        self.grid = grid
        self.seen = set()
        self.queue = [start]
        while self.queue:
            current = self.queue.pop()
            if current in self.seen:
                continue
            self.seen.add(current)
            for next_state in current.getNextStates(self.grid[current.loc]):
                if next_state.loc in self.grid:
                    self.queue.append(next_state)
        return len({state.loc for state in self.seen})


def part_1(input, debug=False):
    '''Solve Part 1'''
    grid = Grid()
    return grid.traceLightPath(input, State((0, 0), Direction.RIGHT))


def part_2(input, debug=False):
    '''Solve Part 2'''
    grid_size = GRID_SIZE
    grid = Grid()
    return max(
        *(
            grid.traceLightPath(input, State((0, col), Direction.DOWN))
            for col in range(grid_size)
        ),
        *(
            grid.traceLightPath(input, State((grid_size - 1, col), Direction.UP))
            for col in range(grid_size)
        ),
        *(
            grid.traceLightPath(input, State((row, 0), Direction.RIGHT))
            for row in range(grid_size)
        ),
        *(
            grid.traceLightPath(input, State((row, grid_size - 1), Direction.LEFT))
            for row in range(grid_size)
        ),
    )


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
