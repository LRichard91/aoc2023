#!/usr/bin/env python

import sys


STRENGTH_1 = "AKQJT98765432"
STRENGTH_2 = "AKQT98765432J"


def parse_input(filename, debug=False):
    '''Parse the input file'''
    with open(filename,'r') as f:
        input = f.read()

    input = input.splitlines()
    if debug:
        print('')
        print('The raw input:')
        print(input)
        print('')
    parsed = []
    for item in input:
        parts = item.split(' ')
        parsed.append((parts[0], int(parts[1])))
    if debug:
        print('The parsed input (matches as list of tuples):')
        print(parsed)
        print('')
    return parsed


def sort_hands_1(lst):
    '''Sort the hands in a given list by order of strength (ascending)'''
    sorted_lst = sorted(lst, key=lambda x: [STRENGTH_1.index(card[0]) for card in x[0]], reverse=True)
    return sorted_lst


def sort_hands_2(lst):
    '''Sort the hands in a given list by order of strength (ascending)'''
    sorted_lst = sorted(lst, key=lambda x: [STRENGTH_2.index(card[0]) for card in x[0]], reverse=True)
    return sorted_lst


def part_1(parsed_input, debug=False):
    '''Solve Part 1'''
    five = []
    four = []
    full = []
    three = []
    tpair = []
    pair = []
    high = []

    for item in parsed_input:
        found = []
        prev_tested = ''
        counter1 = 1
        counter2 = 1
        for card in item[0]:
            if card not in found:
                found.append(card)
            elif prev_tested == '':
                prev_tested = card
                counter1 += 1
            elif card != prev_tested:
                counter2 += 1
            else:
                counter1 += 1

        # if debug:
        #     print('Match:', item)
        #     print('Matching cards:', counter1, counter2)
        #     print('')

        if counter1 == 5:
            five.append(item)
        elif counter1 == 4:
            four.append(item)
        elif counter1 == 3 and counter2 == 2 or counter1 == 2 and counter2 == 3:
            full.append(item)
        elif counter1 == 3:
            three.append(item)
        elif counter1 == 2 and counter2 == 2:
            tpair.append(item)
        elif counter1 == 2:
            pair.append(item)
        else:
            high.append(item)

    if debug:
        print('The hands matching the types:')
        print('Five of a kind:', five)
        print('Four of a kind:', four)
        print('Full house:', full)
        print('Three of a kind:', three)
        print('Two pairs:', tpair)
        print('One pair:', pair)
        print('High card:', high)
        print('')

    five = sort_hands_1(five)
    four = sort_hands_1(four)
    full = sort_hands_1(full)
    three = sort_hands_1(three)
    tpair = sort_hands_1(tpair)
    pair = sort_hands_1(pair)
    high = sort_hands_1(high)

    if debug:
        print('The hands matching the types (sorted):')
        print('Five of a kind:', five)
        print('Four of a kind:', four)
        print('Full house:', full)
        print('Three of a kind:', three)
        print('Two pairs:', tpair)
        print('One pair:', pair)
        print('High card:', high)
        print('')

    sorted_hands = high + pair + tpair + three + full + four + five

    if debug:
        print('All hands sorted by strenght (ascending):')
        print(sorted_hands)

    winnings = 0
    for idx, item in enumerate(sorted_hands):
        winnings += ((idx + 1) * item[1])
        if debug:
            print('Hand:', item, 'Rank:', idx + 1, 'Winning:', (idx + 1) * item[1])

    return winnings


def part_2(parsed_input, debug=False):
    '''Solve Part 2'''
    five = []
    four = []
    full = []
    three = []
    tpair = []
    pair = []
    high = []

    if debug:
        print('')
        print('====================================')
        print('|              Part 2              |')
        print('====================================')
        print('')
    for item in parsed_input:
        found = []
        matched = []
        jokers = 0
        high_counter = 0
        low_counter = 0
        for card in item[0]:
            if card not in found and card != 'J':
                found.append(card)
            elif card == 'J':
                jokers += 1
            elif card not in matched:
                matched.append(card)
                matched.append(card)
            else:
                matched.append(card)
        
        counted = []
        matches = []
        for card in matched:
            if card not in counted:
                counted.append(card)
                matches.append(matched.count(card))

        if len(matches) > 1:
            high_counter = max(matches)
            low_counter = min(matches)
        elif len(matches) == 1:
            high_counter = matches[0]
            low_counter = 0

        if debug:
            print("Hand:", item, "Matched:", matched, "High counter:", high_counter, "Low counter:", low_counter, "Jokers:", jokers)

        if high_counter > 0:
            high_counter += jokers 
        else:
            high_counter += jokers + 1 
            
        if high_counter == 5 or jokers == 5:
            five.append(item)
        elif high_counter == 4:
            four.append(item)
        elif high_counter == 3 and low_counter == 2:
            full.append(item)
        elif high_counter == 3:
            three.append(item)
        elif high_counter == 2 and low_counter == 2:
            tpair.append(item)
        elif high_counter == 2:
            pair.append(item)
        else:
            high.append(item)

    if debug:
        print('The hands matching the types:')
        print('Five of a kind:', five)
        print('Four of a kind:', four)
        print('Full house:', full)
        print('Three of a kind:', three)
        print('Two pairs:', tpair)
        print('One pair:', pair)
        print('High card:', high)
        print('')

    five = sort_hands_2(five)
    four = sort_hands_2(four)
    full = sort_hands_2(full)
    three = sort_hands_2(three)
    tpair = sort_hands_2(tpair)
    pair = sort_hands_2(pair)
    high = sort_hands_2(high)

    if debug:
        print('The hands matching the types (sorted):')
        print('Five of a kind:', five)
        print('Four of a kind:', four)
        print('Full house:', full)
        print('Three of a kind:', three)
        print('Two pairs:', tpair)
        print('One pair:', pair)
        print('High card:', high)
        print('')

    sorted_hands = high + pair + tpair + three + full + four + five

    if debug:
        print('All hands sorted by strenght (ascending):')
        print(sorted_hands)

    winnings = 0
    for idx, item in enumerate(sorted_hands):
        winnings += ((idx + 1) * item[1])
        if debug:
            print('Hand:', item, 'Rank:', idx + 1, 'Winning:', (idx + 1) * item[1])

    return winnings


def main():
    '''Main function'''
    # Check for correct use
    if len(sys.argv) == 2 and sys.argv[1] != '--debug':
        filename = sys.argv[1]
        debug = False
    elif len(sys.argv) == 3 and sys.argv[1] == '--debug':
        filename = sys.argv[2]
        debug = True
    else:
        print('USAGE: ./day7.py [--debug] <input.txt>')
        sys.exit(1)

    parsed = parse_input(filename, debug)
    part_1_solution = part_1(parsed, debug)
    part_2_solution = part_2(parsed, debug)
    
    print('')
    print('The solution for Part 1 is:', part_1_solution)
    print('')
    print('The solution for Part 2 is:', part_2_solution)
    print('')

    sys.exit(0)


if __name__ == "__main__":
    main()
