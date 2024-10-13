# A sweepline algorithm to find the number of line segment intersections
**Problem:** Given $n$ line segments, efficiently find the number of intersection points in $\mathcal{O}((n + k) log n)$ where $k$ is the number of intersections.

**Input:**
1. Number of tests
2. Number of segments in the current test
3. Pairs of segments in the format: x1 y1 x2 y2
4. -1
(See test.txt for example - 5 testsets, each one contains 60 segments in [0, 20]x[0,20])

**Output:** Number of intersection between the segments for each test case.

**Assumptions:**
1. Each intersection point is an intersection of exactly two segments.
2. There is no point of two events (intersection and start/end of a segment, or a startd and end of segment).
3. There are no overlapping segments.

This is a simple python implemintation of the sweepline algorithm from Computational Geometry Algorithms and Applications, 3rd Ed - de Berg et al.


Running example:
1. To generate an input file - use generate_segments.py:
   1. Modify number_of_sets (line 96) to change the number of test cases.
   2. Modify the parameters when calling the function generate_testset (line 99):
      1. n - number of segments to generate.
      2. min, max - the range of x and y values is [min, max].
   3. Run: python3 generate_segments.py > input.txt
2. To run the algorithm: python3 main.py < input.txt
3. Compare to the naive algorithm (time complexity - $\mathcal{O}(n^2)$ ): python3 naive.py < input.txt
         
