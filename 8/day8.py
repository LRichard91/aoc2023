#!/usr/bin/env python

from math import lcm
from pprint import pprint
import sys


def parse_input(filename, debug=False):
    '''Parse the input file'''
    parsed_input = {}

    with open(filename, 'r') as f:
        input = f.read().split('\n\n') 

    if debug:
        print('')
        print('The raw input:')
        pprint(input)
        print('')

    parsed_input['directions'] = input[0]

    lines = input[1].splitlines()

    for line in lines:
        key = line[0:line.find('=')-1]
        left = line[line.find('(')+1:line.find(',')]
        right = line[line.find(',')+2:line.find(')')]
        parsed_input[key] = (left, right)

    if debug:
        print('The parsed input:')
        pprint(parsed_input)
        print('')
    return parsed_input


def path_generator(directions):
    '''Generate the "infinite" path'''
    while True:
        yield directions


def traverse_path(input, starting_node, part, debug=False):
    steps = 0
    node = starting_node
    for dir in path_generator(input['directions']):
        for d in dir:
            if d == 'L':
                steps += 1
                node = input[node][0]
            else:
                steps += 1
                node = input[node][1]
            if debug:
                print('Step:', steps, '- New location:', node)
            if part == 1:
                if node == 'ZZZ':
                    return steps
            elif part == 2:
                if node[2:] == 'Z':
                    return steps


def part_1(input, debug=False):
    '''Solve Part 1'''
    if debug:
        print('')
        print('==================================')
        print('              Part 1              ')
        print('==================================')
        print('')

    loc = 'AAA'
    steps = traverse_path(input, loc, 1, debug)

    return steps


def part_2(input, debug=False):
    '''Solve Part 2'''
    if debug:
        print('')
        print('==================================')
        print('              Part 2              ')
        print('==================================')
        print('')

    starting_nodes = []
    for item in input:
        if item[2:] == 'A':
            starting_nodes.append(item)

    if debug:
        print('Starting nodes:')
        pprint(starting_nodes)
        print('')

    steps = []
    
    while starting_nodes:
        node = starting_nodes.pop()
        steps.append(traverse_path(input, node, 2, debug))

    solution = lcm(*steps)

    return solution


def main():
    '''Main function'''
    # Check for usage
    if len(sys.argv) == 4 and sys.argv[1] == '--debug':
        filename = sys.argv[3]
        debug = True
    elif len(sys.argv) == 3 and sys.argv[1] != '--debug':
        filename = sys.argv[2]
        debug = False
    else:
        print('USAGE: ./day8.py [--debug] [--part1 / --part2] <input.txt>')
        print('')
        sys.exit(1)
    
    parsed_input = parse_input(filename, debug)

    if not debug and sys.argv[1] == '--part1' or debug and sys.argv[2] == '--part1':
        solution_1 = part_1(parsed_input, debug)
        print('')
        print('The solution for Part 1 is:', solution_1)
        print('')

    if not debug and sys.argv[1] == '--part2' or debug and sys.argv[2] == '--part2':
        solution_2 = part_2(parsed_input, debug)
        print('')
        print('The solution for Part 2 is:', solution_2)
        print('')

    sys.exit(0)


if __name__ == "__main__":
    main()
