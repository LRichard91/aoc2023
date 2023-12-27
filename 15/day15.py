#!/usr/bin/env python

import argparse
from pprint import pprint
import sys


### FIXME:
### Should have implemented the boxes as a single dict instead of a list of
### dicts with only one key each. It would've made a lot of things easier.


def parse_input(filename, debug=False):
    '''Parse the input file'''
    parsed_input = []
    with open(filename, 'r') as f:
        input = f.read().replace('\n', '').split(',')
    for item in input:
        parsed_input.append(item.encode())
    return parsed_input


def holiday_hash(input, debug=False):
    '''Holiday ASCII String Helper algorithm'''
    current_value = 0
    for char in input:
        if debug:
            print('The ASCII value of current character is:', char)
        current_value += char
        current_value *= 17
        current_value %= 256
        if debug:
            print('The current value for the current character is:', current_value)
    return current_value



def part_1(input, debug=False):
    '''Solve Part 1'''
    hash_values = []
    for item in input:
        hash_values.append(holiday_hash(item, debug))
    return sum(hash_values)


def hashmap(input, debug=False):
    '''Holiday ASCII String Helper Manual Arrangement Procedure'''
    hash_map = [[] for _ in range(256)]
    if debug:
        print('The length of the hashmap is:', len(hash_map), '\n')
    for item in input:
        if b'=' in item:
            label = item[0:item.find(b'=')]
            focal_length = int(item[item.find(b'=')+1:])
            box_nr = holiday_hash(label)
            label_in_box = False
            label_idx = -1
            for i, d in enumerate(hash_map[box_nr]):
                if label in d:
                    label_in_box = True
                    label_idx = i
            if label_in_box:
                hash_map[box_nr][label_idx][label] = focal_length
                if debug:
                    print(
                        'CHANGE : ',
                        'For item', item, 
                        '\nthe label is:', label, 
                        '\nthe focal length is:', focal_length, 
                        '\nthe box nr. is:', box_nr, 
                        '\nthe contents of the box is:', hash_map[box_nr],
                        '\n'
                    )
            else:
                hash_map[box_nr].append({label: focal_length})
                if debug:
                    print(
                        'ADD : ',
                        'For item', item, 
                        '\nthe label is:', label, 
                        '\nthe focal length is:', focal_length, 
                        '\nthe box nr. is:', box_nr, 
                        '\nthe contents of the box is:', hash_map[box_nr],
                        '\n'
                    )
        elif b'-' in item:
            label = item[0:item.find(b'-')]
            box_nr = holiday_hash(label)
            for d in hash_map[box_nr]:
                if label in d:
                    hash_map[box_nr].remove(d)
                    if debug:
                        print(
                            'REMOVE : ',
                            'For item', item, 
                            '\nthe label is:', label, 
                            '\nthe box nr. is:', box_nr, 
                            '\nthe contents of the box is:', hash_map[box_nr],
                            '\n'
                        )
    return hash_map


def part_2(input, debug=False):
    '''Solve Part 2'''
    boxes = hashmap(input, debug)
    if debug:
        print('The boxes:')
        for index, item in enumerate(boxes):
            if item:
                print('Box nr.', index, ':', item)
        print('')
    total_focusing_power = 0
    for box_nr, box in enumerate(boxes):
        box_focusing_power = 0
        for lens_nr, lens in enumerate(box):
            box_focusing_power += (box_nr + 1) * (lens_nr + 1) * sum([int(x) for x in lens.values()])
        total_focusing_power += box_focusing_power
    return total_focusing_power


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
