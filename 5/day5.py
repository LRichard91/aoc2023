#!/usr/bin/env python

from pprint import pprint
import sys


def parse_input(filename, debug=False):
    '''Parse the input file'''
    input = []
    with open(filename, 'r') as f:
        input = f.read().splitlines()
        while '' in input:
            input.remove('')
    if debug:
        print('The input:')
        pprint(input)
        print('')

    return


def part_1():
    '''Get the solution for Part 1'''
    return 0


def part_2():
    '''Get the solution for Part 2'''
    return 0


def main():
    '''Main function'''
    # Check for correct argument count
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('USAGE: ./day5.py [--debug] <input_file>')
        sys.exit(1)
    
    # Get filename and check for debug flag (enables debugging print statements)
    filename = ''
    debug = False
    if len(sys.argv) == 3 and sys.argv[1] == '--debug':
        debug = True
        filename = sys.argv[2]
    elif len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        print('USAGE: ./day5.py [--debug] <input_file>')
        sys.exit(1)

    # Parse the input file
    parse_input(filename, debug)

    # Get the solutions and print them out
    part_1_solution = part_1()
    part_2_solution = part_2()
    print('')
    print('The solution for Part 1 is:', part_1_solution)
    print('')
    print('The solution for Part 2 is:', part_2_solution)
    sys.exit(0)


if __name__ == "__main__":
    main()
