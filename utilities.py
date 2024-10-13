from enum import Enum

class Point:
    x : float
    y : float
    
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y)


class Segment:
    id : int # to overcome numerical error when we find a point on an ...
    #    # already-known segment we identify segments with unique ID.
    #    # binary search with numerical errors is guaranteed to find an ...
    #    # index whose distance from the correct one is O(1) (here it is 2).
    #
    p : Point # Point, after input we compare and swap to guarantee that p.x <= q.x
    q : Point # Point
    
    def __init__(self,id,p,q):
        self.id = id
        if p.x > q.x:
            p,q = q,p
        self.p = p
        self.q = q
        self.last_y = p.y

    
    # line: y = ax + b. it is guaranteed that the line is not vertical (a is finite)
    def a(self): # () -> float
        return ((self.p.y - self.q.y) / (self.p.x - self.q.x))

    
    def b(self): # () -> float
        return (self.p.y - (self.a() * self.p.x))

    
    # the y-coordinate of the point on the segment whose x-coordinate ..
    #   is given. Segment boundaries are NOT enforced here.
    def get_y(self, x):
        return self.a() * x + self.b()

    
class TestSet:
    segments: list # of Segment
    def __init__(self, segments: list):
        self.segments = segments


def is_left_turn(a: Point, b: Point, c: Point): # (Point,Point,Point) -> bool
    x1 = a.x
    x2 = b.x
    x3 = c.x
    y1 = a.y
    y2 = b.y
    y3 = c.y
    return ((x1 * (y2 - y3)) + (x2 * (y3 - y1)) + (x3 * (y1 - y2))) > 0


def intersection(s1: Segment, s2: Segment):
    if ((is_left_turn(s1.p, s1.q, s2.p) != is_left_turn(s1.p, s1.q, s2.q)) and
        (is_left_turn(s2.p, s2.q, s1.p) != is_left_turn(s2.p, s2.q, s1.q))):
        
        a1 = s1.a()
        a2 = s2.a()

        b1 = s1.b()
        b2 = s2.b()

        # commutation consistency: sort by a (then by b)
        if a1 > a2 or (a1 == a2 and b1 > b2):
            a1,a2 = a2,a1
            b1,b2 = b2,b1

        x = (b2 - b1) / (a1 - a2)
        y = a1 * x + b1

        # check the limits
        if x >= s1.p.x and x <= s1.q.x and x >= s2.p.x and x <= s2.q.x:
            return Point(x, y)
    else:
        return None


class EventType(Enum):
    START = 1
    INTERSECT = 2
    END = 3
    
class Event:
    segment_ids: list 
    point: Point
    event_type: EventType

    def __init__(self, segment_ids, point, event_type):
        self.segment_ids = segment_ids
        self.point = point
        self.event_type = event_type
    
# e1 < e2 -> -1, e1 > e2 -> 1, e1 == e2 -> 0
def compare_events(e1, e2):
    if e1.point.x != e2.point.x:
        return 1 if e1.point.x > e2.point.x else -1
    if e1.point.y != e2.point.y:
        return 1 if e1.point.y > e2.point.y else -1
    if e1.event_type != e2.event_type:
        return 1 if e1.event_type.value > e2.event_type.value else -1
    return 0


class EventQueue:
    def __init__(self):
        self.t    = 0
        self.arr  = [0] # of events
        self.size = 0


    def sift_up(self, i):
        parent = i // 2
        while parent > 0 and compare_events(self.arr[i], self.arr[parent]) == -1:
            self.arr[i], self.arr[parent] = self.arr[parent], self.arr[i]
            i = parent
            parent = parent // 2
    

    def sift_down(self, i):
        while 2*i <= self.size:
            min_index = self.min_leaf_index(i)
            if not min_index:
                return
            if compare_events(self.arr[i], self.arr[min_index]) == 1:
                self.arr[i], self.arr[min_index] = self.arr[min_index], self.arr[i]
            i = min_index


    def min_leaf_index(self, i):
        if 2*i > self.size:
            return None
        elif 2*i+1 > self.size:
            return 2*i
        else:
            left_event = self.arr[2*i]
            right_event = self.arr[2*i+1]
            if compare_events(left_event, right_event) == -1:
                return 2*i
            return 2*i+1


    def insert(self, event: Event):
        self.t += 1
        self.arr.append(event)
        self.size += 1
        self.sift_up(self.size)
         

    def empty(self): # () -> bool
        return self.size == 0
    

    def pop(self): # () -> any
        if self.size == 0:
            return None
        
        res = self.arr[1]

        self.arr[1] = self.arr[self.size]
        self.arr.pop()
        self.size -= 1

        if self.size > 1:
            self.sift_down(1)

        return res
    

    def min(self):
        if self.size == 0:
            return None
        
        return self.arr[1]
