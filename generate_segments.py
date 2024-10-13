import random
from utilities import *


def overlaps(s1: Segment, s2: Segment):
    if s1.a() == s2.a() and s1.b() == s2.b():
        if s1.p.x >= s2.p.x and s1.p.x <= s2.q.x:
            return True
        elif s2.p.x >= s1.p.x and s2.p.x <= s1.q.x:
            return True
    return False 


def print_to_stdout(set: TestSet):
    print(f"{len(set.segments)}")
    for segment in set.segments:
        print(f"{segment.p.x} {segment.p.y} {segment.q.x} {segment.q.y}")


# Generate segments in [min, max] X [min, max]
def generate_segment(min, max, id):
    p = Point(random.uniform(min, max), random.uniform(min, max))
    q = Point(random.uniform(min, max), random.uniform(min, max))
    while q.x == p.x:
        q = Point(random.uniform(min, max), random.uniform(min, max))

    return Segment(id, p, q)

def generate_segment_with_px(min, max, segment: Segment, id):
    p = Point(segment.p.x, random.uniform(min, max))
    while p.y == segment.p.y:
        p = Point(segment.p.x, random.uniform(min, max))
    q = Point(random.uniform(min, max), random.uniform(min, max))
    while q.x == p.x:
        q = Point(random.uniform(min, max), random.uniform(min, max))

    return Segment(id, p, q)

def generate_segment_with_qx(min, max, segment: Segment, id):
    q = Point(segment.q.x, random.uniform(min, max))
    while q.y == segment.q.y:
        q = Point(segment.q.x, random.uniform(min, max))

    p = Point(random.uniform(min, max), random.uniform(min, max))
    while q.x == p.x:
        p = Point(random.uniform(min, max), random.uniform(min, max))

    return Segment(id, p, q)

def generate_testset(n, min, max):
    segments = []

    for i in range(n):
        to_generate = True
        while to_generate:
            segment = generate_segment(min, max, i)

            # Check there are no two overlapping segments
            for j in range(i):
                if overlaps(segment, segments[j]):
                    to_generate = True
                    break
            to_generate = False
            segments.append(segment)

    for i in range(n):
        to_generate = True
        while to_generate:
            segment = generate_segment_with_px(min, max, segments[i], i+n)

            # Check there are no two overlapping segments
            for j in range(i+n):
                if overlaps(segment, segments[j]):
                    to_generate = True
                    break
            to_generate = False
            segments.append(segment)
    
    for i in range(n):
        to_generate = True
        while to_generate:
            segment = generate_segment_with_qx(min, max, segments[i], i+n)

            # Check there are no two overlapping segments
            for j in range(i+n):
                if overlaps(segment, segments[j]):
                    to_generate = True
                    break
            to_generate = False
            segments.append(segment)
    
    return TestSet(segments)


def main():
    number_of_sets = 5
    print(number_of_sets)
    for i in range(number_of_sets):
        testset = generate_testset(20, 0, 20)
        print_to_stdout(testset)
    print("-1")

if __name__ == "__main__":
    main()
