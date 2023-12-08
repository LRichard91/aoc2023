#!/usr/bin/env python

from pprint import pprint
import sys

# Using global data structures because parse_input needs to return multiple ones
SEEDS_1 = []
SEEDS_2 = []
SEED_TO_SOIL = []
SOIL_TO_FERTILIZER = []
FERTILIZER_TO_WATER = []
WATER_TO_LIGHT = []
LIGHT_TO_TEMP = []
TEMP_TO_HUMIDITY = []
HUMIDITY_TO_LOCATION = []


def parse_input(filename):
    """Parse the input file into the required data structures"""
    global SEEDS_1
    global SEED_TO_SOIL
    global SOIL_TO_FERTILIZER
    global FERTILIZER_TO_WATER
    global WATER_TO_LIGHT
    global LIGHT_TO_TEMP
    global TEMP_TO_HUMIDITY
    global HUMIDITY_TO_LOCATION
    # Get raw input split by lines into a list and remove empty lines
    with open(filename, 'r') as file:
        lines = file.read().splitlines()
        while '' in lines:
            lines.remove('')
    print('The input:')
    pprint(lines)
    print('')

    # Get the seeds for Part 1
    seeds_str = lines[0][lines[0].index(':') + 2:]
    seeds = seeds_str.split(' ')
    SEEDS_1 = [int(x) for x in seeds]
    print('The seed numbers are:')
    pprint(SEEDS_1)
    print('')

    # Get the indices for the maps
    idx_sts, idx_stf, idx_ftw, idx_wtl, idx_ltt, idx_tth, idx_htl = 0, 0, 0, 0, 0, 0, 0
    for idx, item in enumerate(lines):
        if item == '''seed-to-soil map:''':
            idx_sts = idx
        elif item == '''soil-to-fertilizer map:''':
            idx_stf = idx
        elif item == '''fertilizer-to-water map:''':
            idx_ftw = idx
        elif item == '''water-to-light map:''':
            idx_wtl = idx
        elif item == '''light-to-temperature map:''':
            idx_ltt = idx
        elif item == '''temperature-to-humidity map:''':
            idx_tth = idx
        elif item == '''humidity-to-location map:''':
            idx_htl = idx

    # Parse the maps
    for item in lines[idx_sts+1:idx_stf]:
        elements = item.split(' ')
        tup = []
        for n in elements:
            tup.append(int(n))
        tup = tuple(tup)
        for i in range(tup[2]):
            SEED_TO_SOIL.append({'to': tup[0] + i, 'from': tup[1] + i})
    print('The seed-to-soil map:')
    pprint(SEED_TO_SOIL)
    print('')

    for item in lines[idx_stf+1:idx_ftw]:
        elements = item.split(' ')
        tup = []
        for n in elements:
            tup.append(int(n))
        tup = tuple(tup)
        for i in range(tup[2]):
            SOIL_TO_FERTILIZER.append({'to': tup[0] + i, 'from': tup[1] + i})
    print('The soil-to-fertilizer map:')
    pprint(SOIL_TO_FERTILIZER)
    print('')

    for item in lines[idx_ftw+1:idx_wtl]:
        elements = item.split(' ')
        tup = []
        for n in elements:
            tup.append(int(n))
        tup = tuple(tup)
        for i in range(tup[2]):
            FERTILIZER_TO_WATER.append({'to': tup[0] + i, 'from': tup[1] + i})
    print('The fertilizer-to-water map:')
    pprint(FERTILIZER_TO_WATER)
    print('')
        
    for item in lines[idx_wtl+1:idx_ltt]:
        elements = item.split(' ')
        tup = []
        for n in elements:
            tup.append(int(n))
        tup = tuple(tup)
        for i in range(tup[2]):
            WATER_TO_LIGHT.append({'to': tup[0] + i, 'from': tup[1] + i})
    print('The water-to-light map:')
    pprint(WATER_TO_LIGHT)
    print('')
    
    for item in lines[idx_ltt+1:idx_tth]:
        elements = item.split(' ')
        tup = []
        for n in elements:
            tup.append(int(n))
        tup = tuple(tup)
        for i in range(tup[2]):
            LIGHT_TO_TEMP.append({'to': tup[0] + i, 'from': tup[1] + i})
    print('The light-to-temperature map:')
    pprint(LIGHT_TO_TEMP)
    print('')

    for item in lines[idx_tth+1:idx_htl]:
        elements = item.split(' ')
        tup = []
        for n in elements:
            tup.append(int(n))
        tup = tuple(tup)
        for i in range(tup[2]):
            TEMP_TO_HUMIDITY.append({'to': tup[0] + i, 'from': tup[1] + i})
    print('The temperature-to-humidity map:')
    pprint(TEMP_TO_HUMIDITY)
    print('')

    for item in lines[idx_htl+1:]:
        elements = item.split(' ')
        tup = []
        for n in elements:
            tup.append(int(n))
        tup = tuple(tup)
        for i in range(tup[2]):
            HUMIDITY_TO_LOCATION.append({'to': tup[0] + i, 'from': tup[1] + i})
    print('The humidity-to-location map:')
    pprint(HUMIDITY_TO_LOCATION)
    print('')


def get_location_naive():
    """Naive implementation of get_location"""
    # This is basically a linear search and walk the graph implementation
    locations = []
    global SEEDS_1
    global SEED_TO_SOIL
    global SOIL_TO_FERTILIZER
    global FERTILIZER_TO_WATER
    global WATER_TO_LIGHT
    global LIGHT_TO_TEMP
    global TEMP_TO_HUMIDITY
    global HUMIDITY_TO_LOCATION
    for item in SEEDS_1:
        print('Processing seed #:', item)
        f = int(item)
        t = 0
        for n in SEED_TO_SOIL:
            if f == n['from']:
                t = n['to']
                break
            else:
                t = f
        f = t
        t = 0
        for n in SOIL_TO_FERTILIZER:
            if f == n['from']:
                t = n['to']
                break
            else:
                t = f
        f = t
        t = 0
        for n in FERTILIZER_TO_WATER:
            if f == n['from']:
                t = n['to']
                break
            else:
                t = f
        f = t
        t = 0
        for n in WATER_TO_LIGHT:
            if f == n['from']:
                t = n['to']
                break
            else:
                t = f
        f = t
        t = 0
        for n in LIGHT_TO_TEMP:
            if f == n['from']:
                t = n['to']
                break
            else:
                t = f
        f = t
        t = 0
        for n in TEMP_TO_HUMIDITY:
            if f == n['from']:
                t = n['to']
                break
            else:
                t = f
        f = t
        t = 0
        for n in HUMIDITY_TO_LOCATION:
            if f == n['from']:
                t = n['to']
                break
            else:
                t = f
        locations.append(t)
    print('')
    print('The locations are:')
    pprint(locations)
    print('')
    return locations


def part_1(locations):
    """Get the lowest location number"""
    solution = min(locations)
    return solution


def main():
    """Main function"""
    if len(sys.argv) != 2:
        print('USAGE: ./day5.py input.txt')
        sys.exit(1)
    parse_input(sys.argv[1])
    locations = get_location_naive()
    solution_1 = part_1(locations)
    print('')
    print('The solution for Part 1 is:', solution_1)
    print('')
    print('The solution for Part 2 is:')
    sys.exit(0)


if __name__ == "__main__":
    main()

