#!/usr/bin/env python

import sys
from pprint import pprint


def get_input(filename):
    """Get input from file and store it in a list of dicts"""
    input = []
    game = {}
    id = 0 
    sets = []
    with open(filename, "r") as input_file:
        for line in input_file:
            line = line.strip().replace("\n", "").removeprefix("Game ")
            id = get_id(line)
            idx = line.index(":")
            line = line[idx+1:]
            sets = get_sets(line)
            game["id"] = id
            game["sets"] = sets
            input.append(game.copy())
    return input


def get_id(line):
    """Get the game ID for the current line"""
    try:
        idx = line.index(":") 
    except ValueError:
        print("Couldn't find substring ':'")
        sys.exit(2)
    id = int(line[0:idx])
    return id


def get_sets(line):
    """Get the game sets from the current line"""
    sets = []
    while line != "":
        current_set = {"red": 0, "green": 0, "blue": 0}
        try:
            idx = line.index(";")
        except ValueError:
            idx = len(line)
        number = 0
        words = line[:idx].replace(",", "").split()
        for word in words: 
            if word.isnumeric():
                number = int(word)
            elif word == "red":
                current_set["red"] = number
            elif word == "green":
                current_set["green"] = number
            elif word == "blue":
                current_set["blue"] = number
        line = line[idx+1:]
        sets.append(current_set.copy())
    return sets


def part_1(input):
    """Get the answer to the question for Part 1"""
    constraint = {"red": 12, "green": 13, "blue": 14}
    sum = 0
    for game in input:
        possible = True
        for current_set in game["sets"]:
            if current_set["red"] > constraint["red"] or \
               current_set["green"] > constraint["green"] or \
               current_set["blue"] > constraint["blue"]:
                possible = False
        if possible:
            sum += game["id"]
    return sum


def part_2(input):
    """Get the answer to the question for Part 2"""
    sum = 0
    for game in input:
        red = []
        green = []
        blue = []
        min_red = 0
        min_green = 0
        min_blue = 0
        for sets in game["sets"]:
            red.append(sets.get("red"))
            green.append(sets.get("green"))
            blue.append(sets.get("blue"))
        min_red = max(red)
        min_green = max(green)
        min_blue = max(blue)
        sum += (min_red * min_green * min_blue)
    return sum


def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("USAGE: ./day2.py input.txt")
        sys.exit(1)
    input = get_input(sys.argv[1])
    pprint(input)
    print("")
    sum = part_1(input)
    print("For Part 1, the sum of the possible games' IDs is:", sum)
    sum_of_powers = part_2(input)
    print("For Part 2, the sum of the powers of the minimum sets is:", 
          sum_of_powers)
    print("")
    sys.exit(0)


if __name__ == "__main__":
    main()

