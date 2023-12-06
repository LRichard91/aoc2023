#!/usr/bin/env python

import pprint
import sys


def get_input(filename):
    """Get puzzle input from file"""

    with open(filename, "r") as f:
        input = []
        for line in f:
            input.append(line.strip().replace("\n", ""))
    print("The puzzle input is:\n")
    pprint.pprint(input)
    print("")
    return input


def parse_input(input):
    """Parse the input data"""
    parsed_input = []
    for line in input:
        d = {}
        d['id'] = 0
        d['win'] = []
        d['player'] = []
        line = line.removeprefix("Card ")
        idx = line.index(":")
        d['id'] = int(line[:idx])
        line = line[idx+2:]
        idx = line.index("|")
        for word in line[0:idx-1].split(" "):
            if word != '':
                d['win'].append(int(word))
        for word in line[idx+2:].split(" "):
            if word != '':
                d['player'].append(int(word))
        parsed_input.append(d)
    print("The parsed input is:\n")
    pprint.pprint(parsed_input)
    print("")
    return parsed_input


def part_1(input):
    """Get the solution for Part 1"""
    sum = 0
    for item in input:
        counter = 0
        for num in item['player']:
            if num in item['win']:
                counter += 1
        if counter >= 1:
            sum += (2 ** (counter - 1))
    return sum 


def part_2(input):
    """Get the solution for Part 2"""
    count = [1 for _ in input]
    for idx, item in enumerate(input):
        counter = 0
        for num in item['player']:
            if num in item['win']:
                counter += 1
        if idx + counter <= len(input):
            for i in range(1, counter + 1):
                count[idx + i] += count[idx] 
    return sum(count)


def main():
    if len(sys.argv) != 2:
        print("USAGE: ./day4.py input.txt")
        sys.exit(1)
    input = get_input(sys.argv[1])
    parsed_input = parse_input(input)
    part_1_solution = part_1(parsed_input)
    part_2_solution = part_2(parsed_input)
    print("\n")
    print("The solution for Part 1 is:", part_1_solution)
    print("")
    print("The solution for Part 2 is:", part_2_solution)
    return sys.exit(0)

if __name__ == "__main__":
    main()
