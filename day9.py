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


def candidates(points):
    for p1 in points:
        for p2 in points:
            if p1 != p2:
                yield (p1, p2)


def part1(points):
    return max(area(*box) for box in candidates(points))


print("part 1:", part1(TEST))


def boxes_by_area(points):
    areas = [(area(p1, p2), (p1, p2)) for (p1, p2) in candidates(points)]
    return [a[1] for a in sorted(areas, reverse=True)]


def box_to_points(box):
    ((x1, y1), (x2, y2)) = box
    for x in range(min(x1, x2), max(x1, x2) + 1):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            yield (x, y)


def on_edge(point, edge):
    px, py = point

    ((x1, y1), (x2, y2)) = edge

    if px == x1 and px == x2 and min(y1, y2) <= py and py <= max(y1, y2):
        return True
    elif py == y1 and py == y2 and min(x1, x2) <= px and px <= max(x1, x2):
        return True
    else:
        return False


def point_in_polygon(point, polygon):
    """https://en.wikipedia.org/wiki/Point_in_polygon"""

    px, py = point

    # we'll say our ray is is pointing to left.

    intersections = 0
    for edge in polygon_edges(polygon):
        ((x1, y1), (x2, y2)) = edge
        # On an edge means included in the polygon
        if on_edge(point, edge):
            return True

        # check intersections on edges lines to the point's left.
        # I'm not sure this is right???
        if x1 < px and x2 < px:
            # does the height of the ray to the left go between the line's top
            # an bottom points?
            if min(y1, y2) <= py and py <= max(y1, y2):
                intersections += 1

    # odd means inside
    return (intersections % 2) == 1


def polygon_edges(points):
    for i in range(len(points) - 1):
        yield points[i], points[i + 1]

    # and it loops back around to close
    yield (points[-1], points[0])


def box_in_polygon(box, polygon):
    """
    A box (represented as two corners) in inside another polygon (vertex
    list) when each point is 'inside' and edge of the box is does not intersect
    an edge of the polygon.
    """
    box_points = box_to_points(box)

    for point in box_points:
        if not point_in_polygon(point, polygon):
            return False

    return True


def compress_point(point, key):
    (x, y) = point
    return (key[0].index(x), key[1].index(y))


def compress(polygon):
    xs = list(sorted(map(lambda p: p[0], polygon)))
    ys = list(sorted(map(lambda p: p[1], polygon)))
    key = (xs, ys)

    poly = [compress_point(p, key) for p in polygon]

    return (poly, key)


def decompress(point, key):
    (x, y) = point
    return (key[0][x], key[1][y])


def part2(points):
    # Area is cheap, so we find and sort by largest area, and then find the
    # first one that's inside (expensive), so we only need to consider one
    # to success, instead of every possible box to find the largest area.

    (key, small) = compress(points)

    found = None
    for box in boxes_by_area(small):
        if box_in_polygon(box, small):
            found = box
            break

    if found:
        print(found)
        (p1, p2) = found
        return area(decompress(p1, key), decompress(p2, key))


print("part 2:", part2(TEST))
