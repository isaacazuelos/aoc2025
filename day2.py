#!/bin/env python3

"""day1.py - Advent of Code 2025 - Day 1."""


def parse(input: str):
    ranges = []
    for range in input.split(","):
        [s, e] = list(range.split("-"))
        ranges.append((int(s), int(e)))
    return ranges


TEST = parse(open("test/2.txt", "r").read())
INPUT = parse(open("input/2.txt", "r").read())


def is_valid(n):
    s = str(n)
    if len(s) % 2:
        return False

    l = len(s) // 2
    return s[:l] == s[l:]


def part1(input):
    acc = 0

    for s, e in input:
        for n in range(s, e + 1):
            if is_valid(n):
                acc += n

    return acc


def is_invalid(n):
    s = str(n)
    l = len(s)

    for pl in range(1, l):
        prefix = s[:pl]

        if prefix * int(l // pl) == s:
            return True

    return False


def part2(input):
    acc = 0

    for s, e in input:
        for n in range(s, e + 1):
            if is_invalid(n):
                acc += n

    return acc


print("part 1:", part1(INPUT))
print("part 2:", part2(INPUT))
