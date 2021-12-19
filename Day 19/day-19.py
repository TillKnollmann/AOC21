import time
from tqdm import tqdm

from importlib.machinery import SourceFileLoader

lib = SourceFileLoader("lib", "lib.py").load_module()

from aocd import get_data
from aocd import submit

day = 19
path = ""

# possible axis orientations
orientations = [
    (1, 1, 1),
    (1, 1, -1),
    (1, -1, 1),
    (1, -1, -1),
    (-1, 1, 1),
    (-1, 1, -1),
    (-1, -1, 1),
    (-1, -1, -1),
]

# possible axis remappings
axis_maps = [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]


def parseInput(input: list):
    """Parses the input and returns a list of point sets

    Args:
        input (list): A list of strings

    Returns:
        list: A list of point sets. The set at position i is associated with scanner i
    """
    result = []

    current_scan = []
    for i in range(len(input)):
        # get current line
        current_line = input[i].replace("\n", "").strip()
        if "scanner" in current_line:
            # we need a new scanner
            current_scan = []
        elif len(current_line) > 0:
            # we can the line later
            current_scan.append(current_line)

        if (len(current_line) == 0) or (i == len(input) - 1):
            # the point set for the last scanner is in current_scan
            result.append(parse_scanner_input(current_scan))

    return result


def parse_scanner_input(input: list) -> set:
    """Generates a set of points out of a list of string

    Args:
        input (list): Input points, one per line

    Returns:
        set: Point set
    """
    result = set()
    for line in input:
        values = line.split(",")
        result.add((int(values[0]), int(values[1]), int(values[2])))
    return result


def transform_scan(scan: set, axis_map: tuple, orientation: tuple) -> list:
    """Transforms all points of a point set in scan according to the axis remaps and the orientation

    Args:
        scan (set): A set of all points to be transformed
        axis_map (tuple): A mapping from the axes to each other
        orientation (tuple): A tuple determining how each axis is oriented

    Returns:
        list: A list of the transformed points
    """
    result = []
    for point in scan:
        # each coordinate of a point is translated to the axes given by axis_map and then either flipped according to the orientation of the target axis
        result.append(
            (
                orientation[0] * point[axis_map[0]],
                orientation[1] * point[axis_map[1]],
                orientation[2] * point[axis_map[2]],
            )
        )
    return result


def align(scan_A: set, scan_B: set) -> tuple:
    """Tries to align points of scan_B to points of scan_A

    Args:
        scan_A (set): Aligned point set
        scan_B (set): Point set to be aligned

    Returns:
        tuple: set of aligned points, if the alignment succeeded, the coordinate of the scanner of scan_B
    """
    # try each axis permutation
    for axis_map in axis_maps:
        # try each possible axis orientation
        for orientation in orientations:
            # transform the points of B according to the translated system
            scan_B_transformed = transform_scan(scan_B, axis_map, orientation)
            # align each possible pair
            for point_A in scan_A:
                for point_B in scan_B_transformed:
                    # store the alignment, i.e., the offset between the two reference points
                    alignment = (
                        point_B[0] - point_A[0],
                        point_B[1] - point_A[1],
                        point_B[2] - point_A[2],
                    )
                    # count matches
                    matches = 0
                    # get aligned beacons
                    aligned_beacons = []
                    # test each point
                    for other_point_B in scan_B_transformed:
                        # translate the point according to the alignment
                        other_point_B_aligned = (
                            other_point_B[0] - alignment[0],
                            other_point_B[1] - alignment[1],
                            other_point_B[2] - alignment[2],
                        )
                        # check if the point has a match in scan_A
                        if other_point_B_aligned in scan_A:
                            matches += 1
                        aligned_beacons.append(other_point_B_aligned)
                    if matches >= 12:
                        # We succeeded
                        return aligned_beacons, True, alignment
    return None, False, None


def align_scanners(scanners: list) -> list:
    """Aligns the scanners

    Args:
        scanners (list): A list of the point sets of the scanners 

    Returns:
        list: A list containing: The number of beacons, the largest manhattan distance between two scanners
    """
    # Initally only scanner zero is aligned
    scanner_0 = scanners[0]
    # will store all beacons that are aligned
    all_aligned_beacons = list(scanner_0.copy())
    # stores the aligned beacons for each scanner
    aligned_beacons_scanner = {}
    aligned_beacons_scanner[0] = scanner_0.copy()
    # stores the aligned scanners
    aligned_scanners = set([0])
    # stores the scanners which are not the zeroth
    not_zero_scanners = set([i for i in range(1, len(scanners))])
    # stores pairs of scanners such that the second could not be aligned to the first
    cannot_be_aligned = set()
    # stores the positions of the scanners
    scanner_positions = [(0, 0, 0)]

    print("Aligning " + str(len(scanners) - 1) + " scanners")

    with tqdm(total=len(scanners) - 1, unit="Sc") as pbar:
        while len(aligned_scanners) < len(scanners):
            # we still need to align some scanner
            for not_aligned in not_zero_scanners:
                if not not_aligned in aligned_scanners:
                    is_aligned = False
                    # get some scanner that we try to align to
                    for aligned in aligned_scanners:
                        if not (aligned, not_aligned) in cannot_be_aligned:
                            # try to align
                            mapped_points, success, scanner_pos = align(
                                aligned_beacons_scanner[aligned], scanners[not_aligned]
                            )
                            if success:
                                is_aligned = True
                                # store the scanner
                                aligned_scanners.add(not_aligned)
                                # store the beacons
                                aligned_beacons_scanner[not_aligned] = mapped_points
                                all_aligned_beacons += mapped_points
                                # store the scanner position
                                scanner_positions.append(scanner_pos)
                                break
                            else:
                                # remember the failure
                                cannot_be_aligned.add((aligned, not_aligned))
                    if is_aligned:
                        pbar.update(1)

    print("All Scanners aligned!")

    # remove duplicates
    all_aligned_beacons = set(all_aligned_beacons)

    return len(all_aligned_beacons), get_max_Manhattan_dist(scanner_positions)


def get_max_Manhattan_dist(points: list) -> int:
    """Returns the maximum manhattan distance between any two points in the list

    Args:
        points (list): Set of points to compare

    Returns:
        int: The largest manhattan distance for all point pairs
    """
    return max(
        [
            get_Manhattan_dist(points[i], points[j])
            for i in range(len(points))
            for j in range(len(points))
        ]
    )


def get_Manhattan_dist(point_A: tuple, point_B: tuple) -> int:
    """Returns the Manhattan distance between point_A and point_B

    Args:
        point_A (tuple): First Point
        point_B (tuple): Second Point

    Returns:
        int: The manhattan distance between both points
    """
    return sum([abs(point_A[i] - point_B[i]) for i in range(len(point_A))])


# cache the result
result_input = None


def part1(data, measure=False, isInput=False):
    global result_input

    startTime = time.time()
    result_1 = None

    input = parseInput(data)

    result = align_scanners(input)

    if isInput:
        # cache the result
        result_input = result

    result_1 = result[0]

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 1 took: " + str(executionTime) + " s")
    return result_1


def part2(data, measure=False, isInput=False):
    global result_input
    startTime = time.time()
    result_2 = None

    input = parseInput(data)

    # if the result is cached, retrieve it
    if isInput and result_input:
        result_2 = result_input[1]
    else:
        result_2 = align_scanners(input)[1]

    executionTime = round(time.time() - startTime, 2)
    if measure:
        print("\nPart 2 took: " + str(executionTime) + " s")
    return result_2


def runTests(test_sol, path):
    test_res = []

    all_check = True

    paths = lib.getTestPaths(path)

    test_res += list(map(part1, map(lib.getDataLines, paths)))
    test_res += list(map(part2, map(lib.getDataLines, paths)))

    success = [test_sol[i] == test_res[i] for i in range(len(test_sol))]

    for i in range(len(test_sol)):
        output = "Test " + str(i + 1)
        output = (
            "".join([output, " Success!"])
            if success[i]
            else "".join(
                [
                    output,
                    " Failed! Expected ",
                    str(test_sol[i]),
                    " received ",
                    str(test_res[i]),
                ]
            )
        )
        all_check = False if test_sol[i] != test_res[i] else all_check
        print(output)

    return all_check


def main():
    global path
    path = "Day " + str(day) + "/"

    test_sol = [79, 3621]  # Todo put in test solutions

    test = True  # Todo

    sol1 = sub1 = True  # Todo
    sol2 = sub2 = True  # Todo

    if test:
        if not runTests(test_sol, path):
            sub1 = sub2 = False

    data_main = get_data(day=day, year=2021).splitlines()

    if sol1:
        result_1 = part1(data_main, True, True)
        print("Result Part 1: " + str(result_1))

    if sol2:
        result_2 = part2(data_main, True, True)
        print("Result Part 2: " + str(result_2))

    print("\n")

    if sub1:
        submit(int(result_1), part="a", day=day, year=2021)

    if sub2:
        submit(int(result_2), part="b", day=day, year=2021)


if __name__ == "__main__":
    main()

