#!/usr/bin/env python

import argparse
from pprint import pprint
import sys


def parse_input(filename, debug=False):
    '''Parse the input file'''
    parsed_input = []
    # Get the raw input
    with open(filename, 'r') as f:
        input = f.read().splitlines()
    if debug:
        print('The raw input:\n')
        pprint(input)
        print('')
    # Sanitize input by moving all patterns into separate lists
    temp_list = []
    for idx, line in enumerate(input):
        if line == '' or idx == len(input) - 1:
            if idx == len(input) - 1:
                temp_list.append(line)
            if debug:
                print('The temporary list:', temp_list, '\n')
            parsed_input.append(temp_list.copy())
            temp_list.clear()
        else:
            temp_list.append(line)
    return parsed_input


def horizontal_ref(block, smudge=0, debug=False):
    '''Check for reflection between rows'''
    for idx in range(len(block)):
        if idx == 0:
            continue
        if sum(smudges(before, after) for before, after in zip(reversed(block[:idx]), block[idx:])) == smudge:
            return idx
    return 0


def score_reflection(block, smudge=0, debug=False):
    '''Get score of the reflection on a block'''
    # Check horizontal reflection
    if debug:
        print('Checking for horizontal mirror')
    if mirror := horizontal_ref(block, smudge, debug):
        if debug:
            print('Found at row:', mirror)
        return 100 * mirror
    # Transpose block and check vertical reflection
    if debug:
        print('Checking for vertical mirror')
    if mirror := horizontal_ref(list(zip(*block)), smudge, debug):
        if debug:
            print('Found at column:', mirror)
        return mirror


def part_1(input, debug=False):
    '''Solve Part 1'''
    score = 0
    for bl_nr, block in enumerate(input):
        if debug:
            print('Processing block nr.', bl_nr)
        try:
            score += score_reflection(block, debug)
        except TypeError:
            pass
    return score


def smudges(before, after):
    '''Return the number of smudges needed for reflection'''
    return sum(a != b for a, b in zip(before, after))


def part_2(input, debug=False):
    '''Solve Part 2'''
    score = 0
    for bl_nr, block in enumerate(input):
        if debug:
            print('Processing block nr.', bl_nr)
        try:
            score += score_reflection(block, 1, debug)
        except TypeError:
            pass
    return score


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
