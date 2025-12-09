#!/bin/env python3

"""day8.py - Advent of Code 2025 - Day 8."""

from util import *


def parse(input):
    return [tuple(map(int, line.strip().split(","))) for line in input]


TEST = parse(open("test/8.txt", "r").readlines())
INPUT = parse(open("input/8.txt", "r").readlines())


def distance(p1, p2):
    (x1, y1, z1) = p1
    (x2, y2, z2) = p2
    return (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2


def compute_distances(points):
    t = {}
    for p1 in points:
        for p2 in points:
            if p1 < p2 and (p1, p2) not in t:
                t[(p1, p2)] = distance(p1, p2)
    return t


def pairs_by_dist(table):
    """Returns a list of (p1, p2) sorted with distances increasing."""
    table = list(table.items())
    table.sort(key=lambda e: e[1])
    table.reverse()
    return [t[0] for t in table]


def find_circuit(circuits, p):
    for i, c in enumerate(circuits):
        if p in c:
            return i
    return None


def join(circuits, p1, p2):
    c1 = find_circuit(circuits, p1)
    c2 = find_circuit(circuits, p2)

    if c1 != None and c2 != None:
        if c1 != c2:
            circuits[c1].update(circuits[c2])
            del circuits[c2]
    elif c1 != None and c2 == None:
        circuits[c1].add(p2)
    elif c1 == None and c2 != None:
        circuits[c2].add(p1)
    elif c1 == None and c2 == None:
        circuits.append(set([p1, p2]))


def part1(points, steps):
    table = compute_distances(points)
    ordered = pairs_by_dist(table)
    circuits = []

    for _ in range(steps):
        (p1, p2) = ordered.pop()
        join(circuits, p1, p2)

    circuits.sort(key=len, reverse=True)
    return product(len(c) for c in circuits[:3])


# print("part 1:", part1(INPUT, 10))
print("part 1:", part1(INPUT, 1000))


def count_points(circuits):
    return sum(len(c) for c in circuits)


def part2(points):
    table = compute_distances(points)
    ordered = pairs_by_dist(table)
    circuits = []

    p1, p2 = points[0], points[0]
    while count_points(circuits) < len(points):
        (p1, p2) = ordered.pop()
        join(circuits, p1, p2)

    return p1[0] * p2[0]


print("part 2:", part2(INPUT))
