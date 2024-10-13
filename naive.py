from utilities import *
import sys
from convert_input import *

def dummy_number_of_intersections(set: TestSet):
    num_of_inter = 0
    
    for i in range(0, len(set.segments)):
        for j in range(i+1, len(set.segments)):
            intersection_point = intersection(set.segments[i], set.segments[j])
            if intersection_point:
                num_of_inter +=1
    
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
        print(str(dummy_number_of_intersections(set)))
        i += 1
        

if __name__ == "__main__":
    main()