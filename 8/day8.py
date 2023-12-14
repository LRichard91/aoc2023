#!/usr/bin/env python

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
    yield directions

def part_1(input, debug=False):
    '''Solve Part 1'''
    if debug:
        print('')
        print('==================================')
        print('              Part 1              ')
        print('==================================')
        print('')

    loc = 'AAA'
    steps = 0
    while loc != 'ZZZ':
        for dir in path_generator(input['directions']):
            for d in dir:
                if d == 'L':
                    steps += 1
                    loc = input[loc][0]
                else:
                    steps += 1
                    loc = input[loc][1]
                if debug:
                    print('Step', steps, '- New location:', loc)

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

    location = starting_nodes.copy()
    end_reached = False
    steps = 0

    while not end_reached:
        for dir in path_generator(input['directions']):
            end_node_found = [False for _ in range(len(location))]
            for d in dir:
                end_node_found = [False for _ in range(len(location))]
                if d == 'L':
                    steps += 1
                    for i, l in enumerate(location):
                        location[i] = input[l][0]
                if d == 'R':
                    steps += 1
                    for i, l in enumerate(location):
                        location[i] = input[l][1]
                for i, l in enumerate(location):
                    if l[2:] == 'Z':
                        end_node_found[i] = True
                if end_node_found.count(True) == len(location):
                    end_reached = True

                if debug:
                    print('New nodes:', location)
                    print('End nodes:', end_node_found)
                    print('End reached:', end_reached)
    return steps


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
