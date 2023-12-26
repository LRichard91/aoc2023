#!/usr/bin/env python

import argparse
from functools import cache
from pprint import pprint
import sys


CUBES = []
ROLLED = []
PREV_STATES = []
LEN_X = 0
LEN_Y = 0


def parse_input(filename, debug=False):
    '''Parse the input file'''
    parsed_input = {'round': [], 'cube': [], 'length': 0}
    with open(filename, 'r') as f:
        input = f.read().splitlines()
    if debug:
        print('The raw input:\n')
        pprint(input)
        print('')
    parsed_input['length_y'] = len(input)
    parsed_input['length_x'] = len(input[0])
    for y, line in enumerate(input):
        for x, char in enumerate(line):
            if char == 'O':
                parsed_input['round'].append((x, y))
            elif char == '#':
                parsed_input['cube'].append((x, y))
            else:
                continue
    return parsed_input


def tilt_platform(positions, debug=False):
    '''Tilt the platform and recalculate rounded rock positions -- for Part 1'''
    rolled = []
    for rock in positions['round']:
        x, y = rock[0], rock[1] 
        while True:
            if y == -1:
                break
            elif (x, y) in rolled:
                break
            elif (x, y) in positions['cube']:
                break
            y -= 1
        rolled.append((x, y + 1))
        if debug:
            print('For round rock', rock, 'the new position:', (x, y + 1))
    return rolled


def calculate_load(positions, length, debug=False):
    '''Calculate the load on the north support beam'''
    load = 0
    for rock in positions['round']:
        load += length - rock[1]
    return load


def part_1(input, debug=False):
    '''Solve Part 1'''
    new_positions = {}
    new_positions['cube'] = input['cube'].copy()
    new_positions['round'] = tilt_platform(input, debug)
    if debug:
        print('The new positions:\n')
        pprint(new_positions)
        print('')
    return calculate_load(new_positions, input['length_y'], debug)


def move_rock(rock, direction, debug=False):
    '''Move a round rock in the direction given'''
    if rock in CUBES or rock in ROLLED:
        if debug:
            if rock in CUBES:
                print('Hit cube rock at position:', rock)
            elif rock in ROLLED:
                print('Hit previously rolled rock at position:', rock)
        if direction == 'N':
            return (rock[0], rock[1] + 1)
        elif direction == 'W':
            return (rock[0] + 1, rock[1])
        elif direction == 'S':
            return (rock[0], rock[1] - 1)
        elif direction == 'E':
            return (rock[0] - 1, rock[1])
    elif (direction == 'W' and rock[0] == 0) or (direction == 'E' and rock[0] == LEN_X):
        return rock
    elif (direction == 'N' and rock[1] == 0) or (direction == 'S' and rock[1] == LEN_Y):
        return rock
    if direction == 'N':
        return move_rock((rock[0], rock[1] - 1), 'N')
    elif direction == 'W':
        return move_rock((rock[0] - 1, rock[1]), 'W')
    elif direction == 'S':
        return move_rock((rock[0], rock[1] + 1), 'S')
    elif direction == 'E':
        return move_rock((rock[0] + 1, rock[1]), 'E')


def rotate_platform(positions, debug=False):
    '''Rotate platform north-west-south-east - for Part 2'''
    global ROLLED
    global PREV_STATES
    new_positions = positions.copy()
    for direction in ['N', 'W', 'S', 'E']:
        for idx, rock in enumerate(new_positions):
            new_pos = move_rock(rock, direction, debug)
    for rock in positions:
        new_pos = move_rock(rock, 'N', debug)
        new_positions.append(new_pos)
        ROLLED.append(new_pos)
        if debug:
            print(new_pos)
            print('The list of new positions:', ROLLED)
    PREV_STATES.append(new_positions)
    return new_positions


def part_2(input, debug=False):
    '''Solve Part 2'''
    global CUBES
    global LEN_X
    global LEN_Y
    CUBES = input['cube'].copy()
    LEN_X = input['length_x']
    LEN_Y = input['length_y']
    positions = input['round'].copy()
    new_positions = rotate_platform(positions, debug)
    if debug:
        print('New positions:\n')
        print(new_positions)
        print('')
    final_positions = {}
    final_positions['round'] = new_positions
    return calculate_load(final_positions, LEN_Y, debug)


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
