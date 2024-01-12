#!/usr/bin/env python

import argparse
from collections import defaultdict, deque
from pprint import pprint
import sys
from typing import NamedTuple


Node = NamedTuple(
    'Node',
    [
        ('x', int),
        ('y', int),
    ],
)


class Graph:

    def __init__(self, nodeNum: int, debug: bool) -> None:
        '''Initialize graph with default dict (adjacency list) and the number of nodes'''
        self.adjacent = defaultdict(list)
        self.allPaths: list[list[Node]] = []
        self.nodes = nodeNum
        self.start: Node = Node(0, 0)
        self.end: Node = Node(0, 0)
        self.firstJunction: Node = Node(0, 0)
        self.lastJunction: Node = Node(0, 0)
        self.firstDistance: int = 0
        self.lastDistance: int = 0
        self.debug = debug

    def addEdge(self, src: Node, dst: Node) -> None:
        '''Add non-directional edge'''
        self.adjacent[src].append(dst)
        self.adjacent[dst].append(src)

    def addDirectedEdge(self, src: Node, dst: Node) -> None:
        '''Add directional edge'''
        self.adjacent[src].append(dst)

    def displayAdjacencyList(self) -> None:
        '''Display the adjacency list'''
        pprint(self.adjacent, width=200)

    def buildGraph(self, listInput: list[list[str]]) -> None:
        '''Build the graph from a list of list of characters'''
        ### This is a DFS basically ###
        # Set up the stack, get the beginning and end nodes, push beginning node on the stack
        stack: list[tuple[Node, Node]] = []
        start: Node = Node(0, 0) 
        end: Node = Node(0, 0)
        for x, char in enumerate(listInput[0]):
            if char == '.':
                start = Node(x, 0)
        for x, char in enumerate(listInput[l := len(listInput) - 1]):
            if char == '.':
                end = Node(x, l)
        stack.append((start, start))
        # Debug message to check the above
        if self.debug:
            print('The start of the path:', start)
            print('The end of the path:', end)
            print('The stack at start', stack, '\n')
        # Set up visited list and start DFS for the nodes
        visited: list[Node] = [start]
        curr: Node = Node(0, 0)
        prev: Node = Node(0, 0)
        while stack:
            if stack[0] == start:
                current = stack.pop()
                curr = current[1]
                stack.extend(self._getNextNodes(curr, '.', visited, listInput))
                continue
            current = stack.pop()
            curr = current[1]
            prev = current[0]
            if listInput[curr.y][curr.x] in ['<', '>', '^', 'v'] or listInput[prev.y][prev.x] in ['<', '>', '^', 'v']:
                self.addDirectedEdge(prev, curr)
            else:
                self.addEdge(prev, curr)
            visited.append(curr)
            stack.extend(self._getNextNodes(curr, listInput[curr.y][curr.x], visited, listInput))
        # Remove connection to self from the start node and connection to previous from end node
        self.adjacent[start] = [item for item in self.adjacent[start] if item != start]
        self.adjacent[end].clear()
        # Store start and end as instance properties
        self.start = start
        self.end = end
        # Debug message to check the completed graph
        if self.debug:
            print('')
            print('The complete graph:\n')
            self.displayAdjacencyList()
            print('')

    def _getNextNodes(self, current: Node, direction: str, visited: list[Node], listInput: list[list[str]]) -> list[tuple[Node, Node]]:
        '''Private method to get all possible next nodes'''
        nextNodes: list[tuple[Node, Node]] = []
        if direction == '^' and current.y > 0:
            if listInput[current.y - 1][current.x] in ['.', '<', '>', '^', 'v'] and Node(current.x, current.y - 1) not in visited:
                nextNodes.append((current, Node(current.x, current.y - 1)))
        elif direction == 'v' and current.y < len(listInput) - 1:
            if listInput[current.y + 1][current.x] in ['.', '<', '>', '^', 'v'] and Node(current.x, current.y + 1) not in visited:
                nextNodes.append((current, Node(current.x, current.y + 1)))
        elif direction == '<' and current.x > 0:
            if listInput[current.y][current.x - 1] in ['.', '<', '>', '^', 'v'] and Node(current.x - 1, current.y) not in visited:
                nextNodes.append((current, Node(current.x - 1, current.y)))
        elif direction == '>' and current.x < len(listInput[0]) - 1:
            if listInput[current.y][current.x + 1] in ['.', '<', '>', '^', 'v'] and Node(current.x + 1, current.y) not in visited:
                nextNodes.append((current, Node(current.x + 1, current.y)))
        else:
            if current.y > 0:
                if listInput[current.y - 1][current.x] in ['.', '<', '>', '^', 'v'] and Node(current.x, current.y - 1) not in visited:
                    nextNodes.append((current, Node(current.x, current.y - 1)))
            if current.y < len(listInput) - 1:
                if listInput[current.y + 1][current.x] in ['.', '<', '>', '^', 'v'] and Node(current.x, current.y + 1) not in visited:
                    nextNodes.append((current, Node(current.x, current.y + 1)))
            if current.x > 0:
                if listInput[current.y][current.x - 1] in ['.', '<', '>', '^', 'v'] and Node(current.x - 1, current.y) not in visited:
                    nextNodes.append((current, Node(current.x - 1, current.y)))
            if current.x < len(listInput) - 1:
                if listInput[current.y][current.x + 1] in ['.', '<', '>', '^', 'v'] and Node(current.x + 1, current.y) not in visited:
                    nextNodes.append((current, Node(current.x + 1, current.y)))
        if self.debug:
            print('For node', current, 'the next nodes:', nextNodes)
        return nextNodes 


def parse_input(filename: str, debug: bool=False) -> Graph | None:
    '''Parse the input file'''
    rawInput: list[str] = []
    with open(filename, 'r') as f:
        rawInput = f.read().splitlines()

    if debug:
        print('The raw input:\n')
        pprint(rawInput)
        print('')

    listInput: list[list[str]] = []
    for line in rawInput:
        listInput.append(list(line))

    if debug:
        print('The raw input transformed into [][]\n')
        pprint(listInput, width=400)
        print('')

    nodeNum: int = 0
    for line in listInput:
        nodeNum += (
            line.count('.') +
            line.count('>') +
            line.count('<') +
            line.count('^') +
            line.count('v')
        )

    if debug:
        print('The number of nodes:', nodeNum, '\n')

    graph: Graph = Graph(nodeNum, debug)
    graph.buildGraph(listInput)

    return graph


def part_1(input: Graph, debug=False) -> int:
    '''Solve Part 1'''

    return 0


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
