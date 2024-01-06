#!/usr/bin/env python

import argparse
from pprint import pprint
import sys
from typing import Any, NamedTuple


Brick = NamedTuple(
    'Brick',
    [
        ('x', int),
        ('y', int),
        ('z', int),
        ('x_', int),
        ('y_', int),
        ('z_', int),
    ],
)


def parse_input(filename: str, debug: bool=False) -> Any:
    '''Parse the input file'''
    parsed_input: dict[int, Brick] = {}
    with open(filename, 'r') as f:
        raw_input = f.read().splitlines()

    if debug:
        print('The raw input:\n')
        pprint(raw_input)
        print('')

    bricks: list[Brick] = []
    for line in raw_input:
        start, end = line.split('~')
        x, y, z = start.split(',')
        x_, y_, z_ = end.split(',')
        bricks.append(
            Brick(
                int(x),
                int(y),
                int(z),
                int(x_),
                int(y_),
                int(z_)
            )
        )
    bricks.sort(key=lambda a: a.z, reverse=False)

    if debug:
        print('The list of bricks:\n')
        pprint(bricks)
        print('')

    for i in range(len(bricks)):
        parsed_input[i + 1] = bricks[i]

    return parsed_input


def part_1(input, debug: bool=False) -> int:
    '''Solve Part 1'''
    return 0


def part_2(input, debug: bool=False) -> int:
    '''Solve Part 2'''
    return 0


def main() -> None:
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
