#!/usr/bin/env python

from functools import reduce
from pprint import pprint
import sys


def parse_input(filename, debug=False):
    '''Parse input file'''
    with open(filename, 'r') as f:
        input = f.read().splitlines()
        if debug:
            print('The raw input:')
            pprint(input)
            print('')
    races = []
    times = []
    distances = []
    for lines in input:
        if lines.find('Time:') != -1:
            times = lines[lines.find('Time:')+5:].split(' ')
            times = [int(x) for x in times if x != '']
        elif lines.find('Distance:') != -1:
            distances = lines[lines.find('Distance:')+9:].split(' ')
            distances = [int(x) for x in distances if x != '']
        else:
            continue
    for idx, time in enumerate(times):
        races.append((time, distances[idx]))
    
    if debug:
        print('The races:')
        pprint(races)
        print('')
    return races


def part_1(input, debug=False):
    '''Solve Part 1'''
    n_of_ways = []
    for idx, race in enumerate(input):
        if debug:
            print('')
            print('Race', idx+1)
        can_win = 0
        boat_spd = 0
        distance = 0
        for btn_hold in range(1, race[0]):
            if debug:
                print('Held for:', btn_hold, 'ms')
            time_remaining = race[0] - btn_hold
            boat_spd = 0 + btn_hold
            if boat_spd * time_remaining > race[1]:
                can_win += 1
                if debug:
                    print('Win!')
        n_of_ways.append(can_win)

    return reduce((lambda x, y: x * y), n_of_ways)


def part_2(input, debug=False):
    '''Solve Part 2'''
    n_of_ways = 0
    time = ''
    distance = ''
    for item in input:
        time = time + str(item[0])
        distance = distance + str(item[1])
    race = (int(time), int(distance))

    if debug:
        print('')
        print('===================================')
        print('              Part 2               ')
        print('===================================')
        print('')
        print('The correct input for Part 2:')
        pprint(race)
        print('')

    spd = 0
    dst = 0
    for btn_hold in range(1, race[0]):
        time_remaining = race[0] - btn_hold
        spd = 0 + btn_hold
        if spd * time_remaining > race[1]:
            n_of_ways += 1

    return n_of_ways


def main():
    '''Main function'''
    # Check for usage
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('USAGE: ./day6.py [--debug] <input.txt>')
        sys.exit(1)

    # Check for debug flag
    debug = False
    filename = ''
    if sys.argv[1] == '--debug' and len(sys.argv) == 3:
        debug = True
        filename = sys.argv[2]
    else:
        filename = sys.argv[1]

    # Parse the input
    input = parse_input(filename, debug)

    # Get Part 1 solution
    part_1_solution = part_1(input, debug)

    # Get Part 2 solution
    part_2_solution = part_2(input, debug)

    # Print out solutions
    print('')
    print('The solution for Part 1 is:', part_1_solution)
    print('')
    print('The solution for Part 2 is:', part_2_solution)
    print('')
    sys.exit(0)


if __name__ == "__main__":
    main()

