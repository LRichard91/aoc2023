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

    # Parsed input is a dictionary containing lists of tuples like this:
    # {'seeds': [...], 'sts': [(t, f, i), ...], stf:[(t, f, i), ...], ...}
    parsed_input = {}
    sts_idx, stf_idx, ftw_idx, wtl_idx, ltt_idx, tth_idx, htl_idx = 0, 0, 0, 0, 0, 0, 0
    for index, item in enumerate(input):
        if item.find('seeds:') != -1:
            idx = item.find(':') + 2 
            seed_str = item[idx:]
            seeds = []
            for n in seed_str.split(' '):
                seeds.append(int(n))
            parsed_input['seeds'] = seeds 
        if item == 'seed-to-soil map:':
            sts_idx = index
        elif item == 'soil-to-fertilizer map:':
            stf_idx = index
        elif item == 'fertilizer-to-water map:':
            ftw_idx = index
        elif item == 'water-to-light map:':
            wtl_idx = index
        elif item == 'light-to-temperature map:':
            ltt_idx = index
        elif item == 'temperature-to-humidity map:':
            tth_idx = index
        elif item == 'humidity-to-location map:':
            htl_idx = index
        else:
            continue
        
    parsed_input['seed-to-soil'] = []
    for item in input[sts_idx+1:stf_idx]:
        t, f, i = 0, 0, 0
        for idx, n in enumerate(item.split(' ')):
            if idx == 0:
                t = int(n)
            elif idx == 1:
                f = int(n)
            else:
                i = int(n)
        parsed_input['seed-to-soil'].append((t, f, i))

    parsed_input['soil-to-fertilizer'] = []
    for item in input[stf_idx+1:ftw_idx]:
        t, f, i = 0, 0, 0
        for idx, n in enumerate(item.split(' ')):
            if idx == 0:
                t = int(n)
            elif idx == 1:
                f = int(n)
            else:
                i = int(n)
        parsed_input['soil-to-fertilizer'].append((t, f, i))

    parsed_input['fertilizer-to-water'] = []
    for item in input[ftw_idx+1:wtl_idx]:
        t, f, i = 0, 0, 0
        for idx, n in enumerate(item.split(' ')):
            if idx == 0:
                t = int(n)
            elif idx == 1:
                f = int(n)
            else:
                i = int(n)
        parsed_input['fertilizer-to-water'].append((t, f, i))

    parsed_input['water-to-light'] = []
    for item in input[wtl_idx+1:ltt_idx]:
        t, f, i = 0, 0, 0
        for idx, n in enumerate(item.split(' ')):
            if idx == 0:
                t = int(n)
            elif idx == 1:
                f = int(n)
            else:
                i = int(n)
        parsed_input['water-to-light'].append((t, f, i))

    parsed_input['light-to-temp'] = []
    for item in input[ltt_idx+1:tth_idx]:
        t, f, i = 0, 0, 0
        for idx, n in enumerate(item.split(' ')):
            if idx == 0:
                t = int(n)
            elif idx == 1:
                f = int(n)
            else:
                i = int(n)
        parsed_input['light-to-temp'].append((t, f, i))

    parsed_input['temp-to-hum'] = []
    for item in input[tth_idx+1:htl_idx]:
        t, f, i = 0, 0, 0
        for idx, n in enumerate(item.split(' ')):
            if idx == 0:
                t = int(n)
            elif idx == 1:
                f = int(n)
            else:
                i = int(n)
        parsed_input['temp-to-hum'].append((t, f, i))

    parsed_input['hum-to-loc'] = []
    for item in input[htl_idx+1:]:
        t, f, i = 0, 0, 0
        for idx, n in enumerate(item.split(' ')):
            if idx == 0:
                t = int(n)
            elif idx == 1:
                f = int(n)
            else:
                i = int(n)
        parsed_input['hum-to-loc'].append((t, f, i))

    if debug:
        print('The parsed input:')
        pprint(parsed_input)
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
