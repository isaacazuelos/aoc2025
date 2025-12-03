#!/bin/env python3

"""day1.py - Advent of Code 2025 - Day 1."""

DIAL_MAX = 100
DIAL_START = 50


def parse(input):
    return list(map(lambda l: (l[0], int(l[1:])), input))


TEST = parse(open("test/1.txt", "r").readlines())
INPUT = parse(open("input/1.txt", "r").readlines())


def part1(input):
    dial = DIAL_START
    password = 0

    for dir, dist in input:
        if dir == "L":
            dial = (dial - dist) % DIAL_MAX
        else:
            dial = (dial + dist) % DIAL_MAX

        password += int(dial == 0)

    return password


def part2(input):
    dial = DIAL_START
    clicks = 0

    for dir, dist in input:
        for _ in range(dist):
            if dir == "L":
                dial = (dial - 1) % DIAL_MAX
            else:
                dial = (dial + 1) % DIAL_MAX

            clicks += int(dial == 0)

    return clicks


print("part 1:", part1(INPUT))
print("part 2:", part2(INPUT))
