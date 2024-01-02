#!/usr/bin/env python

import argparse
from collections import namedtuple
from pprint import pprint
import sys
from typing import Dict, List, NamedTuple, Tuple


Part = NamedTuple(
    'Part', 
    [
        ('x', int), 
        ('m', int), 
        ('a', int), 
        ('s', int),
    ]
)

Condition = NamedTuple(
    'Condition',
    [
        ('cat', str),
        ('op', str),
        ('val', int),
        ('dst', str)
    ]
)


def parse_input(filename: str, debug: bool=False) -> Tuple[List[Part], Dict]:
    '''Parse the input file'''
    raw_input: List[str] = []

    with open(filename, 'r') as f:
        raw_input = f.read().splitlines()

    if debug:
        print('The raw input:\n')
        pprint(raw_input)
        print('')

    parts: List[Part] = []
    line: str = raw_input.pop()
    idx: int = 0

    while line != '':
        x: int = int(line[line.find('x=') + 2 : line.find(',')])
        line = line[line.find(',') + 1 :]
        m: int = int(line[line.find('m=') + 2 : line.find(',')])
        line = line[line.find(',') + 1 :]
        a: int = int(line[line.find('a=') + 2 : line.find(',')])
        line = line[line.find(',') + 1 :]
        s: int = int(line[line.find('s=') + 2 : line.find('}')])
        part: Part = Part(x, m, a, s)
        # if debug:
        #     print('The xmas values of part nr.', idx, 'are:', part.x, part.m, part.a, part.s, '\n')
        idx += 1
        parts.append(part)
        line = raw_input.pop()

    if debug:
        print('The parts:\n')
        pprint(parts)
        print('')

    workflows: Dict = {}
    idx = 0

    while raw_input:
        line = raw_input.pop()
        conditions: List[Condition] = []

        workflow: str = line[:line.find('{')]
        line = line[line.find('{') + 1:]

        p = line.replace('{', '').replace('}', '').split(',')

        for item in p:
            val: str = ''
            value: int = 0
            dest: str = ''
            op: str = ''
            cat: str = ''
            cond: bool = False

            if item == p[len(p) - 1]:
                conditions.append(Condition('*', '*', 0, item))

            for i, _ in enumerate(item):
                if i == 0 and item[i] in ['x', 'm', 'a', 's']:
                    cond = True
                    cat = item[i]

                elif item[i] == '<':
                    op = 'lt'

                elif item[i] == '>':
                    op = 'gt'

                elif item[i].isdigit():
                    val = val + item[i]
                    if val == '':
                        value = 0
                    else:
                        value = int(val)

                elif item[i] == ':':
                    dest = item[i + 1:]

            if cond: 
                conditions.append(Condition(cat, op, value, dest))

        workflows[workflow] = conditions

    if debug:
        print('The workflows:\n')
        pprint(workflows)
        print('')

    return parts, workflows


def sortPart(part: Part, workflow: str, workflows: Dict, acceptList: List[Part], rejectList: List[Part]) -> None:
    '''Sort the part through the workflows'''
    for condition in workflows[workflow]:
        if condition.cat == '*':
            if condition.dst == 'A':
                acceptList.append(part)
                return
            elif condition.dst == 'R':
                rejectList.append(part)
                return
            else:
                sortPart(part, condition.dst, workflows, acceptList, rejectList)
                return
        else:
            if condition.cat == 'x':
                if condition.op == 'lt':
                    if part.x < condition.val:
                        if condition.dst == 'A':
                            acceptList.append(part)
                            return
                        elif condition.dst == 'R':
                            rejectList.append(part)
                            return
                        else:
                            sortPart(part, condition.dst, workflows, acceptList, rejectList)
                            return
                elif condition.op =='gt':
                    if part.x > condition.val:
                        if condition.dst == 'A':
                            acceptList.append(part)
                            return
                        elif condition.dst == 'R':
                            rejectList.append(part)
                            return
                        else:
                            sortPart(part, condition.dst, workflows, acceptList, rejectList)
                            return
            elif condition.cat == 'm':
                if condition.op == 'lt':
                    if part.m < condition.val:
                        if condition.dst == 'A':
                            acceptList.append(part)
                            return
                        elif condition.dst == 'R':
                            rejectList.append(part)
                            return
                        else:
                            sortPart(part, condition.dst, workflows, acceptList, rejectList)
                            return
                elif condition.op =='gt':
                    if part.m > condition.val:
                        if condition.dst == 'A':
                            acceptList.append(part)
                            return
                        elif condition.dst == 'R':
                            rejectList.append(part)
                            return
                        else:
                            sortPart(part, condition.dst, workflows, acceptList, rejectList)
                            return
            elif condition.cat == 'a':
                if condition.op == 'lt':
                    if part.a < condition.val:
                        if condition.dst == 'A':
                            acceptList.append(part)
                            return
                        elif condition.dst == 'R':
                            rejectList.append(part)
                            return
                        else:
                            sortPart(part, condition.dst, workflows, acceptList, rejectList)
                            return
                elif condition.op =='gt':
                    if part.a > condition.val:
                        if condition.dst == 'A':
                            acceptList.append(part)
                            return
                        elif condition.dst == 'R':
                            rejectList.append(part)
                            return
                        else:
                            sortPart(part, condition.dst, workflows, acceptList, rejectList)
                            return
            elif condition.cat == 's':
                if condition.op == 'lt':
                    if part.s < condition.val:
                        if condition.dst == 'A':
                            acceptList.append(part)
                            return
                        elif condition.dst == 'R':
                            rejectList.append(part)
                            return
                        else:
                            sortPart(part, condition.dst, workflows, acceptList, rejectList)
                            return
                elif condition.op =='gt':
                    if part.s > condition.val:
                        if condition.dst == 'A':
                            acceptList.append(part)
                            return
                        elif condition.dst == 'R':
                            rejectList.append(part)
                            return
                        else:
                            sortPart(part, condition.dst, workflows, acceptList, rejectList)
                            return

    raise LookupError('No path found for part')


def sortParts(parts: List[Part], workflows: Dict) -> Tuple[List[Part], List[Part]]:
    '''Sort the parts until Accept/Reject'''
    acceptList: List[Part] = []
    rejectList: List[Part] = []

    for part in parts:
        sortPart(part, 'in', workflows, acceptList, rejectList)

    return acceptList, rejectList


def part_1(input, debug=False):
    '''Solve Part 1'''
    acceptList, rejectList = sortParts(*input)

    if debug:
        print('The accepted parts:\n')
        pprint(acceptList)
        print('')
        print('The rejected parts:\n')
        pprint(rejectList)

    ratingSum: int = 0
    for item in acceptList:
        ratingSum += item.x + item.m + item.a + item.s

    return ratingSum


def bisectRange(r: range, value: int) -> Tuple[range, range]:
    '''Bisect a range at the value given'''
    return range(r.start, value), range(value, r.stop)


def traceWorkflows(workflows: Dict) -> None:
    '''Trace the workflows'''
    genericPart = NamedTuple(
        'genericPart', 
        [
            ('x', range), 
            ('m', range), 
            ('a', range),
            ('s', range),
        ],
    )

    gPart: genericPart = genericPart(range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001))

    for wFlow in workflows['in']:
        if wFlow.op == 'gt':
            match(wFlow.cat):
                case 'x':
                    keep, send = bisectRange(gPart.x, wFlow.val + 1)
                    break
                case 'm':
                    keep, send = bisectRange(gPart.m, wFlow.val + 1)
                    break
                case 'a':
                    keep, send = bisectRange(gPart.a, wFlow.val + 1)
                    break
                case 's':
                    keep, send = bisectRange(gPart.s, wFlow.val + 1)
                    break
        elif wFlow.op == 'lt':
            match(wFlow.cat):
                case 'x':
                    send, keep = bisectRange(gPart.x, wFlow.val)
                    break
                case 'm':
                    send, keep = bisectRange(gPart.x, wFlow.val)
                    break
                case 'a':
                    send, keep = bisectRange(gPart.x, wFlow.val)
                    break
                case 's':
                    send, keep = bisectRange(gPart.x, wFlow.val)
                    break
        else:
            ...
    return


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

    # if args.debug:
    #     print('The parsed input:')
    #     print('')
    #     pprint(parsed_input)
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
