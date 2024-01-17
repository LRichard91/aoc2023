#!/usr/bin/env python

import argparse
from collections import defaultdict
import networkx as nx
from pprint import pprint
import sys
from typing import Any


def parse_input(filename: str, debug: bool=False) -> dict[str, set]:
    '''Parse the input file'''
    parsed_input: dict[str, set] = defaultdict(set)
    with open(filename, 'r') as f:
        rawInput: list[str] = f.read().splitlines()
    if debug:
        print('The raw input:\n')
        pprint(rawInput)
        print('')
    for line in rawInput:
        key: str = line[:line.find(':')]
        values: list[str] = line[line.find(':') + 2:].split(' ')
        if debug:
            print('For component', key, 'the connected modules:', values, '\n')
        for value in values:
            parsed_input[key].add(value)
            parsed_input[value].add(key)
    return parsed_input


def part_1(input: Any, debug: bool=False):
    '''Solve Part 1'''
    graph = nx.DiGraph()
    leftGraph, rightGraph = set(), set()
    for key, values in input.items():
        for value in values:
            graph.add_edge(key, value, capacity=1.0)
    for component in [list(input.keys())[0]]:
        for key in input.keys():
            cut = 0
            left, right = set(), set()
            if component != key:
                cut, (left, right) = nx.minimum_cut(graph, component, key)
                if debug:
                    print('Cut:', cut, 'left:', left, 'right:', right, '\n')
            if cut == 3:
                leftGraph = left
                rightGraph = right
                break
    return len(leftGraph) * len(rightGraph)


def part_2(input: Any, debug: bool=False):
    '''Solve Part 2'''
    return 0


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
