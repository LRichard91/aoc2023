#!/usr/bin/env python

import argparse
from collections import deque
from pprint import pprint
import sys
from typing import Any, NamedTuple


Brick = NamedTuple(
    'Brick',
    [
        ('x', int),
        ('y', int),
        ('z', int),
        ('x_', int),
        ('y_', int),
        ('z_', int),
    ],
)


def parse_input(filename: str, debug: bool=False) -> Any:
    '''Parse the input file'''
    parsed_input: dict[int, Brick] = {}
    with open(filename, 'r') as f:
        raw_input = f.read().splitlines()

    if debug:
        print('The raw input:\n')
        pprint(raw_input)
        print('')

    bricks: list[Brick] = []
    max_x: int = 0
    max_y: int = 0
    for line in raw_input:
        start, end = line.split('~')
        x, y, z = start.split(',')
        x_, y_, z_ = end.split(',')
        if int(x_) > max_x:
            max_x = int(x_)
        if int(y_) > max_y:
            max_y = int(y_)
        bricks.append(
            Brick(
                int(x),
                int(y),
                int(z),
                int(x_),
                int(y_),
                int(z_)
            )
        )
    bricks.sort(key=lambda a: a.z, reverse=False)

    if debug:
        print('The list of bricks:\n')
        pprint(bricks)
        print('')

    for i in range(len(bricks)):
        parsed_input[i + 1] = bricks[i]

    return parsed_input, (max_x, max_y)


def settleBricks(bricks: dict[int, Brick], gridSize: tuple[int, int], debug: bool=False) -> dict[int, tuple[Brick, list[int]]]:
    '''Get the state after all bricks have fallen'''
    # finalState has BrickIDs, and a tuple with the Brick's coords and a list of its supports
    finalState: dict[int, tuple[Brick, list[int]]] = {}
    # gridHeights is for tracking current heights of each grid location and the ID of the uppermost Brick at that location
    gridHeights: list[list[tuple[int, int]]] = []
    for y in range(gridSize[1] + 1):
        rowHeight: list[tuple[int, int]] = []
        for x in range(gridSize[0] + 1):
            rowHeight.append((0, 0))
        gridHeights.append(rowHeight)

    if debug:
        print('The starting gridHeights and uppermost IDs:\n')
        pprint(gridHeights)
        print('')

    for i in bricks.keys():
        # Unpack coordinates
        x, y, z, x_, y_, z_ = bricks[i]
        # Set up variables for row and column indices
        xIdx: int = -1 
        yIdx: int = -1
        # Set up variable for tracking maximum height in a set of positions
        maxHeight: int = 0
        # Set up list for the supporting bricks
        supports: list[int] = []
        # If y and y_ are the same, we remain in the same row
        if y == y_:
            yIdx = y
        # If x and x_ are the same, we remain in the same column
        if x == x_:
            xIdx = x
        # If both xIdx and yIdx are above 0, we are dealing with a cube or a vertical brick
        if xIdx >= 0 and yIdx >= 0:
            # Get current maximum height of the grid
            maxHeight = gridHeights[yIdx][xIdx][0]
            # Get the id of what's underneath
            support = gridHeights[yIdx][xIdx][1]
            # If the support is a brick, append it's ID to the supports list
            if support > 0:
                supports.append(support)
            # Decrement z and z_
            z, z_ = decrementZ(z, z_, maxHeight)
            # Update the current max height of the grid and what's in that location with the height and ID of current brick
            gridHeights[yIdx][xIdx] = (z_, i)
        # Else, if yIdx is above 0, we have a brick that remains in the same row
        elif yIdx >= 0:
            heights: list[int] = [x[0] for x in gridHeights[yIdx][x:x_ + 1]]
            maxHeight = max(heights)
            maxIndices = findAllMaxIndices(heights, maxHeight)
            for idx in maxIndices:
                if gridHeights[yIdx][idx + x][1] > 0 and gridHeights[yIdx][idx + x][1] not in supports:
                    supports.append(gridHeights[yIdx][idx + x][1])
            z, z_ = decrementZ(z, z_, maxHeight)
            for idx in range(x, x_ + 1):
                gridHeights[yIdx][idx] = (z_, i)
        # Else, if xIdx is above 0, we have a brick that remains in the same column
        elif xIdx >= 0:
            heights: list[int] = [x[xIdx][0] for x in gridHeights[y: y_ + 1]]
            maxHeight = max(heights)
            maxIndices = findAllMaxIndices(heights, maxHeight)
            for idx in maxIndices:
                if gridHeights[idx + y][xIdx][1] > 0 and gridHeights[idx + y][xIdx][1] not in supports:
                    supports.append(gridHeights[idx + y][xIdx][1])
            z, z_ = decrementZ(z, z_, maxHeight)
            for idx in range(y, y_ + 1):
                gridHeights[idx][xIdx] = (z_, i)
        # Else, we have done something really-really wrong...
        else:
            print('OH SHIT!\n')

        # Add the brick with updated coords and its supports list to the finalState dict
        finalState[i] = Brick(x, y, z, x_, y_, z_), supports

    return finalState


def decrementZ(z: int, z_: int, maxHeight: int) -> tuple[int, int]:
    '''Helper function for decrementing z coordinates'''
    # Set up a Δz variable for decrementing z and z_ coordinates
    zDelta: int = 0
    zDelta = z - (maxHeight + 1)
    return z - zDelta, z_ - zDelta


def findAllMaxIndices(lst: list[int], val: int) -> list[int]:
    '''Find all indices where we are at max height'''
    start: int = -1
    indices: list[int] = []
    while True:
        try:
            idx = lst.index(val, start + 1)
        except ValueError:
            break
        else:
            indices.append(idx)
            start = idx
    return indices


def canDisintegrate(brickId: int, grid: dict[int, tuple[Brick, list[int]]], debug: bool = False) -> bool:
    '''Check if a brick can be disintegrated'''
    onlySupport: bool = False
    for brick in grid.values():
        if brickId in brick[1] and len(brick[1]) == 1:
            onlySupport = True
    if onlySupport:
        return False
    return True


def chainReaction(grid: dict[int, tuple[Brick, list[int]]], debug: bool=False) -> int:
    '''Get the number of bricks that would fall in a chain reaction'''
    starters = deque()
    # Get inital bricks that can cause a fall (those that are the only supports for another brick)
    for brickId in grid:
        if not canDisintegrate(brickId, grid, debug):
            starters.append(brickId)

    if debug:
        print('The initial targets:', starters, '\n')

    # For all starters, get all the bricks that would fall
    fallingBricks: list[int] = []
    while starters:
        falling = []
        currId = starters.popleft()
        if debug:
            print('If brick', currId, 'would disintegrate,', falling, 'bricks would also fall')
        fallingBricks.append(len(falling))

    return sum(fallingBricks)


def part_1(input: Any, debug: bool=False) -> int:
    '''Solve Part 1'''
    finalState = settleBricks(input[0], input[1], debug)

    if debug:
        print('The final state:\n')
        pprint(finalState)
        print('')

    safeBricks: int = 0
    for brickId in finalState.keys():
        if canDisintegrate(brickId, finalState, debug):
            if debug:
                print('Brick nr.', brickId, 'can be disintegrated')
            safeBricks += 1

    return safeBricks


def part_2(input: Any, debug: bool=False) -> int:
    '''Solve Part 2'''
    finalState = settleBricks(input[0], input[1], debug)
    falling: int = chainReaction(finalState, debug)
    return falling


def main() -> None:
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
