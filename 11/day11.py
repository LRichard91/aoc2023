#!/usr/bin/env python

import argparse
from itertools import combinations
from pprint import pprint
import sys


def parse_input(filename, debug=False):
    '''Parse the input file'''
    parsed_input = []
    with open(filename, 'r') as f:
        parsed_input = f.read().splitlines()
    return parsed_input


def expand_universe(input, debug=False):
    '''Expand the universe based on the gravitational rules'''
    empty_rows = []
    empty_columns = []
    for idx, line in enumerate(input):
        if line.count('.') == len(line):
            empty_rows.append(idx)
    for i in range(len(input[0])):
        empty = True
        for line in input:
            if line[i] != '.':
                empty = False
        if empty:
            empty_columns.append(i)
    if debug:
        print('Empty rows:', empty_rows, '\n')
        print('Empty columns:', empty_columns, '\n')
    expanded_universe = ['' for _ in input]
    while empty_columns:
        i = empty_columns.pop()
        for idx, line in enumerate(input):
            if expanded_universe[idx] == '':
                expanded_universe[idx] = line[:i] + '.' + line[i:]
            else:
                expanded_universe[idx] = expanded_universe[idx][:i] + '.' + expanded_universe[idx][i:]
    while empty_rows:
        i = empty_rows.pop()
        expanded_universe.insert(i, '.' * len(expanded_universe[0]))
    if debug:
        print('The expanded universe:\n')
        pprint(expanded_universe)
        print('')
    return expanded_universe


def get_galaxies(input, debug):
    '''Get the galaxies and their coordinates'''
    g_nr = 0
    galaxies = []
    for i, line in enumerate(input):
        for j, tile in enumerate(line):
            if tile == '#':
                g_nr += 1
                galaxies.append({'ID': g_nr, 'Coord': (i, j)})
    if debug:
        print('The Galaxies:\n')
        pprint(galaxies)
        print('')
    return galaxies


def get_pairs(galaxies, debug):
    '''Get the galaxy pairs'''
    pairs = combinations(galaxies, 2)
    if debug:
        print('The galaxy pairs:\n')
        for pair in pairs:
            print(pair)
        print('')
    return pairs


def part_1(galaxies, debug=False):
    '''Solve Part 1'''
    distances = []
    pairs = get_pairs(galaxies, debug=False)
    for pair in pairs:
        if debug:
            print('Galaxy', pair[0]['ID'], 'to galaxy', pair[1]['ID'])
            print('From coordinate', pair[0]['Coord'], 'to coordinate', pair[1]['Coord'])
        x_distance = abs(pair[0]['Coord'][1] - pair[1]['Coord'][1])
        y_distance = abs(pair[0]['Coord'][0] - pair[1]['Coord'][0])
        if debug:
            print('Distance x:', x_distance, 'Distance y:', y_distance, 'Total distance:', x_distance + y_distance)
        distances.append(x_distance + y_distance)
    if debug:
        print('The distances:\n')
        pprint(distances)
    return sum(distances)


def expand_universe_2(input, debug=False):
    '''Expand universe for Part 2'''
    empty_rows = []
    empty_columns = []
    for idx, line in enumerate(input):
        if line.count('.') == len(line):
            empty_rows.append(idx)
    for i in range(len(input[0])):
        empty = True
        for line in input:
            if line[i] != '.':
                empty = False
        if empty:
            empty_columns.append(i)
    if debug:
        print('Empty rows:', empty_rows, '\n')
        print('Empty columns:', empty_columns, '\n')
    empty = [empty_columns, empty_rows]
    return empty


def part_2(input, debug=False):
    '''Solve Part 2'''
    empty = expand_universe_2(input, debug)
    galaxies = get_galaxies(input, debug)
    for galaxy in galaxies:
        x_expansion = 0
        y_expansion = 0
        for column in empty[0]:
            if column in range(0, galaxy['Coord'][1]):
                if debug:
                    print('Empty column', column, 'before galaxy', galaxy)
                x_expansion += 999_999
        for row in empty[1]:
            if row in range(0, galaxy['Coord'][0]):
                if debug:
                    print('Empty row', row, 'before galaxy', galaxy)
                y_expansion += 999_999
        galaxy['Coord'] = (galaxy['Coord'][0], galaxy['Coord'][1] + x_expansion) 
        galaxy['Coord'] = (galaxy['Coord'][0] + y_expansion, galaxy['Coord'][1]) 
    pairs = get_pairs(galaxies, debug=False)
    distances = []
    for pair in pairs:
        if debug:
            print('Galaxy', pair[0]['ID'], 'to galaxy', pair[1]['ID'])
            print('From coordinate', pair[0]['Coord'], 'to coordinate', pair[1]['Coord'])
        x_distance = abs(pair[0]['Coord'][1] - pair[1]['Coord'][1])
        y_distance = abs(pair[0]['Coord'][0] - pair[1]['Coord'][0])
        if debug:
            print('Distance x:', x_distance, 'Distance y:', y_distance, 'Total distance:', x_distance + y_distance)
        distances.append(x_distance + y_distance)
    if debug:
        print('The distances:\n')
        pprint(distances)
    return sum(distances)


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
    
    expanded_input = expand_universe(parsed_input, args.debug)
    galaxies = get_galaxies(expanded_input, args.debug)
    # pairs = get_pairs(galaxies, args.debug)

    if args.part1 and args.debug:
        print('======================================================')
        print('                        Part 1                        ')
        print('======================================================')
        print('')

    if args.part1:
        solution_1 = part_1(galaxies, args.debug)
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
