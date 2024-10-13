from utilities import *

class Node:
    def __init__(self, segment: Segment):
        self.segment = segment
        self.height = 1
        self.left = None
        self.right = None


class AVLSegmentTree:
    curr_x : float

    def __init__(self, curr_x):
        self.curr_x = curr_x


    def get_height(self, node: Node):
        if not node:
            return 0
        return node.height


    def get_balance(self, node: Node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)


    def right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x


    def left_rotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y


    # Return the new root
    def insert(self, node: Node, segment: Segment):
        if not node:
            return Node(segment)
        elif segment.get_y(self.curr_x) < (node.segment).get_y(self.curr_x):
            node.left = self.insert(node.left, segment)
        elif segment.get_y(self.curr_x) > (node.segment).get_y(self.curr_x):
            node.right = self.insert(node.right, segment)
        else: # error
            return node

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        balance = self.get_balance(node)

        # Left Left
        if balance > 1 and segment.get_y(self.curr_x) < (node.left.segment).get_y(self.curr_x):
            return self.right_rotate(node)

        # Right Right
        if balance < -1 and segment.get_y(self.curr_x) > (node.right.segment).get_y(self.curr_x):
            return self.left_rotate(node)

        # Left Right
        if balance > 1 and segment.get_y(self.curr_x) > (node.left.segment).get_y(self.curr_x):
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Right Left
        if balance < -1 and segment.get_y(self.curr_x) < (node.right.segment).get_y(self.curr_x):
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node


    def find_node_by_segment(self, root: Node, segment: Segment):
        if not root:
            return None
        if segment.get_y(self.curr_x) == root.segment.get_y(self.curr_x):
            return root
        elif segment.get_y(self.curr_x) < root.segment.get_y(self.curr_x):
            return self.find_node_by_segment(root.left, segment)
        else:
            return self.find_node_by_segment(root.right, segment)
    

    # For intersection - two segments with same coordinate
    # Two segments that intersect - one of them is the parent of the other one
    def find_two_nodes_by_segments(self, root: Node, segment1: Segment, segment2: Segment):
        if not root:
            return None, None
        
        node1, node2 = None, None

        # Case 1 - there is no numeric difference, so we find the heighst segments
        # Then we search for the second one in its children
        if segment1.get_y(self.curr_x) == segment2.get_y(self.curr_x):
            node1 = self.find_node_by_segment(root, segment1)
            if not node1:
                return None, None
            node_l = self.find_node_by_segment(node1.left, segment2)
            node_r = self.find_node_by_segment(node1.right, segment2)
            node2 = node_l if node_l else node_r
            if not node2:
                return None, None
        
        # Case 2 - there is a numeric difference, and the AVL tree might be a little not "accurate" at this point
        # We search for both segments, and if we can't find one of them - we search in the children of the one we did find
        else:
            node1 = self.find_node_by_segment(root, segment1)
            node2 = self.find_node_by_segment(root, segment2)
            if not node1 and not node2:
                return None, None
            if not node1:
                node_l = self.find_node_by_segment(node2.left, segment1)
                node_r = self.find_node_by_segment(node2.right, segment1)
                node1 = node_l if node_l else node_r
                if not node1:
                    return None, None
            if not node2:
                node_l = self.find_node_by_segment(node1.left, segment2)
                node_r = self.find_node_by_segment(node1.right, segment2)
                node2 = node_l if node_l else node_r
                if not node2:
                    return None, None
            
        # Return the segments by increasing order of y before intersection
        if node1.segment.id == segment1.id:
            return node1, node2
        return node2, node1


    # Delete by segment
    # Return the new root
    def delete(self, root: Node, segment: Segment):
        if not root:
            return root

        if segment.get_y(self.curr_x) < root.segment.get_y(self.curr_x):
            root.left = self.delete(root.left, segment)
        elif segment.get_y(self.curr_x) > root.segment.get_y(self.curr_x):
            root.right = self.delete(root.right, segment)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp

            # Node to delete has two children
            temp = self.min_segment_node(root.right)
            root.segment = temp.segment
            root.right = self.delete(root.right, temp.segment)

        if root is None:
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        balance = self.get_balance(root)

        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)

        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)

        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root


    def min_segment_node(self, node: Node):
        current = node
        while current.left:
            current = current.left
        return current

    
    def find_successor(self, root: Node, segment: Segment):
        successor = None
        while root:
            if root.segment.get_y(self.curr_x) > segment.get_y(self.curr_x):
                successor = root
                root = root.left
            else:
                root = root.right
        return successor


    def find_predecessor(self, root: Node, segment: Segment):
        predecessor = None
        while root:
            if root.segment.get_y(self.curr_x) < segment.get_y(self.curr_x):
                predecessor = root
                root = root.right
            else:
                root = root.left
        return predecessor
    

    def swap_node_segments(self, root, segment1: Segment, segment2: Segment):
        node1, node2 = self.find_two_nodes_by_segments(root, segment1, segment2)

        if not node1 or not node2:
            return

        node1.segment, node2.segment = node2.segment, node1.segment
