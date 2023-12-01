#!/usr/bin/env python

import sys


def main():
    """Main function"""
    input = []
    with open("input.txt", "r") as inputfile:
        for row in inputfile:
            input.append(row.replace("\n", ""))

    sum = 0
    for word in input:
        number = ""
        for char in word:
            if char.isdigit():
                number += char
        if len(number) == 2:
            number = int(number)
        elif len(number) == 1:
            number = int(number + number)
        else:
            length = len(number)
            number = int(number[:1] + number[length - 1:])
        sum += number

    print("The calibration SUM is:", sum)
    sys.exit(0)


if __name__ == "__main__":
    main()
