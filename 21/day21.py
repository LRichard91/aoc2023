#!/usr/bin/env python

import argparse
from collections import deque
from pprint import pprint
import sys
from typing import Any, NamedTuple


Point = NamedTuple('Point', [('x', int), ('y', int)]) 

MAX_STEPS = 64

def parse_input(filename: str, debug: bool=False) -> tuple[Point, dict[Point, list[Point]], list[str]]:
    '''Parse the input file'''
    parsed_input: dict[Point, list[Point]] = {}
    with open(filename, 'r') as f:
        raw_input: list[str] = f.read().splitlines()
    if debug:
        print('The raw input:\n')
        pprint(raw_input)
        print('')
    walled_garden: list[str] = []
    l = len(raw_input[0])
    walled_garden.append('#' * (l + 2))
    for line in raw_input:
        new_line = '#' + line + '#' 
        walled_garden.append(new_line)
    walled_garden.append('#' * (l + 2))
    if debug:
        print('The walled garden:\n')
        pprint(walled_garden)
        print('')
    startPoint: Point = Point(0, 0)
    for y in range(1, len(walled_garden) - 1):
        for x in range(1, len(walled_garden[0]) - 1):
            neighbours: list[Point] = []
            if walled_garden[y][x] in ['.', 'S']:
                if walled_garden[y][x] == 'S':
                    startPoint = Point(x, y)
                if walled_garden[y - 1][x] in ['.', 'S']:
                    neighbours.append(Point(x, y - 1))
                if walled_garden[y + 1][x] in ['.', 'S']:
                    neighbours.append(Point(x, y + 1))
                if walled_garden[y][x - 1] in ['.', 'S']:
                    neighbours.append(Point(x - 1, y))
                if walled_garden[y][x + 1] in ['.', 'S']:
                    neighbours.append(Point(x + 1, y))
            parsed_input[Point(x, y)] = neighbours
    return startPoint, parsed_input, walled_garden


def getPossibleSteps(graph: dict[Point, list[Point]], position: Point) -> deque[Point]:
    '''Get the possible steps from a particular garden plot'''
    return deque(graph[position])


def part_1(input: Any, debug: bool=False) -> int:
    '''Solve Part 1'''
    startPoint, graph, walledGarden = input
    if debug:
        print('The starting point:', startPoint, '\n')
        print('The nodes:\n')
        pprint(graph, width=400)
        print('')
        print('The walled garden:\n')
        pprint(walledGarden)
        print('')
    # stack = deque(getPossibleSteps(graph, startPoint))
    # steps: int = 1
    # while stack:
    #     if debug:
    #         print('Step', steps, 'stack:', stack)
    #     if steps == MAX_STEPS + 1:
    #         break
    #     steps += 1
    #     stack.extend(getPossibleSteps(graph, stack.popleft()))
    queue: deque = getPossibleSteps(graph, startPoint)
    steps: int = 1
    while steps < MAX_STEPS:
        print('Step:', steps, '\n')
        if debug:
            print('Step', steps, 'queue:', queue)
        next_queue: deque = queue.popleft()
        new_queue: deque = deque()
        steps += 1
        while next_queue:
            if type(next_queue) == Point:
                next: Point = next_queue
                try:
                    next_queue = queue.popleft()
                except IndexError:
                    next_queue = deque() 
            else:
                next: Point = next_queue.popleft()
            nextNodes = getPossibleSteps(graph, next)
            while nextNodes:
                item = nextNodes.popleft()
                if item not in new_queue:
                    new_queue.append(item)
            if debug:
                print('New queue:', new_queue)
        queue.append(new_queue)
    return len(queue[0])


def part_2(input: Any, debug: bool=False) -> int:
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

    # if args.debug:
    #     print('The parsed input:')
    #     print('')
    #     pprint(parsed_input, width=200)
    #     print('')        

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
