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


def horizontal_reflection(input, debug=False):
    '''Check for horizontal reflections'''
    rows_above = []
    for bl_nr, block in enumerate(input):
        changed = False
        for idx, _ in enumerate(block):
            if idx > 0:
                if block[idx] == block[idx - 1]:
                    mirror_index = idx
                    space_below = len(block) - idx
                    if space_below < idx:
                        rng = space_below
                    else:
                        rng = idx
                    for i in range(1, rng):
                        if block[idx - i - 1] == block[idx + i] and not changed:
                            reflection = True
                        else:
                            reflection = False
                            changed = True
                    if reflection:
                        rows_above.append(mirror_index)
                        if debug:
                            print(
                                'Horizontal reflection in block', bl_nr, 
                                'between rows', mirror_index - 1, 
                                'and', mirror_index,
                                '\n'
                            )
    return rows_above


def vertical_reflection(input, debug=False):
    '''Check for vertical reflections'''
    # Rotate input so columns become rows
    rotated_input = []
    for block in input:
        new_block = []
        for idx in range(0, len(block[0])):
            line = ''
            for row in block:
                line = line + row[idx]
            new_block.append(line)
        rotated_input.append(new_block)
    if debug:
        print('The rotated input:\n')
        pprint(rotated_input)
        print('')
    # Reuse horizontal reflection code 
    # (could call it on rotated_input but then the debug message would be 
    # all wrong)
    rows_above = []
    for bl_nr, block in enumerate(rotated_input):
        changed = False
        for idx, _ in enumerate(block):
            if idx > 0:
                if block[idx] == block[idx - 1]:
                    mirror_index = idx
                    space_below = len(block) - idx
                    if space_below < idx:
                        rng = space_below
                    else:
                        rng = idx
                    for i in range(1, rng):
                        if block[idx - i - 1] == block[idx + i] and not changed:
                            reflection = True
                        else:
                            reflection = False
                            changed = True
                    if reflection:
                        rows_above.append(mirror_index)
                        if debug:
                            print(
                                'Vertical reflection in block', bl_nr, 
                                'between columns', mirror_index - 1, 
                                'and', mirror_index,
                                '\n'
                            )
    return rows_above


def part_1(input, debug=False):
    '''Solve Part 1'''
    rows_above = horizontal_reflection(input, debug)
    rows_left = vertical_reflection(input, debug)
    if debug:
        print('Rows above:\n')
        pprint(rows_above)
        print('')
        print('Columns left:\n')
        pprint(rows_left)
        print('')
    summary = 0
    while rows_left:
        summary += rows_left.pop()
    while rows_above:
        summary += rows_above.pop() * 100
    return summary


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
