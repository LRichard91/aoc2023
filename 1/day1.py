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
        word = word.lower()
        number = ""
        for char in range(len(word)):
            if word[char].isdigit():
                number += word[char]
            elif word[char:char+3] == "one":
                number += "1"
            elif word[char:char+3] == "two":
                number += "2"
            elif word[char:char+5] == "three":
                number += "3"
            elif word[char:char+4] == "four":
                number += "4"
            elif word[char:char+4] == "five":
                number += "5"
            elif word[char:char+3] == "six":
                number += "6"
            elif word[char:char+5] == "seven":
                number += "7"
            elif word[char:char+5] == "eight":
                number += "8"
            elif word[char:char+4] == "nine":
                number += "9"
            elif word[char:char+4] == "zero":
                number += "0"
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
