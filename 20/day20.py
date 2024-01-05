#!/usr/bin/env python

import argparse
from collections import deque
from pprint import pprint
import sys
from typing import Any

####################################################################################################################
# button -> broadcaster : when pushed, gives LOW pulse
# broadcaster -> [modules] : sends the received pulse to all connected modules
# %flip-flop -> module : default off, if gets HIGH -> ignore, if gets LOW -> flop and give HIGH if ON, LOW if OFF
# [modules] -> &conjuction -> module : remembers each input's pulse -> if all HIGH, sends LOW, otherwise HIGH
####################################################################################################################


LOW: int = 0
HIGH: int = 1

Mod = dict[str, Any]

class Machine:
    '''Superclass representing the machine's parts'''
    def __init__(self, mods: list[Mod]) -> None:
        self.modules: list = []
        for mod in mods:
            self.connectModule(mod)
        self.connectUpstreamModules()

    def connectModule(self, mod: Mod) -> None:
        if mod['type'] == 'bc':
            self.modules.append(Broadcaster(mod))
        elif mod['type'] == '%':
            self.modules.append(FlipFlop(mod))
        elif mod['type'] == '&':
            self.modules.append(Conjunction(mod))

    def connectUpstreamModules(self):
        for mod in self.modules:
            if mod.name != 'broadcaster':
                mod.connectUpstream(self)

    def getModules(self) -> list:
        return self.modules

    def pressButton(self, debug: bool=False) -> tuple[int, int]:
        '''Simulate pressing the button'''
        broadcasterIdx: int = 0
        for idx, item in enumerate(self.modules):
            if item.name == 'broadcaster':
                broadcasterIdx = idx
        queue: deque = deque(item for item in self.modules[broadcasterIdx].sendSignal(LOW))
        if debug:
            print('The initial queue:\n')
            pprint(queue)
            print('\n')
        low: int = 1
        high: int = 0
        while queue:
            sender, name, signal = queue.popleft()
            if signal == LOW:
                low += 1
            else:
                high += 1
            if debug:
                print('##########################################################')
                print('Sender:', sender, 'Receiver:', name, 'Signal:', signal)
                print('Nr. of LOW signals:', low, ', nr. of HIGH signals:', high)
                print('##########################################################')
                print('')
            for mod in self.modules:
                if mod.name == name:
                    new_signals = mod.sendSignal(sender, signal)
                    queue.extend(item for item in new_signals)
            if debug:
                print('The queue:\n')
                pprint(queue)
                print('\n')
        return (low, high)

    def pressButtonBool(self, debug: bool=False) -> bool:
        '''Simulate the button pressing for Part 2 -> return True if rx received Low pulse'''
        broadcasterIdx: int = 0
        for idx, item in enumerate(self.modules):
            if item.name == 'broadcaster':
                broadcasterIdx = idx
        queue: deque = deque(item for item in self.modules[broadcasterIdx].sendSignal(LOW))
        if debug:
            print('The initial queue:\n')
            pprint(queue)
            print('\n')
        while queue:
            sender, name, signal = queue.popleft()
            if debug:
                print('##########################################################')
                print('Sender:', sender, 'Receiver:', name, 'Signal:', signal)
                print('##########################################################')
                print('')
            if name == 'rx' and signal == LOW:
                if debug:
                    print('END CONDITION REACHED!')
                return True
            for mod in self.modules:
                if mod.name == name:
                    new_signals = mod.sendSignal(sender, signal)
                    queue.extend(item for item in new_signals)
            if debug:
                print('The queue:\n')
                pprint(queue)
                print('\n')
        return False


class Broadcaster:
    '''Class representing the broadcaster module'''
    def __init__(self, mod: Mod) -> None:
        self.name: str = 'broadcaster'
        self.sendTo: list[str] = mod['send']
        self.state: str = 'OFF'

    def sendSignal(self, signal: int) -> deque[tuple[str, str, int]]:
        self.state = 'ON'
        signals: deque[tuple[str, str, int]] = deque() 
        for name in self.sendTo:
            signals.append((self.name, name, signal))
        self.state = 'OFF'
        return signals


class FlipFlop:
    '''Class representing a flip-flop module'''
    def __init__(self, mod: Mod) -> None:
        self.name: str = mod['name']
        self.state: str = 'OFF'
        self.sendTo: list[str] = mod['send']
        self.receiveFrom: list[str] = []

    def connectUpstream(self, machine) -> None:
        for item in machine.getModules():
            if self.name in item.sendTo:
                self.receiveFrom.append(item.name)

    def sendSignal(self, sender: str, signal: int) -> deque[tuple[str, str, int]]:
        if sender not in self.receiveFrom:
            return deque()
        signals: deque[tuple[str, str, int]] = deque()
        if self.state == 'OFF' and signal == LOW:
            self.state = 'ON'
            for name in self.sendTo:
                signals.append((self.name, name, HIGH))
        elif self.state == 'ON' and signal == LOW:
            self.state = 'OFF'
            for name in self.sendTo:
                signals.append((self.name, name, LOW))
        return signals


class Conjunction:
    '''Class representing a conjunction module'''
    def __init__(self, mod: Mod) -> None:
        self.name: str = mod['name']
        self.sendTo: list[str] = mod['send']
        self.receiveFrom: list[str] = []
        self.state: dict[str, int] = {}

    def connectUpstream(self, machine) -> None:
        for item in machine.getModules():
            if self.name in item.sendTo:
                self.receiveFrom.append(item.name)
        self.state = {item: LOW for item in self.receiveFrom}

    def sendSignal(self, sender: str, signal: int) -> deque[tuple[str, str, int]]:
        if sender not in self.receiveFrom:
            return deque()
        signals: deque[tuple[str, str, int]] = deque()
        self.state[sender] = signal
        if all(self.state.values()) == HIGH:
            for name in self.sendTo:
                signals.append((self.name, name, LOW))
        else:
            for name in self.sendTo:
                signals.append((self.name, name, HIGH))
        return signals


def parse_input(filename, debug=False):
    '''Parse the input file'''
    parsed_input: list[Mod] = []
    with open(filename, 'r') as f:
        raw_input = f.read().splitlines()
    if debug:
        print('The raw input:\n')
        pprint(raw_input)
        print('')

    for item in raw_input:
        mod: Mod = Mod()
        if item[0] not in ['%', '&']:
            if item[:11] == 'broadcaster':
                mod['type'] = 'bc'
                mod['name'] = 'broadcaster'
                mod['send'] = item[15:].split(', ')
        elif item[0] == '%':
            mod['type'] = '%'
            mod['name'] = item[1:item.find('->') - 1]
            mod['send'] = item[item.find('->') + 3:].split(', ')
        elif item[0] == '&':
            mod['type'] = '&'
            mod['name'] = item[1:item.find('->') - 1]
            mod['send'] = item[item.find('->') + 3:].split(', ')
        parsed_input.append(mod)
    return parsed_input


def part_1(input, debug=False):
    '''Solve Part 1'''
    machine = Machine(input)
    if debug:
        print('The whole machine:\n')
        pprint(machine.getModules())
        print('')
        for mod in machine.getModules():
            print('Module type:', mod.__class__)
            print('Module name:', mod.name)
            print('Module state:', mod.state)
            print('Module sends to:', mod.sendTo)
            print('')
    pulses: list[tuple[int, int]] = []
    for _ in range(1000):
        pulses.append(machine.pressButton(debug))
    # pulses = machine.pressButton(debug)
    if debug:
        print('The whole machine:\n')
        pprint(machine.getModules())
        print('')
        for mod in machine.getModules():
            print('Module type:', mod.__class__)
            print('Module name:', mod.name)
            print('Module state:', mod.state)
            print('Module sends to:', mod.sendTo)
            print('')
    # total_pulses = pulses
    total_pulses = sum([x[0] for x in pulses]), sum([y[1] for y in pulses])
    if debug:
        print('\nThe total number of pulses:\n')
        print('LOW:', total_pulses[0], 'HIGH:', total_pulses[1])
        print('')
    return total_pulses[0] * total_pulses[1]


def part_2(input, debug=False):
    '''Solve Part 2'''
    machine = Machine(input)
    if debug:
        print('The whole machine:\n')
        pprint(machine.getModules())
        print('')
        for mod in machine.getModules():
            print('Module type:', mod.__class__)
            print('Module name:', mod.name)
            print('Module state:', mod.state)
            print('Module sends to:', mod.sendTo)
            print('')
    button_presses: int = 0
    rxReceivedLow: bool = False
    while not rxReceivedLow:
        button_presses += 1
        rxReceivedLow = machine.pressButtonBool(debug)
        if debug:
            print('Nr. of button presses:', button_presses)
            print('rxReceivedLow:', rxReceivedLow)
            print('')
        if button_presses % 10_000 == 0:
            print('Progress:', button_presses, 'button presses')
    if debug:
        print('The whole machine:\n')
        pprint(machine.getModules())
        print('')
        for mod in machine.getModules():
            print('Module type:', mod.__class__)
            print('Module name:', mod.name)
            print('Module state:', mod.state)
            print('Module sends to:', mod.sendTo)
            print('')
    return button_presses


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
