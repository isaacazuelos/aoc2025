#!/bin/env python3

"""day10.py - Advent of Code 2025 - Day 10."""

from util import *


def parse_seq(seq):
    return [int(item) for item in seq.split(",")]


def parse_goal(raw):
    return [c == "#" for c in raw]


def powerset(s):
    x = len(s)
    for i in range(1 << x):
        yield [s[j] for j in range(x) if (i & (1 << j))]


def parse(input):
    parsed = []

    for row in input:
        (raw_goal, rest) = row[1:-2].split("] (")
        (rest, raw_jolts) = rest.split(") {")

        jolts = parse_seq(raw_jolts)
        goal = parse_goal(raw_goal)
        buttons = [parse_seq(b) for b in rest.split(") (")]
        parsed.append((goal, buttons, jolts))

    return parsed


TEST = parse(open("test/10.txt", "r").readlines())
INPUT = parse(open("input/10.txt", "r").readlines())


def press(buttons, state):
    for button in buttons:
        for i in button:
            state[i] = not state[i]


def button_presses(machine):
    (goal, buttons, _) = machine
    smallest = len(buttons)
    for pressed in powerset(buttons):
        state = [False for i in goal]
        press(pressed, state)
        if state == goal and smallest > len(pressed):
            smallest = len(pressed)

    return smallest


def part1(input):
    # I think the key here is that we'll never need to push a button twice so we
    # can just look at the power set of buttons to find combinations that work.
    return sum(button_presses(m) for m in input)


print("part 1:", part1(INPUT))


def part2(input):
    pass


print("part 2:", part2(TEST))
