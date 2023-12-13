#!/usr/bin/env python

import sys

def parse_input(filename):
    '''Parse the input file'''
    with open(filename,'r') as f:
        input = f.read()

    input = input.splitlines()
    print(input)
    parsed = []
    for item in input:
        parts = item.split(' ')
        print(parts)
        parsed.append((parts[0], int(parts[1])))
    print(parsed)
    return parsed


def main():
    '''Main function'''
    parsed = parse_input(sys.argv[1])
    sys.exit(0)


if __name__ == "__main__":
    main()
