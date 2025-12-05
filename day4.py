#!/bin/env python3

"""day4.py - Advent of Code 2025 - Day 4."""


def parse(input):
    return list(map(list, input))


TEST = parse(open("test/4.txt", "r").readlines())
INPUT = parse(open("input/4.txt", "r").readlines())

ROLL = "@"
EMPTY = "."


def at(grid, coord):
    (x, y) = coord
    return grid[y][x]


def set(grid, coord, value):
    (x, y) = coord
    old = grid[y][x]
    grid[y][x] = value
    return old


def coords(grid):
    for x in range(len(grid[0])):
        for y in range(len(grid)):
            yield (x, y)


def adjacent(coord, grid):
    (x, y) = coord
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if (
                x + dx >= 0
                and y + dy >= 0
                and x + dx < len(grid[0])
                and y + dy < len(grid)
                and not (dx == 0 and dy == 0)
            ):
                yield (x + dx, y + dy)


def is_accessible(grid, coord):
    if at(grid, coord) == ROLL:
        count = 0
        for adj in adjacent(coord, grid):
            if at(grid, adj) == ROLL:
                count += 1
        return count < 4


def count_accessible_rolls(grid):
    count = 0
    for coord in coords(grid):
        if is_accessible(grid, coord):
            count += 1
    return count


def part1(input):
    return count_accessible_rolls(input)


def remove_accessible_rolls(grid):
    count = 0
    for coord in coords(grid):
        if is_accessible(grid, coord):
            count += 1
            set(grid, coord, EMPTY)
    return count


def part2(input):
    removed = 0
    while True:
        new = remove_accessible_rolls(input)
        removed += new
        if new == 0:
            return removed


print("part 1:", part1(INPUT))
print("part 2:", part2(INPUT))
