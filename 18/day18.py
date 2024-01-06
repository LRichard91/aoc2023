#!/usr/bin/env python

import argparse
from pprint import pprint
import sys
from typing import List, NamedTuple


DigDirection = NamedTuple('DigDirection', [('dir', str), ('dst', int), ('color', str)])


def parse_input(filename: str, debug: bool=False) -> List[DigDirection]:
    '''Parse the input file'''
    parsed_input: List[DigDirection] = []
    with open(filename, 'r') as f:
        raw = f.read().splitlines()
    if debug:
        print('The raw input:\n')
        pprint(raw)
        print('')
    for line in raw:
        dir: str = line[:1]
        dst: int = int(line[2:line.index('(')-1])
        color: str = line[line.index('(')+1:line.index(')')]
        if debug:
            print('For line:', line)
            print('The values:', dir, dst, color, '\n')
        direction: DigDirection = DigDirection(dir, dst, color)
        parsed_input.append(direction)
    return parsed_input


def makeGrid(input: List[DigDirection], debug: bool=False) -> List[str]:
    '''Make the grid'''
    len_x: int = 0
    len_y: int = 0
    for item in input:
        if item.dir in ['U', 'D']:
            len_y += item.dst
        else:
            len_x += item.dst
    if debug:
        print('The grid size is:', len_y, 'rows and:', len_x, 'columns\n')
    grid: List[str] = []
    for _ in range(len_y):
        grid.append('.' * len_x)
    if debug:
        print('The raw grid:\n')
        pprint(grid)
        print('')
    return grid


def digTrench(grid: List[str], last_pos: tuple[int, int], direction: DigDirection) -> tuple[List[str], tuple[int, int], list[tuple[int, int, str]]]:
    '''Dig the specified trench'''
    verticalWalls: list[tuple[int, int, str]] = []
    if direction.dir == 'R':
        line = list(grid[last_pos[0]])
        for idx, _ in enumerate(line):
            if idx > last_pos[1] and idx <= last_pos[1] + direction.dst:
                line[idx] = '#'
        grid[last_pos[0]] = ''.join(line)
        last_pos = last_pos[0], last_pos[1] + direction.dst
    elif direction.dir == 'D':
        col: int = last_pos[1]
        for row in range(last_pos[0], last_pos[0] + direction.dst + 1):
            if row == last_pos[0]:
                verticalWalls.append((row, col, 'D'))
                continue
            line = list(grid[row])
            line[col] = '#'
            grid[row] = ''.join(line)
            verticalWalls.append((row, col, 'D'))
        last_pos = last_pos[0] + direction.dst, last_pos[1]
    elif direction.dir == 'U':
        col: int = last_pos[1]
        for row in range(last_pos[0], last_pos[0] - direction.dst - 1, -1):
            line = list(grid[row])
            line[col] = '#'
            grid[row] = ''.join(line)
            verticalWalls.append((row, col, 'U'))
        last_pos = last_pos[0] - direction.dst, last_pos[1]
    else:
        line = list(grid[last_pos[0]])
        for idx, _ in enumerate(line):
            if idx < last_pos[1] and idx >= last_pos[1] - direction.dst:
                line[idx] = '#'
        grid[last_pos[0]] = ''.join(line)
        last_pos = last_pos[0], last_pos[1] - direction.dst
    return grid, last_pos, verticalWalls


def digPool(grid: List[str], verticalWalls: dict[tuple[int, int], str], debug: bool=False) -> List[str]:
    '''Dig the whole pool'''
    pool: List[str] = []
    for row, line in enumerate(grid):
        tiles = list(line)
        if debug:
            print(tiles)
            print('')
        for col, tile in enumerate(tiles):
            turnsPassed: int = 0
            lastWall: str = ''
            if tile == '.':
                for c in range(col + 1, len(tiles)):
                    if (row, c) in verticalWalls:
                        if verticalWalls[(row, c)] != lastWall:
                            turnsPassed += 1
                        lastWall = verticalWalls[(row, c)]
            if turnsPassed % 2 == 1:
                tiles[col] = '#'
        pool.append(''.join(tiles))
    return pool


def calculateVolume(grid: List[str]) -> int:
    '''Calculate the volume of the pool'''
    sum: int = 0
    for line in grid:
        sum += line.count('#')
    return sum


def part_1(input: List[DigDirection], debug: bool=False) -> int:
    '''Solve Part 1'''
    grid = makeGrid(input, debug)
    len_x: int = len(grid[0])
    len_y: int = len(grid)
    last_pos = (round(len_y / 4), round(len_x / 4))
    verticalWalls: list[list[tuple[int, int, str]]]
    *new_grid, verticalWalls = digTrench(grid, last_pos, input[0])
    for idx in range(1, len(input)):
        *new_grid, vertWall = digTrench(new_grid[0], new_grid[1], input[idx])
        verticalWalls.append(vertWall)
    if debug:
        print('The trenches dug:\n')
        pprint(new_grid[0])
        print('')
    verticalWallsSanitized: dict[tuple[int, int], str] = {} 
    while verticalWalls:
        walls = verticalWalls.pop()
        for item in walls:
            verticalWallsSanitized[(item[0], item[1])] = item[2]
    if debug:
        print('The vertical walls:\n')
        pprint(verticalWallsSanitized)
        print('')
    pool: List[str] = digPool(new_grid[0], verticalWallsSanitized, debug)
    if debug:
        print('The complete pool:\n')
        pprint(pool)
        print('')
    volume = calculateVolume(pool)
    return volume


def part_2(input, debug=False):
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
