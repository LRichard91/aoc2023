#!/usr/bin/env python

import argparse
from itertools import groupby, product
from functools import cache
from pprint import pprint
import sys


def parse_input(filename, debug=False):
    '''Parse the input file'''
    parsed_input = {}
    with open(filename, 'r') as f:
        input = f.read().splitlines()
    if debug:
        print('The raw input:\n')
        pprint(input)
        print('')
    records = []
    alt_records = []
    for line in input:
        records.append(line.split(' ')[0])
        alt_records.append([int(x) for x in line.split(' ')[1].split(',')])
    if debug:
        print('The records:\n')
        pprint(records)
        print('')
        print('The alternate records:\n')
        pprint(alt_records)
        print('')
    parsed_input['rec'] = records
    parsed_input['alt'] = alt_records
    return parsed_input


def match(record, alt_record):
    '''Return true if possible combination matches the alternate record'''
    return alt_record == [
        sum(1 for _ in group)
        for key, group in groupby(record)
        if key == "#"
    ]


def part_1(input, debug=False):
    '''Solve Part 1'''
    all_combinations = []
    for idx, record in enumerate(input['rec']):
        generator = ("#." if letter == "?" else letter for letter in record)
        possible_combinations = sum(match(possible, input['alt'][idx]) for possible in product(*generator))
        if debug:
            print('The possible combinations for line nr.', idx, 'are:', possible_combinations, '\n')
        all_combinations.append(possible_combinations)
    if debug:
        print('\nAll possible combinations:\n')
        pprint(all_combinations)
        print('')
    return sum(all_combinations)


def unfold(input, debug=False):
    '''Return unfolded input'''
    unfolded_input = {'rec': [], 'alt': []}
    for record in input['rec']:
        unfolded_input['rec'].append(record + (("?" + record) * 4))
    if debug:
        print('The unfolded records:\n')
        pprint(unfolded_input['rec'])
        print('')
    for alt in input['alt']:
        unfolded_input['alt'].append(alt * 5)
    if debug:
        print('The unfolded alternate records:\n')
        pprint(unfolded_input['alt'])
        print('')
    return unfolded_input


def part_2(input, debug=False):
    '''Solve Part 2'''
    unfolded = unfold(input, debug)
    all_combinations = []
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
