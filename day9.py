#!/bin/env python3

"""day9.py - Advent of Code 2025 - Day 9."""

from util import *


def parse(input):
    return [tuple(map(int, r.split(","))) for r in input]


TEST = parse(open("test/9.txt", "r").readlines())
INPUT = parse(open("input/9.txt", "r").readlines())


def area(p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2
    length = abs(x1 - x2) + 1
    height = abs(y1 - y2) + 1
    return length * height


def part1(points):
    largest = 0
    # corners = points[0], points[0]
    for p1 in points:
        for p2 in points:
            a = area(p1, p2)
            if a > largest:
                # corners = p1, p2
                largest = a

    return largest


print("part 1:", part1(INPUT))


def part2(points):
    """
    So we want the largest square with red corners from before, which is inside
    the shape enclosed by the path.

    If we can tell if a point is inside or outside the shape? Does being able to
    do that mean we can tell if a box is enclosed? Convex shapes are weird.

    Is there a trick here with only the edges?

    Can we tell if a line segment is contained inside another? Yes.

    Is this true: If any edge of our box contains points which are not along the
    known edges of the shape, it's not on the shape or not maximal?

    If it's in the shape and not touching edges, it can be expanded -- that the
    idea for the maximal clause.

    It's too late to try this, or seriously consider it. G'night.
    """
    pass


print("part 2:", part2(TEST))
