#!/usr/bin/env python

import argparse
from fractions import Fraction
from pprint import pprint
import sys
from typing import NamedTuple


Hailstone = NamedTuple(
    'Hailstone',
    [
        ('x', int),
        ('y', int),
        ('z', int),
        ('vx', int),
        ('vy', int),
        ('vz', int),
    ]
)


Intersection = NamedTuple(
    'Intersection',
    [
        ('Px', float),
        ('Py', float)
    ]
)


TEST_AREA = (7, 27)


def intersectLines2D(stones: dict[int, Hailstone], testArea: tuple[int, int], debug: bool=False) -> int:
    '''Line-line intersection for x-y coordinates'''
    intersectionsInTestArea: int = 0
    for currIdx, current in stones.items():
        for nextIdx, next in stones.items():
            parallel: bool = False
            pastCurrent: bool = False
            pastNext: bool = False
            outside: bool = False
            if nextIdx <= currIdx:
                continue
            dx = current.x - next.x
            dy = current.y - next.y
            if (denominator := current.vy * next.vx - current.vx * next.vy) == 0:
                parallel = True
            if not parallel:
                numerator = next.vy * dx - next.vx * dy
                if (tCurrent := Fraction(numerator, denominator)) <= 0:
                    pastCurrent = True
                numerator = current.vy * dx - current.vx * dy
                if (tNext := Fraction(numerator, denominator)) <= 0:
                    pastNext = True
                if not (testArea[0] <= (current.x + tCurrent * current.vx) <= testArea[1]):
                    outside = True
                if not (testArea[0] <= (current.y + tCurrent * current.vy) <= testArea[1]):
                    outside = True
            if not parallel and not pastCurrent and not pastNext and not outside:
                intersectionsInTestArea += 1
            if debug:
                if parallel:
                    print('Stones', currIdx, 'and', nextIdx, 'have parallel paths')
                elif pastCurrent and pastNext:
                    print('Stones', currIdx, 'and', nextIdx, 'have crossed paths in both their pasts')
                elif pastCurrent:
                    print('Stone', currIdx, 'and', nextIdx, 'crossed paths in the past for', currIdx)
                elif pastNext:
                    print('Stone', currIdx, 'and', nextIdx, 'crossed paths in the past for', nextIdx)
                elif outside:
                    print('Stones', currIdx, 'and', nextIdx, 'cross paths outside the test area')
                else:
                    print('Stones', currIdx, 'and', nextIdx, 'cross paths at: x=', float(next.x + tNext * next.vx), 'y=', float(next.y + tNext * next.vy))

    return intersectionsInTestArea


def parse_input(filename: str, debug: bool=False) -> dict[int, Hailstone]:
    '''Parse the input file'''
    parsed_input: dict[int, Hailstone] = {}
    rawInput: list[str] = []
    with open(filename, 'r') as f:
        rawInput = f.read().splitlines()
    if debug:
        print('The raw input:\n')
        pprint(rawInput)
        print('')
    for idx, line in enumerate(rawInput):
        position: str = line[:line.index('@') - 1]
        velocity: str = line[line.index('@') + 2:]
        x, y, z = tuple([int(num) for num in position.split(', ')])
        vx, vy, vz = tuple([int(num) for num in velocity.split(', ')])
        parsed_input[idx] = Hailstone(x, y, z, vx, vy, vz)
    return parsed_input


def part_1(input: dict[int, Hailstone], debug: bool=False) -> int:
    '''Solve Part 1'''
    crossInside = intersectLines2D(input, TEST_AREA, debug)
    return crossInside


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
