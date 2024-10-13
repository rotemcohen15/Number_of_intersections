import sys
from convert_input import *
from utilities import *
from avl_tree import *


def number_of_intersections(set: TestSet):
    # Initialize event queue
    eq = EventQueue()

    def check_intersection_add_to_queue(segment1: Segment, segment2: Segment):
        intersect_point = intersection(segment1, segment2)
        if intersect_point and intersect_point.x > status.curr_x:
            new_event = Event([segment1.id, segment2.id], intersect_point, EventType.INTERSECT)
            eq.insert(new_event)

    for seg in set.segments:
        start = Event([seg.id], seg.p, EventType.START)
        end = Event([seg.id], seg.q, EventType.END)
        eq.insert(start)
        eq.insert(end)

    # Initialize status
    status = AVLSegmentTree(eq.min().point.x-1)
    root = None
    num_of_inter = 0

    last_event = None
    while not eq.empty():
        event = eq.pop()

        status.curr_x = event.point.x
        
        if event.event_type == EventType.START:
            segment = set.segments[event.segment_ids[0]]

            # Add to status
            root = status.insert(root, segment)

            # Find new couples of segments in status - successor and predecessor of new segment, and add to queue the intersections
            predecessor_node = status.find_predecessor(root, segment)
            if predecessor_node:
                check_intersection_add_to_queue(predecessor_node.segment, segment)

            successor_node = status.find_successor(root, segment)
            if successor_node:
                check_intersection_add_to_queue(segment, successor_node.segment)
            
        elif event.event_type == EventType.INTERSECT:
            # Prevent double counting of intersections
            if last_event.event_type == EventType.INTERSECT and last_event.point == event.point:
                continue

            segment1, segment2 = set.segments[event.segment_ids[0]], set.segments[event.segment_ids[1]]
            num_of_inter += 1

            # Save potential segments to have new intersections
            predecessor_node, successor_node = status.find_predecessor(root, segment1), status.find_successor(root, segment2)

            # Swap the segments in nodes
            status.swap_node_segments(root, segment1, segment2)

            # Find new couples of segments in status - successor and predecessor of the segments, and add to queue the intersections
            # Because the AVL tree is in a "special" status in the intersection point, the predecessor and successor might be the segment itself
            # In that situation, we can find the predecessor and successor after swapping
            if predecessor_node and predecessor_node.segment.id == segment1.id:
                predecessor_node = status.find_predecessor(root, segment2)
            if predecessor_node:
                check_intersection_add_to_queue(predecessor_node.segment, segment2)
            if successor_node and successor_node.segment.id == segment2.id:
                    successor_node = status.find_successor(root, segment1)
            if successor_node:
                check_intersection_add_to_queue(segment1, successor_node.segment)
        
        elif event.event_type == EventType.END:
            segment = set.segments[event.segment_ids[0]]

            # Find successor and predecessor of the ending segment - potentially to have an intersection point
            predecessor_node, successor_node = status.find_predecessor(root, segment), status.find_successor(root, segment)

            # Delete segment from status
            root = status.delete(root, segment)

            # Check intersection and add to queue
            if predecessor_node and successor_node:
                check_intersection_add_to_queue(predecessor_node.segment, successor_node.segment)
        
        last_event = event

    return num_of_inter


def main():
    lines = []
    for line in sys.stdin:
        if line.rstrip() == '-1':
            break
        lines.append(line.rstrip())

    res, test_sets = convert_input_to_testsets(lines)
    if res != None:
        print("\nError: " , res)
        return
    
    i = 0
    for set in test_sets:
        print(str(number_of_intersections(set)))
        i += 1
        

if __name__ == "__main__":
    main()
