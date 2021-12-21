import itertools
import numpy as np
import collections
from scipy.spatial.transform import Rotation as R

# Initialize rotation matricies
rot_90_x = R.from_rotvec(90 * np.array([1, 0, 0]), degrees=True).as_matrix().astype(int)
rot_90_y = R.from_rotvec(90 * np.array([0, 1, 0]), degrees=True).as_matrix().astype(int)
rot_90_z = R.from_rotvec(90 * np.array([0, 0, 1]), degrees=True).as_matrix().astype(int)

def axis_permutations(vec):
    for _ in range(4):
        for _ in range(4):
            yield vec
            vec = rot_90_x.dot(vec)
        vec = rot_90_y.dot(vec)

    for _ in range(2):
        vec = rot_90_z.dot(vec)
        for _ in range(4):
            yield vec
            vec = rot_90_x.dot(vec)
        vec = rot_90_z.dot(vec)

def get_rotation(index):
    rot = np.identity(3)
    for _ in range(4):
        for _ in range(4):
            if index == 0: return rot
            index -= 1
            rot = rot_90_x.dot(rot)
        rot = rot_90_y.dot(rot)

    for _ in range(2):
        rot = rot_90_z.dot(rot)
        for _ in range(4):
            if index == 0: return rot
            index -= 1
            rot = rot_90_x.dot(rot)
        rot = rot_90_z.dot(rot)

class Scanner():
    def __init__(self, local_detections) -> None:
        self.local_detections = local_detections
        self.origin = None
        self.world_detections = None
        self.permutations = list([p for x in local_detections for p in axis_permutations(x)])

scanners: list[Scanner] = []
scanner_detections = []

# Read in scanner
lines = [x.strip() for x in open('input.txt', 'r')]
for l in lines:
    if l.startswith('---'):
        scanner_detections.append([])
    elif l == '':
        continue
    else:
        scanner_detections[-1].append(np.array([int(v) for v in l.split(',')], dtype=int))

scanners = [Scanner(d) for d in scanner_detections]

# Scanner 0 is [0, 0, 0]
scanners[0].world_detections = scanners[0].local_detections
scanners[0].origin = np.array([0, 0, 0])

# All detections of scanner 0 are unique
unique_beacons = set()
for d in scanners[0].world_detections:
    unique_beacons.add(tuple(d))

def calc_common_origin(world_detections, all_permutations):
    origin_counter = collections.Counter()
    # all_permutations = list([p for x in local_beacons for p in axis_permutations(x)])
    for world_beacon in world_detections:
        for i, p in enumerate(all_permutations):
            origin = (tuple(world_beacon - p), i % 24)
            origin_counter[origin] += 1
            if origin_counter[origin] >= 12:
                most_common, counter = origin_counter.most_common()[0]
                return most_common, counter
    
    most_common, counter = origin_counter.most_common()[0]
    return most_common, counter

new_scanners = []
new_scanners.append((0, scanners[0]))

while len(new_scanners) > 0:
    # Get a new scanner to test remaining
    new_scanners.reverse()
    ci, current_scanner = new_scanners.pop()
    # print('Starting at scanner ', ci)
    for i, scanner in enumerate(scanners):
        # if scanner has an origin, we already mapped it
        if scanner.origin is not None: continue

        # try to calculate a common origin
        origin, counter = calc_common_origin(current_scanner.world_detections, scanner.permutations)
        origin, perm_index = origin
        # print('Checking paths to scanner ', i, ' -> found ', origin, ' as origin, with ', counter, ' paths')

        if counter < 12: continue
        rot = get_rotation(perm_index)
        scanner.origin = origin
        scanner.world_detections = np.array([scanner.origin + rot.dot(b) for b in scanner.local_detections], dtype=int)
        for c in scanner.world_detections:
            unique_beacons.add(tuple(c))
        new_scanners.append((i, scanner))
        # print('! Found origin of scanner ', i)
        # print([b for b, c in unique_beacons.most_common() if c > 1])

print(len(unique_beacons))

exit()

max_distance = None
for s1 in scanners:
    for s2 in scanners:
        d = np.abs(np.array(s1.origin) - np.array(s2.origin))
        d = np.sum(d)
        if max_distance is None:
            max_distance = d
        elif max_distance < d:
            max_distance = d

print(max_distance)