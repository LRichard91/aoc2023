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
    return parsed_input


def trace_path(seed_number, parsed_input, debug=False):
    '''Trace the path for the current seed'''
    # IMPORTANT!!! : Only use for Part 1!
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


def map_ranges(parsed_input, debug=False):
    '''Map the seed ranges to location ranges'''
    # Get the seed ranges - list of tuples with start and end of range (inclusive)
    seed_ranges = []
    for index, item in enumerate(parsed_input['seeds']):
        if index % 2 == 0:
            s = item
        else:
            i = item
            seed_ranges.append((s, s+i-1))
    if debug:
        print('The seed ranges for Part 2:')
        pprint(seed_ranges)
        print('')

    # Massage parsed_input so I can work with start-end tuples
    seed_to_soil = []
    soil_to_fert = []
    fert_to_water = []
    water_to_light = []
    light_to_temp = []
    temp_to_humid = []
    humid_to_loc = []

    for item in parsed_input:
        if item == 'seeds':
            continue
        for idx, _ in enumerate(parsed_input[item]):
            for i, n in enumerate(parsed_input[item][idx]):
                if i == 0:
                    dest_start = n
                elif i == 1:
                    source_start = n
                else:
                    delta = n - 1
                    tup = (source_start, source_start+delta, dest_start, dest_start+delta)
                    match item:
                        case 'seed-to-soil':
                            seed_to_soil.append(tup)
                        case 'soil-to-fertilizer':
                            soil_to_fert.append(tup)
                        case 'fertilizer-to-water':
                            fert_to_water.append(tup)
                        case 'water-to-light':
                            water_to_light.append(tup)
                        case 'light-to-temp':
                            light_to_temp.append(tup)
                        case 'temp-to-hum':
                            temp_to_humid.append(tup)
                        case 'hum-to-loc':
                            humid_to_loc.append(tup)
    if debug:
        print('The remapped ranges:\n')
        print('Seed to soil:')
        pprint(seed_to_soil)
        print('Soil to fertilizer:')
        pprint(soil_to_fert)
        print('Fertilizer to water:')
        pprint(fert_to_water)
        print('Water to light:')
        pprint(water_to_light)
        print('Light to temperature:')
        pprint(light_to_temp)
        print('Temperature to humidity:')
        pprint(temp_to_humid)
        print('Humiditiy to location:')
        pprint(humid_to_loc)
        print('')


    # Map seed ranges to location ranges
            
    return 0


def get_seeds(start, interval):
    n = start
    while n < start + interval:
        yield n
        n += 1


def part_2(parsed_input, debug=False):
    '''Get the solution for Part 2'''
    locations = []
    min_locations = []
    seeds = []
    start, interval = 0, 0
    for i, item in enumerate(parsed_input['seeds']):
        if i % 2 == 0:
            start = parsed_input['seeds'][i]
        elif i % 2 == 1:
            interval = parsed_input['seeds'][i]
            seeds.append((start, interval))

    for item in seeds:
        for seed in get_seeds(*item):
            if debug:
                print('Processing seed nr.', seed)
            elif not debug and seed % 100000 == 0:
                print('Processing seed nr.', seed)
            locations.append(trace_path(seed, parsed_input, debug))
        min_locations.append(min(locations))
        locations = []

    if debug:
        print('The locations for Part 2 are:')
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

    # Get the solution for Part 1
    part_1_solution = part_1(parsed_input, debug)

    if debug:
        print('===================================')
        print('              Part 2               ')
        print('===================================')
        print('')

    # Get the mapped ranges for Part 2 solution
    mapped_ranges = map_ranges(parsed_input, debug)

    # Get the solution for Part 2
    part_2_solution = part_2(parsed_input, debug)

    # Print out solutions
    print('')
    print('The solution for Part 1 is:', part_1_solution)
    print('')
    print('The solution for Part 2 is:', part_2_solution)
    print('')
    sys.exit(0)


if __name__ == "__main__":
    main()
