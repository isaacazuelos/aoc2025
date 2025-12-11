//! Just wanted to see how much faster this was, and it's about 40 seconds
//! to Python's 72 minutes, so about 108x faster.

use std::{collections::HashSet, hash::Hash};

#[allow(unused)]
const TEST: &str = include_str!("../../../test/9.txt");
const INPUT: &str = include_str!("../../../input/9.txt");

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
struct Point {
    x: u64,
    y: u64,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
struct Box(Point, Point);

#[derive(Debug, Clone)]
struct Polygon {
    points: Vec<Point>,
    known_inside: HashSet<Point>,
}

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
struct Key {
    xs: Vec<u64>,
    ys: Vec<u64>,
}

impl Polygon {
    fn parse(input: &str) -> Polygon {
        Polygon {
            known_inside: HashSet::new(),
            points: input
                .lines()
                .map(|l| {
                    let (xs, ys) = l.split_once(",").unwrap();
                    let x: u64 = xs.parse().unwrap();
                    let y: u64 = ys.parse().unwrap();
                    Point { x, y }
                })
                .collect(),
        }
    }

    fn compress(&self) -> (Polygon, Key) {
        let mut xs: Vec<u64> = self.points.iter().map(|p| p.x).to_owned().collect();
        xs.sort();
        xs.dedup();

        let mut ys: Vec<u64> = self.points.iter().map(|p| p.y).to_owned().collect();
        ys.sort();
        ys.dedup();

        let key = Key { xs, ys };
        let poly = Polygon {
            points: self.points.iter().map(|p| p.compress(&key)).collect(),
            known_inside: HashSet::new(),
        };

        (poly, key)
    }

    fn candidates(&self) -> Vec<Box> {
        let mut v = Vec::new();
        for p1 in &self.points {
            for p2 in &self.points {
                if p1 != p2 {
                    v.push(Box(*p1, *p2))
                }
            }
        }
        v
    }

    fn boxes_by_area(&self) -> Vec<Box> {
        let mut areas: Vec<(u64, Box)> = self
            .candidates()
            .into_iter()
            .map(|b| (b.area(), b))
            .collect();

        areas.dedup();
        areas.sort();
        areas.reverse();
        areas.into_iter().map(|t| t.1).collect()
    }

    fn contains_box(&mut self, b: Box) -> bool {
        for x in b.0.x.min(b.1.x)..=b.0.x.max(b.1.x) {
            for y in b.0.y.min(b.1.y)..=b.0.y.max(b.1.y) {
                if !self.contains(Point { x, y }) {
                    return false;
                }
            }
        }
        true
    }

    fn contains(&mut self, p: Point) -> bool {
        if self.known_inside.contains(&p) {
            return true;
        }

        // # we'll say our ray is is pointing to left.
        let mut intersections = 0;

        for (p1, p2) in self.edges() {
            if p.is_on(*p1, *p2) {
                return true;
            }

            if p1.x <= p.x && p2.x <= p.x && p1.y.min(p2.y) <= p.y && p.y <= p1.y.max(p2.y) {
                intersections += 1;
            }
        }

        if (intersections % 2) == 1 {
            self.known_inside.insert(p);
            true
        } else {
            false
        }
    }

    fn edges(&self) -> impl Iterator<Item = (&Point, &Point)> {
        self.points.iter().cycle().skip(1).zip(self.points.iter())
    }
}

impl Box {
    fn area(self) -> u64 {
        let width = (self.0.x).abs_diff(self.1.x) + 1;
        let height = (self.0.y).abs_diff(self.1.y) + 1;
        width * height
    }

    fn compress(&self, key: &Key) -> Box {
        Box(self.0.compress(key), self.1.compress(key))
    }

    fn decompress(&self, key: &Key) -> Box {
        Box(self.0.decompress(key), self.1.decompress(key))
    }
}

impl Point {
    fn compress(&self, key: &Key) -> Point {
        Point {
            x: key.xs.iter().position(|&k| k == self.x).unwrap() as u64,
            y: key.ys.iter().position(|&k| k == self.y).unwrap() as u64,
        }
    }

    fn decompress(&self, key: &Key) -> Point {
        Point {
            x: key.xs[self.x as usize],
            y: key.ys[self.y as usize],
        }
    }

    fn is_on(&self, p1: Point, p2: Point) -> bool {
        let Point { x: x1, y: y1 } = p1;
        let Point { x: x2, y: y2 } = p2;

        if self.x == x1 && self.x == x2 && y1.min(y2) <= self.y && self.y <= y1.max(y2) {
            return true;
        }
        if self.y == y1 && self.y == y2 && x1.min(x2) <= self.x && self.x <= x1.max(x2) {
            return true;
        }
        false
    }
}

fn day1(input: &str) -> u64 {
    Polygon::parse(input)
        .candidates()
        .into_iter()
        .map(Box::area)
        .max()
        .unwrap()
}

fn day2(input: &str) -> u64 {
    let polygon = Polygon::parse(input);
    let (mut small, key) = polygon.compress();

    let compressed_boxes: Vec<_> = polygon
        .boxes_by_area()
        .into_iter()
        .map(|b| b.compress(&key))
        .collect();

    let cbl = compressed_boxes.len();

    for (i, b) in compressed_boxes.into_iter().enumerate() {
        if (i % 1000) == 0 {
            let percent = i as f64 / cbl as f64 * 100.0;
            println!("at {i} of {cbl}, or {percent}%");
        }
        if small.contains_box(b) {
            return b.decompress(&key).area();
        }
    }

    0
}

fn main() {
    println!("day 1: {}", day1(INPUT));
    println!("day 2: {}", day2(INPUT));
}
