#!/usr/bin/env python

import pprint
import re
import sys


def get_input(filename):
    """Get the input from file and store it in a list"""
    with open(filename, "r") as in_file:
        input = []
        for line in in_file:
            input.append(line.strip().replace("\n", ""))
    print("The puzzle input is:")
    pprint.pprint(input)
    print("")
    return input


def get_positions(input):
    """Get the positions of numbers and symbols per line"""
    res_list = []
    for row in input:
        num = []
        sym = []
        for match in re.finditer(r'[0-9]+', row):
            num.append([int(match.group()), match.span()])
        for match in re.finditer(r'[^A-Za-z0-9\.]', row):
            sym.append([match.group(), match.span()])
        res_list.append({'num': num, 'sym': sym})
    print("The number and symbol positions are:")
    pprint.pprint(res_list)
    print("")
    return res_list


def get_adjacent(res_list):
    """Get the numbers that are adjacent to a symbol"""
    s = [[] for _ in range(len(res_list))] 
    e = [[] for _ in range(len(res_list))]
    s_ = [[] for _ in range(len(res_list))]
    e_ = [[] for _ in range(len(res_list))]
    adjacent = []
    # Note to self: there should be a way to do this just with list
    # comprehension or with map() -> SO FIGURE IT OUT!
    for index, row in enumerate(res_list):
        for item in row['num']:
            s[index].append(item[1][0])
            e[index].append(item[1][1])
        for item in row['sym']:
            s_[index].append(item[1][0])
            e_[index].append(item[1][1])
    print("Number starting positions (inclusive):")
    pprint.pprint(s)
    print("\nNumber ending positions (non-inclusive):")
    pprint.pprint(e)
    print("\nSymbol starting positions (inclusive)")
    pprint.pprint(s_)
    print("\nSymbol ending positions (non-inclusive):")
    pprint.pprint(e_)
    print("")
    # Merge start and end positions into lists of tuples
    num = [(i, s[i][j], e[i][j]) for i in range(len(s)) for j in range(len(s[i]))]
    sym = [(i, s_[i][j], e_[i][j]) for i in range(len(s_)) for j in range(len(s_[i]))]
    visited = [False for _ in range(len(num))]
    for m in sym:
        c_ = 0
        r_ = 0
        for i, n in enumerate(num):
            if r_ < n[0]:
                c_ = 0
            if n[0] == m[0]-1 or n[0] == m[0] or n[0] == m[0]+1:
                if m[1] >= n[1]-1 and m[1] <= n[2] and visited[i] == False:
                    visited[i] = True
                    adjacent.append(res_list[n[0]]['num'][c_][0])
            c_ += 1
            r_ = n[0]
    print("List of numbers adjacent to a symbol:")
    pprint.pprint(adjacent)
    print("")
    return adjacent


def get_gears(res_list):
    """Get the gears and gear ratios"""
    asterisk = []
    numbers = []
    for idx, item in enumerate(res_list):
        for i in item['sym']:
            if i[0] == '*':
                asterisk.append((idx, i[1][0], i[1][1]))
        for i in item['num']:
            numbers.append((idx, i[1][0], i[1][1]))
    visited = [False for _ in range(len(numbers))]
    gears = []
    for m in asterisk:
        adjacent = []
        c_ = 0
        r_ = 0
        for i, n in enumerate(numbers):
            if r_ < n[0]:
                c_ = 0
            if n[0] == m[0]-1 or n[0] == m[0] or n[0] == m[0]+1:
                if m[1] >= n[1]-1 and m[1] <= n[2] and visited[i] == False:
                    visited[i] = True
                    adjacent.append(res_list[n[0]]['num'][c_][0])
            c_ += 1
            r_ = n[0]
        if len(adjacent) == 2:
            gears.append(adjacent)
    print("The components of the gears' ratios are:")
    pprint.pprint(gears)
    print("")
    return gears 

def part_1(res_list):
    """Get the answer for Part 1"""
    result = 0
    adjacent = get_adjacent(res_list)
    result = sum(adjacent)
    return result


def part_2(res_list):
    """Get the answer for Part 2"""
    result = 0
    gears = get_gears(res_list)
    gear_ratios = [x * y for x, y in gears]
    print("The gear ratios are:")
    pprint.pprint(gear_ratios)
    print("")
    result = sum(gear_ratios)
    return result


def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("USAGE: ./day3.py input.txt")
        sys.exit(1)
    input = get_input(sys.argv[1])
    res_list = get_positions(input)
    part_1_result = part_1(res_list)
    part_2_result = part_2(res_list)
    print("\n")
    print("The result for Part 1 is:", part_1_result)
    print("")
    print("The result for Part 2 is:", part_2_result)
    sys.exit(0)


if __name__ == "__main__":
    main()

