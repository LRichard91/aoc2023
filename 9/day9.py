#!/usr/bin/env python

import argparse
from pprint import pprint
import sys


def parse_input(filename, debug=False):
    '''Parse the input file'''
    with open(filename, 'r') as f:
        input = f.read().splitlines()
        if debug:
            print('The raw input:\n')
            pprint(input)
            print('')

    parsed_input = []
    for line in input:
        parsed_input.append([int(item) for item in line.split(' ')])

    return parsed_input


def extrapolate(lst, debug=False):
    '''Extrapolate the next value in the list'''
    if all(x == 0 for x in lst):
        if debug:
            print('\nAll nulls!\n')
        return 0
    delta = [lst[i + 1] - lst[i] for i in range(len(lst) - 1)]
    if debug:
        print('Delta:')
        pprint(delta)
    return lst[-1] + extrapolate(delta, debug)


def part_1(input, debug=False):
    '''Solve Part 1'''
    next_values = []
    for item in input:
        if debug:
            print('\nThe list we\'re working on:\n')
            pprint(item)
            print('')
        next_value = extrapolate(item, debug)
        next_values.append(next_value)
        if debug:
            print('\nThe next value:', next_value, '\n')
            print('The list of next values:\n')
            pprint(next_values)
            print('')

    return sum(next_values)


def part_2(input, debug=False):
    '''Solve Part 2'''
    next_values = []
    for item in input:
        if debug:
            print('\nThe list we\'re working on:\n')
            pprint(item)
            print('')
        item.reverse()
        next_value = extrapolate(item, debug)
        next_values.append(next_value)
        if debug:
            print('\nThe next value:', next_value, '\n')
            print('The list of next values:\n')
            pprint(next_values)
            print('')

    return sum(next_values)


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
