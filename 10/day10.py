#!/usr/bin/env python

import argparse
from pprint import pprint
import sys


IN_PATH = []
INSIDE = []

def parse_input(filename, debug=False):
    '''Parse the input file'''
    parsed_input = []
    global IN_PATH
    global INSIDE
    with open(filename, 'r') as f:
        input = f.read().splitlines()
        if debug:
            print('The raw input:\n')
            pprint(input)
            print('')

    for line in input:
        parsed_input.append([list(char) for char in line])
        IN_PATH.append([False for _ in line])
        INSIDE.append([False for _ in line])

    return parsed_input


def find_start(input, debug=False):
    '''Find the starting position'''
    global IN_PATH
    for i, line in enumerate(input):
        for j, char in enumerate(line):
            if char == ['S']:
                IN_PATH[i][j] = True
                if debug:
                    print('The starting position is:', (i, j), '\n')
                return (i, j)

def get_first_direction(input, starting_pos):
    '''Get the first node after start'''
    global IN_PATH
    if input[starting_pos[0] - 1][starting_pos[1]] in [['|'], ['7'], ['F']]:
        next_node = (starting_pos[0] - 1, starting_pos[1])
        direction = 'U'
        IN_PATH[starting_pos[0] - 1][starting_pos[1]] = True
    elif input[starting_pos[0] + 1][starting_pos[1]] in [['|'], ['J'], ['L']]:
        next_node = (starting_pos[0] + 1, starting_pos[1])
        direction = 'D'
        IN_PATH[starting_pos[0] + 1][starting_pos[1]] = True
    elif input[starting_pos[0]][starting_pos[1] - 1] in [['-'], ['F'], ['L']]:
        next_node = (starting_pos[0], starting_pos[1] - 1)
        direction = 'L'
        IN_PATH[starting_pos[0]][starting_pos[1] - 1] = True
    elif input[starting_pos[0]][starting_pos[1] + 1] in [['-'], ['7'], ['J']]:
        next_node = (starting_pos[0], starting_pos[1] + 1)
        direction = 'R'
        IN_PATH[starting_pos[0]][starting_pos[1] + 1] = True
    return next_node, direction


def traverse_path(input, starting_pos, direction, steps, debug=False):
    '''Traverse the path'''
    if debug:
        print('Starting position:', starting_pos)

    # Horizontal pipe, coming from the left, continue to the right
    if input[starting_pos[0]][starting_pos[1]] == ['-'] and direction == 'R':
        next_node = (starting_pos[0], starting_pos[1] + 1)
        direction = 'R'
        steps += 1
        IN_PATH[starting_pos[0]][starting_pos[1] + 1] = True
    # Horizontal pipe, coming from the right, continue to the left
    elif input[starting_pos[0]][starting_pos[1]] == ['-'] and direction == 'L':
        next_node = (starting_pos[0], starting_pos[1] - 1)
        direction = 'L'
        steps += 1
        IN_PATH[starting_pos[0]][starting_pos[1] - 1] = True
    # Vertical pipe, coming from below, continue up
    elif input[starting_pos[0]][starting_pos[1]] == ['|'] and direction == 'U':
        next_node = (starting_pos[0] - 1, starting_pos[1])
        direction = 'U'
        steps += 1
        IN_PATH[starting_pos[0] - 1][starting_pos[1]] = True
    # Vertical pipe, coming from above, continue down
    elif input[starting_pos[0]][starting_pos[1]] == ['|'] and direction == 'D':
        next_node = (starting_pos[0] + 1, starting_pos[1])
        direction = 'D'
        steps += 1
        IN_PATH[starting_pos[0] + 1][starting_pos[1]] = True
    # Elbow pipe, S-E, coming from below, continue right
    elif input[starting_pos[0]][starting_pos[1]] == ['F'] and direction == 'U':
        next_node = (starting_pos[0], starting_pos[1] + 1)
        direction = 'R'
        steps += 1
        IN_PATH[starting_pos[0]][starting_pos[1] + 1] = True
    # Elbow pipe, S-E, coming from right, continue bottom
    elif input[starting_pos[0]][starting_pos[1]] == ['F'] and direction == 'L':
        next_node = (starting_pos[0] + 1, starting_pos[1])
        direction = 'D'
        steps += 1
        IN_PATH[starting_pos[0] + 1][starting_pos[1]] = True
    # Elbow pipe, N-E, coming from above, continue right
    elif input[starting_pos[0]][starting_pos[1]] == ['L'] and direction == 'D':
        next_node = (starting_pos[0], starting_pos[1] + 1)
        direction = 'R'
        steps += 1
        IN_PATH[starting_pos[0]][starting_pos[1] + 1] = True
    # Elbow pipe, N-E, coming from right, continue up
    elif input[starting_pos[0]][starting_pos[1]] == ['L'] and direction == 'L':
        next_node = (starting_pos[0] - 1, starting_pos[1])
        direction = 'U'
        steps += 1
        IN_PATH[starting_pos[0] - 1][starting_pos[1]] = True
    # Elbow pipe, S-W, comint from below, continue left
    elif input[starting_pos[0]][starting_pos[1]] == ['7'] and direction == 'U':
        next_node = (starting_pos[0], starting_pos[1] - 1)
        direction = 'L'
        steps += 1
        IN_PATH[starting_pos[0]][starting_pos[1] - 1] = True
    # Elbow pipe, S-W, coming from left, continue down
    elif input[starting_pos[0]][starting_pos[1]] == ['7'] and direction == 'R':
        next_node = (starting_pos[0] + 1, starting_pos[1])
        direction = 'D'
        steps += 1
        IN_PATH[starting_pos[0] + 1][starting_pos[1]] = True
    # Elbow pipe, N-W, coming from above, continue left
    elif input[starting_pos[0]][starting_pos[1]] == ['J'] and direction == 'D':
        next_node = (starting_pos[0], starting_pos[1] - 1)
        direction = 'L'
        steps += 1
        IN_PATH[starting_pos[0]][starting_pos[1] - 1] = True
    # Elbow pipe, N-W, coming from left, continue up
    elif input[starting_pos[0]][starting_pos[1]] == ['J'] and direction == 'R':
        next_node = (starting_pos[0] - 1, starting_pos[1])
        direction = 'U'
        steps += 1
        IN_PATH[starting_pos[0] - 1][starting_pos[1]] = True

    # Exit condition for the recursion
    if input[next_node[0]][next_node[1]] == ['S']:
        if debug:
            print('\nEnd found!\n')
        return steps

    if debug:
        print('Next node:', next_node, '\n')

    return traverse_path(input, next_node, direction, steps, debug)


def part_1(input, debug=False):
    '''Solve Part 1'''
    # Raise recursion depth limit
    sys.setrecursionlimit(20000)
    start = find_start(input, debug)
    starter = get_first_direction(input, start)
    next_node = starter[0]
    direction = starter[1]
    if debug:
        print('====================')
        print('        Path        ')
        print('====================')
        print('')
    steps = traverse_path(input, next_node, direction, 1, debug)
    return round(steps / 2)


# def ray_casting(input, debug=False):
#     '''Check if a tile is inside or outside of path'''
#     # Almost worked...
#     global IN_PATH
#     global INSIDE
#     for i, row in enumerate(input):
#         for j, _ in enumerate(row):
#             count = 0
#             switch = False
#             last = False
#             if not IN_PATH[i][j]:
#                 for k in range(j + 1, len(row)):
#                     if IN_PATH[i][k] and not last:
#                         count += 1
#                         last = True
#                     elif IN_PATH[i][k] and last:
#                         switch = True
#                     elif not IN_PATH[i][k] and last and switch:
#                         count += 1
#                         last = False
#                         switch = False
#                     elif not IN_PATH[i][k] and last:
#                         last = False
#             if debug:
#                 print('Count for row', i, 'tile', j, ':', count)
#             if count % 2 == 1:
#                 INSIDE[i][j] = True
#     inside_count = 0
#     for row in INSIDE:
#         inside_count += row.count(True)
#     return inside_count


def ray_casting_2(input, debug=False):
    '''Check if a tile is inside of path'''
    global INSIDE
    for i, row in enumerate(input):
        for j, _ in enumerate(row):
            count = 0
            if not IN_PATH[i][j]:
                for k in range(j + 1, len(row)):
                    if input[i][k] in [['|'], ['S'], ['7'], ['F'], ['J'], ['L']] and IN_PATH[i][k]:
                        count += 1
            if debug:
                print('Count for row', i, 'tile', j, ':', count)
            if count % 2 == 1:
                INSIDE[i][j] = True
    inside_count = 0
    for row in INSIDE:
        inside_count += row.count(True)
    return inside_count


def part_2(input, debug=False):
    '''Solve Part 2'''
    # Raise recursion depth limit
    sys.setrecursionlimit(20000)
    start = find_start(input, debug)
    starter = get_first_direction(input, start)
    next_node = starter[0]
    direction = starter[1]
    traverse_path(input, next_node, direction, 1, debug)
    if debug:
        print('Nodes in path:\n')
        pprint(IN_PATH, width=150)
        print('')
    # inside = ray_casting(input, debug)
    inside = ray_casting_2(input, debug)
    return inside


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
