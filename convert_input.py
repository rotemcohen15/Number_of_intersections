from utilities import *

def convert_input_to_testsets(lines: list):
    num_tests = int(lines[0])
    test_sets = []
    input_valid = True

    i = 1
    while i < len(lines) and input_valid:
        if i == len(lines)-1:
            if int(lines[i]) == -1:
                break
            input_valid = False
            break
        
        num_segments = int(lines[i])
        test_set = []
        for j in range(1, num_segments+1):
            numbers = (lines[i+j]).split()
            if len(numbers) != 4 :
                input_valid = False
                break

            p = Point(float(numbers[0]), float(numbers[1]))
            q = Point(float(numbers[2]), float(numbers[3]))
            seg = Segment(j-1, p, q)
            test_set.append(seg)

        test_sets.append(TestSet(test_set))
        i = i + num_segments + 1

    if not input_valid:
        return "Input is invalid", None
    
    if len(test_sets) != num_tests:
        return "Number of tests doesn't match the input", None
    
    return None, test_sets
        

