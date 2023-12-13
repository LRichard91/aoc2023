#!/usr/bin/env python

from multiprocessing import Pool
from pprint import pprint
import sys


PARSED_INPUT = {}
DEBUG = False


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
    return parsed_input


def trace_path(seed_number, parsed_input, debug=False):
    '''Trace the path for the current seed'''
    location = 0
    curr_map = parsed_input['seed-to-soil']
    fr = seed_number
    to = seed_number
    for item in curr_map:
        if fr >= item[1] and fr < item[1] + item[2]:
            to = item[0] + (fr - item[1])
    if debug:
        print(f"Seed #{fr} goes to soil #{to}")
    
    curr_map = parsed_input['soil-to-fertilizer']
    fr = to
    for item in curr_map:
        if fr >= item[1] and fr < item[1] + item[2]:
            to = item[0] + (fr - item[1])
    if debug:
        print(f"Soil #{fr} goes to fertilizer #{to}")
    
    curr_map = parsed_input['fertilizer-to-water']
    fr = to
    for item in curr_map:
        if fr >= item[1] and fr < item[1] + item[2]:
            to = item[0] + (fr - item[1])
    if debug:
        print(f"Fertilizer #{fr} goes to water #{to}")

    curr_map = parsed_input['water-to-light']
    fr = to
    for item in curr_map:
        if fr >= item[1] and fr < item[1] + item[2]:
            to = item[0] + (fr - item[1])
    if debug:
        print(f"Water #{fr} goes to light #{to}")

    curr_map = parsed_input['light-to-temp']
    fr = to
    for item in curr_map:
        if fr >= item[1] and fr < item[1] + item[2]:
            to = item[0] + (fr - item[1])
    if debug:
        print(f"Light #{fr} goes to temperature #{to}")

    curr_map = parsed_input['temp-to-hum']
    fr = to
    for item in curr_map:
        if fr >= item[1] and fr < item[1] + item[2]:
            to = item[0] + (fr - item[1])
    if debug:
        print(f"Temperature #{fr} goes to humidity #{to}")

    curr_map = parsed_input['hum-to-loc']
    fr = to
    for item in curr_map:
        if fr >= item[1] and fr < item[1] + item[2]:
            to = item[0] + (fr - item[1])
    if debug:
        print(f"Humidity #{fr} goes to location #{to}")
        print('')

    location = to

    return location


def range_generator(start, interval):
    '''Generator function for the range of seeds'''
    seed = start
    while seed < start + interval:
        yield seed
        seed += 1


def part_1(parsed_input, debug=False):
    '''Get the solution for Part 1'''
    locations = []
    for item in parsed_input['seeds']:
        locations.append(trace_path(item, parsed_input, debug))

    if debug:
        print('The locations for Part 1 are:')
        pprint(locations)
        print('')

    return min(locations)


def worker(seed_nr):
    '''Worker function for multiprocessing'''
    s = trace_path(seed_nr, PARSED_INPUT, DEBUG)
    return s
    

def part_2(parsed_input, debug=False):
    '''Get the solution for Part 2'''
    global PARSED_INPUT
    global DEBUG
    PARSED_INPUT = parsed_input
    DEBUG = debug
    # Convert the seeds part in parsed input
    lst = []
    num, interval = 0, 0
    for idx, item in enumerate(parsed_input['seeds']):
        if idx % 2 == 0:
            num = item
        elif idx % 2 == 1:
            interval = item
            lst.append((num, interval))
            num = 0
            interval = 0
    if debug:
        print('The seeds input for Part 2 is:', lst)
        print('')

    parsed_input['seeds'] = lst
    if debug:
        print('The parsed input for Part 2 is:')
        pprint(parsed_input)
        print('')

    # Run trace_path on generated seed range
    min_locations = []
    # for item in parsed_input['seeds']:
    #     for seed in range_generator(item[0], item[1]):
    #         print(f'Processing seed #{seed}')
    #         locations.append(trace_path(seed, parsed_input, debug))
    with Pool(processes=4) as pool:
        for item in parsed_input['seeds']:
            print(f'Processing seed range {item}')
            print('')
            temp_loc = []
            temp_loc.append([x for x in pool.imap(worker, range_generator(item[0], item[1]), 1000)])
            min_locations.append(min([item for row in temp_loc for item in row]))
            if debug:
                print(f'The locations for seed range {item} are:')
                pprint(temp_loc)
                print('')

    if debug:
        print('The minimum locations for all seed ranges in Part 2 are:')
        pprint(min_locations)
        print('')

    return min(min_locations) 


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
    parsed_input = parse_input(filename, debug)

    # Get the solutions and print them out
    part_1_solution = part_1(parsed_input, debug)
    part_2_solution = part_2(parsed_input, debug)
    print('')
    print('The solution for Part 1 is:', part_1_solution)
    print('')
    print('The solution for Part 2 is:', part_2_solution)
    sys.exit(0)


if __name__ == "__main__":
    main()
