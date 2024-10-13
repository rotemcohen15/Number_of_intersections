# A sweepline algorithm to find the number of line segment intersections
**Problem:** Given $n$ line segments, efficiently find the number of intersection points in $\mathcal{O}((n + k) log n)$ where $k$ is the number of intersections.

**Input:**
1. Number of tests
2. Number of segments in the current test
3. Pairs of segments in the format: x1 y1 x2 y2
4. -1

**Output:** Number of intersection between the segments for each test case.

This is a simple python implemintation 
Assumptions:
1. Each intersection point is an intersection of exactly two segments.
2. Each x value has at most one event (intersection point or a beginning or an end of a segment).
